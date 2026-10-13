#!/usr/bin/env python3
"""Transcreve a narração de um vídeo/áudio com marcação de tempo por frase (VAD Silero + Whisper small,
via sherpa-onnx, 100% local). Modelos em /opt/ml (instalados por scripts/setup.sh na raiz do repo).

Uso: python3 transcrever.py arquivo.(mp4|mp3|wav) [idioma: pt|es|en] [--vocal]
  --vocal  separa a voz da música antes (spleeter), útil quando a música está alta por baixo.
Saída: linhas "[ini → fim] texto" no terminal e <arquivo>.transcricao.tsv ao lado.

Também é importado pelo montar_criativo.py (funções `transcrever` e `tempo_da_frase`).
"""
import subprocess, sys, tempfile, unicodedata
from pathlib import Path

ML = Path("/opt/ml")


def disponivel():
    try:
        import sherpa_onnx  # noqa: F401
    except ImportError:
        return False
    return (ML / "silero_vad.onnx").exists() and (ML / "sherpa-onnx-whisper-small").exists()


def _wav16k(src, dst):
    # normaliza o volume antes: voz muito baixa faz o Whisper alucinar
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5",
                    "-ac", "1", "-ar", "16000", str(dst)], check=True)


def separar_voz(src, pasta):
    subprocess.run([str(ML / "sp/bin/spleeter"), "separate", "-p", "spleeter:2stems", "-o", str(pasta), str(src)],
                   check=True, capture_output=True,
                   env={"MODEL_PATH": str(ML / "pretrained_models"), "PATH": "/usr/bin:/bin"})
    return next(Path(pasta).rglob("vocals.wav"))


def transcrever(src, lang="pt", vocal=False):
    """Retorna [(inicio_s, fim_s, texto)] por frase."""
    import sherpa_onnx
    import soundfile as sf
    tmp = Path(tempfile.mkdtemp())
    entrada = separar_voz(src, tmp) if vocal else src
    _wav16k(entrada, tmp / "a.wav")
    audio, sr = sf.read(tmp / "a.wav", dtype="float32")

    vcfg = sherpa_onnx.VadModelConfig()
    vcfg.silero_vad.model = str(ML / "silero_vad.onnx")
    vcfg.silero_vad.min_silence_duration = 0.25
    vcfg.silero_vad.min_speech_duration = 0.2
    vcfg.silero_vad.max_speech_duration = 12
    vcfg.sample_rate = sr
    vad = sherpa_onnx.VoiceActivityDetector(vcfg, buffer_size_in_seconds=900)

    m = ML / "sherpa-onnx-whisper-small"
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(m / "small-encoder.int8.onnx"), decoder=str(m / "small-decoder.int8.onnx"),
        tokens=str(m / "small-tokens.txt"), language=lang, task="transcribe", num_threads=4)

    # 1) VAD só marca os trechos de fala (copia os índices ANTES do pop: o buffer é reaproveitado)
    win = vcfg.silero_vad.window_size
    trechos = []

    def drenar():
        while not vad.empty():
            seg = vad.front
            trechos.append((seg.start, seg.start + len(seg.samples)))
            vad.pop()
    for i in range(0, len(audio), win):
        vad.accept_waveform(audio[i:i + win]); drenar()
    vad.flush(); drenar()

    # 2) Whisper transcreve cada trecho recortado do áudio original (0,1 s de folga)
    pad = int(0.1 * sr)
    linhas = []
    for a, b in trechos:
        s = rec.create_stream()
        s.accept_waveform(sr, audio[max(a - pad, 0):min(b + pad, len(audio))])
        rec.decode_stream(s)
        linhas.append((a / sr, b / sr, s.result.text.strip()))
    return linhas


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join("".join(c if c.isalnum() else " " for c in s).split())   # ignora pontuação


def tempo_da_frase(linhas, frase, depois_de=0.0):
    """Tempo estimado (s) em que `frase` começa a ser falada (proporcional aos caracteres do trecho).
    Retorna None se não achar."""
    alvo = _norm(frase)
    for a, b, t in linhas:
        if b < depois_de:
            continue
        nt = _norm(t)
        i = nt.find(alvo)
        if i >= 0 and nt:
            return round(a + (b - a) * i / len(nt), 2)
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = Path(args[0]).resolve()
    lang = args[1] if len(args) > 1 else "pt"
    linhas = transcrever(src, lang, "--vocal" in sys.argv)
    out = src.with_suffix(".transcricao.tsv")
    with open(out, "w") as f:
        for a, b, t in linhas:
            print(f"[{a:6.2f} → {b:6.2f}] {t}")
            f.write(f"{a:.2f}\t{b:.2f}\t{t}\n")
    print(f"\nSalvo em {out}")


if __name__ == "__main__":
    main()
