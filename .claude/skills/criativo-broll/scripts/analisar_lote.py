#!/usr/bin/env python3
"""Analisa um LOTE de criativos de referência e resume os padrões de edição numa tabela.

Uso:
  python3 analisar_lote.py lista.tsv pasta_saida      # lista: id_do_drive<TAB>titulo<TAB>idioma (pt|es)
  python3 analisar_lote.py pasta_com_mp4s pasta_saida  # vídeos locais (idioma pelo nome: 'salsa' → es)

Baixa do Drive arquivos públicos via drive.usercontent.google.com (o domínio precisa estar liberado na rede
do ambiente). Para cada vídeo mede: cortes, ritmo, gancho (fala + folha dos 6 primeiros s), frase e entrada
visual do CTA, fim da voz, cauda, níveis de voz e música (com spleeter, se instalado) e se a música toca
desde o início. Gera <saida>/resumo.tsv, <saida>/<nome>/medidas.json, gancho.png e transcricao.tsv.
"""
import json, statistics, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transcrever as tr  # noqa: E402

ML = Path("/opt/ml")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duracao(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout)


def baixar(fid, dst):
    if dst.exists() and dst.stat().st_size > 1_000_000:
        return True
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    r = sh(["curl", "-sSL", "--fail", "-o", str(dst), url])
    if r.returncode != 0 or not dst.exists() or dst.stat().st_size < 1_000_000:
        print(f"  ✗ não baixou ({r.stderr.strip()[:120]})")
        return False
    return True


def cortes(v, dur):
    r = sh(["ffmpeg", "-hide_banner", "-i", str(v), "-filter:v", "select='gt(scene,0.22)',showinfo", "-an", "-f", "null", "-"])
    ts = [float(x.split(":")[1]) for x in r.stderr.split() if x.startswith("pts_time:")]
    c = [0.0] + ts + [dur]
    return [(c[i], c[i + 1] - c[i]) for i in range(len(c) - 1) if c[i + 1] - c[i] > 0.02]


def lufs(arq, a, b):
    r = sh(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{a:.2f}", "-to", f"{b:.2f}", "-i", str(arq),
            "-af", "ebur128=framelog=quiet", "-f", "null", "-"])
    for l in r.stderr.split("Summary")[-1].splitlines():
        if "I:" in l:
            try:
                return float(l.split()[1])
            except (ValueError, IndexError):
                return None
    return None


def entrada_cta(v, dur):
    """Primeiro instante (2ª metade do vídeo) em que aparece a faixa verde do CTA na área do texto."""
    import numpy as np
    w, h = 108, 192
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{dur * 0.5:.1f}", "-i", str(v), "-vf",
                        f"fps=10,scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3).astype(int)
    zona = fr[:, int(h * 0.25):int(h * 0.55)]
    verde = ((zona[..., 1] > 110) & (zona[..., 0] < 60) & (zona[..., 2] < 70)).mean(axis=(1, 2))
    idx = np.where(verde > 0.02)[0]
    # exige que fique na tela até o fim (o CTA não sai mais)
    for i in idx:
        if (verde[i:] > 0.015).mean() > 0.9:
            return round(dur * 0.5 + i / 10, 2)
    return None


def musica_desde_inicio(acomp):
    """Periodicidade da batida em 1–15 s no acompanhamento separado (≥0,5 = batida clara = música presente)."""
    import numpy as np, librosa
    y, sr = librosa.load(str(acomp), sr=22050, offset=1, duration=14)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=256)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
    env = np.maximum(0, np.diff(np.log(S[(f > 30) & (f < 150)].sum(0) + 1e-6))); env -= env.mean()
    ac = np.correlate(env, env, "full")[len(env) - 1:]; ac /= ac[0]
    lags = np.arange(len(ac)) * 256 / sr; m = (lags > 0.3) & (lags < 1.2)
    i = int(np.argmax(ac[m]))
    return round(float(ac[m][i]), 2), round(60 / float(lags[m][i]))


def analisar(v, idioma, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    dur = duracao(v)
    cs = cortes(v, dur)
    ds = [d for _, d in cs]
    med = {"arquivo": v.name, "duracao": round(dur, 2), "cenas": len(cs), "mediana": round(statistics.median(ds), 2),
           "media": round(statistics.mean(ds), 2), "max": round(max(ds), 2),
           "pct_acima_2s": round(100 * sum(d > 2.05 for d in ds) / len(ds)),
           "gancho_cortes": [round(d, 2) for t, d in cs if t < 5]}
    # folha do gancho (0–6 s, 4 fps)
    sh(["ffmpeg", "-loglevel", "error", "-y", "-t", "6", "-i", str(v), "-vf",
        "fps=4,scale=180:320,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='%{pts\\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black,tile=12x2",
        str(pasta / "gancho.png")])
    # fala
    if tr.disponivel():
        linhas = tr.transcrever(v, idioma)
        (pasta / "transcricao.tsv").write_text("".join(f"{a:.2f}\t{b:.2f}\t{t}\n" for a, b, t in linhas))
        if linhas:
            med["voz_inicio"] = round(linhas[0][0], 2)
            med["voz_fim"] = round(linhas[-1][1], 2)
            med["cauda"] = round(dur - linhas[-1][1], 2)
            med["gancho_falado"] = linhas[0][2][:160]
            frases = ["clique no botao", "clica no botao", "dale clic", "haz clic", "da clic", "botao aqui embaixo",
                      "boton aqui abajo", "botao abaixo", "boton de abajo", "clic al boton", "clique aqui"]
            ach = [x for x in (tr.tempo_da_frase(linhas, f, linhas[-1][1] - 25) for f in frases) if x is not None]
            med["cta_fala"] = min(ach) if ach else None
    med["cta_visual"] = entrada_cta(v, dur)
    if med.get("cta_fala") and med["cta_visual"]:
        med["cta_antecedencia"] = round(med["cta_fala"] - med["cta_visual"], 2)
    # níveis
    if (ML / "sp/bin/spleeter").exists():
        wav = pasta / "audio.wav"
        sh(["ffmpeg", "-loglevel", "error", "-y", "-i", str(v), "-vn", "-ac", "2", "-ar", "44100", str(wav)])
        sh([str(ML / "sp/bin/spleeter"), "separate", "-p", "spleeter:2stems", "-o", str(pasta), str(wav)],
           env={"MODEL_PATH": str(ML / "pretrained_models"), "PATH": "/usr/bin:/bin"})
        voc, aco = pasta / "audio" / "vocals.wav", pasta / "audio" / "accompaniment.wav"
        if voc.exists():
            fim = med.get("voz_fim", dur - 8)
            med["lufs_voz"] = lufs(voc, 1, fim - 1)
            med["lufs_musica_sob_voz"] = lufs(aco, 1, fim - 1)
            med["lufs_musica_inicio_0_20"] = lufs(aco, 0.5, 20)
            med["lufs_musica_cauda"] = lufs(aco, fim + 0.3, dur)
            med["batida_inicio"], med["bpm"] = musica_desde_inicio(aco)
            if med["lufs_voz"] and med["lufs_musica_sob_voz"]:
                med["musica_abaixo_da_voz_LU"] = round(med["lufs_voz"] - med["lufs_musica_sob_voz"], 1)
        wav.unlink(missing_ok=True)
    else:
        med["lufs_mix_0_20"] = lufs(v, 0.5, 20)
    (pasta / "medidas.json").write_text(json.dumps(med, indent=2, ensure_ascii=False))
    return med


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    itens = []
    if src.is_dir():
        itens = [(None, p.name, "es" if "salsa" in p.name.lower() else "pt", p) for p in sorted(src.glob("*.mp4"))]
    else:
        for l in src.read_text().splitlines():
            if l.strip() and not l.startswith("#"):
                fid, tit, lang = (l.split("\t") + ["", "pt"])[:3]
                itens.append((fid, tit, lang or "pt", out / "videos" / tit))
    (out / "videos").mkdir(exist_ok=True)
    linhas = []
    for fid, tit, lang, p in itens:
        print(f"▶ {tit}")
        if fid and not baixar(fid, p):
            linhas.append({"arquivo": tit, "erro": "download"}); continue
        try:
            m = analisar(p, lang, out / Path(tit).stem.replace(" ", "_"))
            print("  ", {k: m.get(k) for k in ("duracao", "cenas", "mediana", "pct_acima_2s", "cta_antecedencia",
                                                "cauda", "musica_abaixo_da_voz_LU", "batida_inicio")})
            linhas.append(m)
        except Exception as e:  # um vídeo ruim não derruba o lote
            print("   erro:", e); linhas.append({"arquivo": tit, "erro": str(e)[:200]})
    cols = ["arquivo", "duracao", "cenas", "mediana", "media", "max", "pct_acima_2s", "gancho_cortes", "voz_inicio",
            "voz_fim", "cauda", "cta_fala", "cta_visual", "cta_antecedencia", "lufs_voz", "lufs_musica_sob_voz",
            "musica_abaixo_da_voz_LU", "lufs_musica_inicio_0_20", "lufs_musica_cauda", "batida_inicio", "bpm",
            "gancho_falado", "erro"]
    with open(out / "resumo.tsv", "w") as f:
        f.write("\t".join(cols) + "\n")
        for m in linhas:
            f.write("\t".join(str(m.get(c, "")) for c in cols) + "\n")
    ok = [m for m in linhas if "erro" not in m]
    if ok:
        print("\n== PADRÃO DO LOTE (mediana entre os vídeos)")
        for c in ["duracao", "cenas", "mediana", "pct_acima_2s", "voz_inicio", "cauda", "cta_antecedencia",
                  "musica_abaixo_da_voz_LU", "batida_inicio", "bpm"]:
            vals = [m[c] for m in ok if isinstance(m.get(c), (int, float))]
            if vals:
                print(f"  {c:28s} mediana {statistics.median(vals):7.2f} | faixa {min(vals):.2f}–{max(vals):.2f} | n={len(vals)}")
    print(f"\nResumo: {out / 'resumo.tsv'}")


if __name__ == "__main__":
    main()
