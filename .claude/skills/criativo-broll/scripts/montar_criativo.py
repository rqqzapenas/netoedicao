#!/usr/bin/env python3
"""Monta um criativo b-roll no método do Neto como projeto HyperFrames pronto para render.

Uso:
  python3 montar_criativo.py spec.json [--render] [--seed=N]

Formato do spec.json: ver ../SKILL.md, seção "Spec". Regras e números: SKILL.md + references/.
Depende de python3, ffmpeg/ffprobe; transcrição (CTA e sincronia automáticos) usa sherpa-onnx
instalado por scripts/setup.sh na raiz do repo — sem ele, use "cta_tempo" e "tempo" nas âncoras.
"""
import json, random, re, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import transcrever as tr  # noqa: E402

# ---------------------------------------------------------------- regras do método (fonte: SKILL.md)
W, H, FPS = 1080, 1920, 30
MAX_CENA = 2.0           # regra do dono: nenhuma cena passa de 2 s
MIN_CENA = 0.2           # flash mais curto permitido
VOZ_INICIO = 0.2         # a voz entra praticamente no primeiro frame (referências: 0,18–0,25 s)
CAUDA = 9.0              # só música + CTA + b-roll depois da voz (referências: 6,4 s salsas, 11 s gelato)
CTA_ANTES_DA_FALA = 0.4  # CTA visual entra ~0,3–0,6 s ANTES da voz falar "clique no botão"
LUFS_VOZ = -16.0
LUFS_MUSICA = -30.0      # 12–18 LU abaixo da voz nas referências, constante do começo ao fim
FRASES_CTA = ["clique no botao", "clica no botao", "clique no botão", "dale clic", "haz clic", "da clic",
              "botao aqui embaixo", "botón aquí abajo", "boton aqui abajo", "botao abaixo", "boton de abajo"]
CTA_PADRAO = {"pt": ["Clique no", "botão abaixo"], "es": ["Haz clic en", "el botón de abajo"]}

# Ritmo medido nas referências (duração, categorias preferidas). Gancho = só o objeto do hook falado.
GANCHO = [1.43, 1.13, 0.83, 0.67, 0.27, 1.13]          # gelato; salsas: 1.43 1.90 0.27 0.37 0.63
CORPO = [  # processo calmo 1,6–2,0 s intercalado com rajadas 0,6–0,9 s e reação a cada ~20 s
    (1.20, ["processo"]), (0.93, ["processo"]), (0.20, ["processo", "textura"]), (1.60, ["processo"]),
    (1.10, ["processo"]), (2.00, ["processo", "textura"]), (1.67, ["textura", "final"]),
    (1.43, ["textura", "final"]), (1.83, ["textura"]), (1.83, ["textura", "final"]),
    (1.90, ["final", "textura"]), (1.93, ["final"]), (2.00, ["final"]), (2.00, ["reacao", "final"]),
    (1.27, ["processo"]), (1.50, ["processo"]), (1.50, ["processo", "textura"]),
    (0.60, ["final", "textura"]), (0.70, ["final"]), (0.70, ["textura"]), (1.07, ["textura"]),
    (1.30, ["textura"]), (0.60, ["textura"]), (2.00, ["final"]), (2.00, ["textura", "final"]),
    (0.27, ["textura"]), (2.00, ["textura"]), (0.33, ["textura"]), (2.00, ["textura", "final"]),
    (1.83, ["reacao", "final"]), (2.00, ["reacao", "textura"]), (0.57, ["reacao", "final"]),
    (1.93, ["final", "textura"]), (1.20, ["final"]), (1.40, ["final"]), (1.43, ["final"]),
    (0.70, ["textura"]), (0.73, ["textura"]), (0.87, ["textura"]), (0.77, ["textura"]),
    (0.93, ["final"]), (1.80, ["final", "textura"]), (1.63, ["textura"]), (1.27, ["textura", "final"]),
]
CAUDA_RITMO = [(2.0, ["final", "textura"]), (1.63, ["final"]), (2.0, ["textura"]), (1.77, ["final"])]
CATEGORIAS = ["gancho", "final", "processo", "textura", "reacao"]


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duracao(path):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout)


def tem_video(path):
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=codec_type",
              "-of", "csv=p=0", str(path)])
    return "video" in out.stdout


def categoria(nome):
    base = Path(nome).stem.lower()
    return next((c for c in CATEGORIAS if base.startswith(c)), "geral")


def seguro(nome):
    return re.sub(r"[^\w.\-]", "_", Path(nome).name)


# ---------------------------------------------------------------- áudio
def preparar_voz(src, dst, apertar_pausas=False):
    """Voz entregue pelo usuário (MiniMax/ElevenLabs). Só tira o silêncio do começo e normaliza.
    NUNCA corta o fim. `apertar_pausas` encurta pausas > 0,45 s para 0,3 s (use só se a voz vier arrastada)."""
    filtros = ["silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03"]
    if apertar_pausas:
        filtros.append("silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-50dB:stop_silence=0.3")
    filtros += [f"loudnorm=I={LUFS_VOZ}:TP=-1.5:LRA=11", "apad=pad_dur=0.25"]   # 0,25 s de respiro no final
    sh(["ffmpeg", "-y", "-i", str(src), "-af", ",".join(filtros), "-ar", "48000", "-ac", "2", str(dst)])
    bruto, final = duracao(src), duracao(dst)
    if final < bruto * 0.85:
        print(f"ATENÇÃO: a voz encolheu de {bruto:.1f}s para {final:.1f}s — confira se nenhuma palavra foi comida.")


def preparar_musica(src, dst, offset, dur):
    """Trecho da música a partir de `offset` (s dentro do arquivo), com loop se faltar, nível constante.
    Entra e sai seca (15 ms anti-clique)."""
    sh(["ffmpeg", "-y", "-stream_loop", "-1", "-ss", f"{offset}", "-i", str(src), "-t", f"{dur:.3f}",
        "-af", f"loudnorm=I={LUFS_MUSICA}:TP=-2:LRA=11,afade=t=in:d=0.015,"
               f"afade=t=out:st={max(dur - 0.015, 0):.3f}:d=0.015",
        "-ar", "48000", "-ac", "2", str(dst)])


# ---------------------------------------------------------------- b-roll
class Pool:
    """Banco de b-roll. Regra do dono: NUNCA repetir o mesmo trecho de um b-roll. Cada arquivo pode voltar,
    mas sempre num trecho que ainda não apareceu (sem sobreposição) e a ≥ 15 s do último uso na timeline."""
    MARGEM = 0.15        # folga entre trechos do mesmo arquivo
    INTERVALO = 15.0     # distância mínima na timeline entre dois usos do mesmo arquivo

    def __init__(self, arquivos, rng):
        self.rng = rng
        self.clips = {}
        self.repetidos = 0
        for f in arquivos:
            D = duracao(f)
            if D >= MIN_CENA + 0.1:
                self.clips[f.name] = {"src": f, "dur": D, "cat": categoria(f.name), "usados": [], "tempos": []}
        if not self.clips:
            sys.exit("Nenhum b-roll utilizável encontrado.")

    def livres(self, c, d):
        """Inícios possíveis (passo 0,1 s) cujo trecho [s, s+d] não encosta em nenhum trecho já usado."""
        max_ini = c["dur"] - d - 0.05
        if max_ini < 0:
            return []
        cands = [round(x * 0.1, 2) for x in range(int(max_ini * 10) + 1)]
        return [s for s in cands if all(s + d + self.MARGEM <= u0 or s >= u1 + self.MARGEM for u0, u1 in c["usados"])]

    def trecho(self, c, dur, t, permitir_repetir=False):
        d = min(dur, c["dur"] - 0.05)
        cands = self.livres(c, d)
        if not cands:
            if not permitir_repetir:
                return None
            self.repetidos += 1
            cands = [round(x * 0.1, 2) for x in range(int(max(c["dur"] - d - 0.05, 0) * 10) + 1)] or [0.0]
        if c["usados"]:   # o mais longe possível do que já apareceu
            ini = max(cands, key=lambda s: min(abs(s - u0) for u0, _ in c["usados"]))
        else:
            ini = cands[0] if c["cat"] in ("gancho", "final") else self.rng.choice(cands[: max(1, len(cands) // 2)])
        c["usados"].append((ini, ini + d)); c["tempos"].append(t)
        return ini, d

    def escolher(self, cats, dur, anterior, t, evitar=()):
        def score(c):
            rank = cats.index(c["cat"]) if c["cat"] in cats else (len(cats) + (0 if c["cat"] == "geral" else 1))
            recente = bool(c["tempos"]) and t - c["tempos"][-1] < self.INTERVALO
            return (not self.livres(c, min(dur, c["dur"] - 0.05)), c["src"] == anterior, c["src"].name in evitar,
                    recente, rank, len(c["usados"]), self.rng.random())
        c = min(self.clips.values(), key=score)
        r = self.trecho(c, dur, t)
        if r is None:     # banco esgotado: repete trecho, mas avisa no relatório
            r = self.trecho(c, dur, t, permitir_repetir=True)
        return (c,) + r


def planejar(total, cta_ini, pool, ancoras, gancho_clips, rng):
    """Lista de cenas cobrindo 0→total. `ancoras` = [(tempo, nome_arquivo)] ordenadas."""
    cenas, t, anterior = [], 0.0, None
    pend = list(ancoras)
    # 1) GANCHO: só o(s) clipe(s) que mostram exatamente o que a primeira frase fala
    if gancho_clips:
        for i, d in enumerate(GANCHO):
            c = pool.clips[gancho_clips[i % len(gancho_clips)]]
            ini, dd = pool.trecho(c, d, t, permitir_repetir=True)
            cenas.append({"inicio": t, "dur": dd, "clip": c, "in": ini, "motivo": "gancho"})
            t += dd; anterior = c["src"]
    # 2) CORPO + CAUDA, respeitando as âncoras de sincronia
    i_corpo = i_cauda = 0
    while t < total - 1e-6:
        if t >= cta_ini:
            d, cats = CAUDA_RITMO[i_cauda % len(CAUDA_RITMO)]; i_cauda += 1
        else:
            d, cats = CORPO[i_corpo % len(CORPO)]; i_corpo += 1
        forcado = None
        while pend and pend[0][0] < t - 0.3:           # âncora que ficou para trás (ex.: dentro do gancho)
            pend.pop(0)
        if pend and pend[0][0] < t + d:
            ta, nome = pend[0]
            if nome is None:                             # ponto de corte (pico do flash branco)
                if ta - t >= 0.2:
                    d = ta - t
                pend.pop(0)
            elif ta - t >= 0.45:                         # termina esta cena logo antes da palavra
                d = ta - 0.1 - t
            else:                                        # esta cena É a da palavra
                forcado = nome; pend.pop(0); d = max(d, 1.2)
        d = min(d, MAX_CENA, total - t)
        if total - (t + d) < MIN_CENA:
            d = total - t
            if d > MAX_CENA:
                d /= 2
        if forcado:
            c = pool.clips[forcado]; ini, dd = pool.trecho(c, d, t, permitir_repetir=True); motivo = "sincronia"
        else:
            evitar = {a[1] for a in pend if a[1]}               # reserva os clipes das âncoras para a hora da palavra
            c, ini, dd = pool.escolher(cats, d, anterior, t, evitar); motivo = cats[0]
        cenas.append({"inicio": t, "dur": dd, "clip": c, "in": ini, "motivo": motivo})
        t += dd; anterior = c["src"]
    return cenas


# ---------------------------------------------------------------- HTML
def html(cenas, total, cta_ini, cta_linhas, entrada, musica, flashes):
    vids = []
    for i, c in enumerate(cenas):
        vids.append(
            f'      <video id="cena{i+1:02d}" class="clip broll" src="assets/broll/{c["clip"]["src"].name}" muted playsinline '
            f'data-start="{c["inicio"]:.3f}" data-duration="{c["dur"]:.3f}" data-media-start="{c["in"]:.2f}" '
            f'data-track-index="{i % 2}"></video>')
    for j, ft in enumerate(flashes):
        vids.append(f'      <div id="flash{j+1}" class="clip flash" data-start="{ft:.3f}" data-duration="0.24" '
                    f'data-track-index="4"></div>')
    linhas = "\n".join(f'          <span class="linha"><span class="txt">{l}</span></span>' for l in cta_linhas)
    mus = ""
    if musica:
        mus = (f'    <audio id="musica" src="assets/musica.wav" data-start="{musica["inicio"]:.3f}" '
               f'data-duration="{total - musica["inicio"]:.3f}" data-track-index="11" data-volume="1"></audio>')
    if entrada == "digitar":   # salsas: texto e faixa verde surgem juntos "digitando" + ícone em fade
        passos, t0, partes = 0.018, cta_ini, []
        for k, l in enumerate(cta_linhas):
            n = max(len(l), 1)
            partes.append(f'      tl.fromTo(".linha:nth-child({k+1})", {{ clipPath: "inset(-20px 100% -20px 0)" }}, '
                          f'{{ clipPath: "inset(-20px 0% -20px 0)", duration: {n*passos:.2f}, ease: "steps({n})" }}, {t0:.3f});')
            t0 += n * passos
        partes.append(f'      tl.fromTo("#cta-icone", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {cta_ini:.3f});')
        anim = "\n".join(partes)
    else:                      # gelato: grupo texto+ícone cresce do centro em 10 frames
        anim = f'      tl.fromTo("#cta-grupo", {{ scale: 0 }}, {{ scale: 1, duration: 0.33, ease: "power2.out" }}, {cta_ini:.3f});'
    flash_anim = "\n".join(
        f'      tl.fromTo("#flash{j+1}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.07 }}, {ft:.3f})'
        f'.to("#flash{j+1}", {{ opacity: 0, duration: 0.14 }}, {ft + 0.1:.3f});' for j, ft in enumerate(flashes))
    return f"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Montserrat"; font-weight: 600; src: url("assets/fonts/montserrat-latin-600-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Montserrat"; font-weight: 700; src: url("assets/fonts/montserrat-latin-700-normal.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .broll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 8; }}
      /* CTA: branco com contorno preto sobre faixa verde de bordas "pinceladas" + sticker do WhatsApp */
      #cta {{ position: absolute; inset: 0; z-index: 10; }}
      #cta-grupo {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
      #cta-texto {{ position: absolute; top: 640px; left: 0; width: 100%; display: flex; flex-direction: column;
                    align-items: center; gap: 4px; font-family: "Montserrat", sans-serif; font-weight: 600;
                    font-size: 108px; line-height: 1.12; letter-spacing: -0.5px; }}
      .linha {{ position: relative; display: inline-block; padding: 0 20px; white-space: nowrap; }}
      .linha::before {{ content: ""; position: absolute; inset: 10px 0 4px 0; background: #009b01; filter: url(#pincel); }}
      .txt {{ position: relative; color: #fff; -webkit-text-stroke: 9px #000; paint-order: stroke fill; }}
      #cta-icone {{ position: absolute; left: 340px; top: 1040px; width: 400px; height: 400px; }}
    </style>
  </head>
  <body>
    <svg width="0" height="0" style="position:absolute">
      <filter id="pincel" x="-5%" y="-20%" width="110%" height="140%">
        <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="7" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G" />
      </filter>
    </svg>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
{chr(10).join(vids)}
      <div id="cta" class="clip" data-start="{cta_ini:.3f}" data-duration="{total - cta_ini:.3f}" data-track-index="5">
        <div id="cta-grupo">
          <div id="cta-texto">
{linhas}
          </div>
          <img id="cta-icone" src="assets/whatsapp_badge.svg" alt="" />
        </div>
      </div>
    </div>
    <audio id="voz" src="assets/voz.wav" data-start="{VOZ_INICIO:.3f}" data-track-index="10" data-volume="1"></audio>
{mus}
    <script>
      const tl = gsap.timeline({{ paused: true }});
{anim}
{flash_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    spec_path = Path(args[0]).resolve()
    spec = json.loads(spec_path.read_text())
    base = spec_path.parent
    seed = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--seed=")), spec.get("seed", 1)))
    rng = random.Random(seed)
    idioma = spec.get("idioma", "pt")
    if not spec.get("voz"):
        sys.exit("Spec sem 'voz'. A voz é sempre enviada pelo usuário (MiniMax/ElevenLabs) — peça o arquivo.")
    if not spec.get("musica"):
        print("ATENÇÃO: spec sem 'musica'. O método sempre tem música — peça o arquivo ao usuário.")

    out = (base / spec.get("saida", spec.get("nome", "criativo"))).resolve()
    (out / "assets" / "broll").mkdir(parents=True, exist_ok=True)
    (out / "assets" / "fonts").mkdir(exist_ok=True)
    for f in ["gsap.min.js", "whatsapp_badge.svg"]:
        shutil.copy(ASSETS / f, out / "assets" / f)
    for f in (ASSETS / "fonts").glob("*.woff2"):
        shutil.copy(f, out / "assets" / "fonts" / f.name)

    # ---- voz + transcrição
    voz = out / "assets" / "voz.wav"
    preparar_voz((base / spec["voz"]).resolve(), voz, spec.get("apertar_pausas", False))
    voz_fim = VOZ_INICIO + duracao(voz) - 0.25          # o apad não conta como fala
    linhas = []
    if tr.disponivel():
        linhas = [(a + VOZ_INICIO, b + VOZ_INICIO, t) for a, b, t in tr.transcrever(voz, idioma)]
        (out / "transcricao.tsv").write_text("".join(f"{a:.2f}\t{b:.2f}\t{t}\n" for a, b, t in linhas))
        if linhas:
            voz_fim = linhas[-1][1]
    else:
        print("AVISO: transcritor não instalado (rode scripts/setup.sh). CTA e sincronia só com tempos manuais.")

    # ---- CTA: ancorado na frase falada "clique no botão…"
    cta_ini = spec.get("cta_tempo")
    if cta_ini is None and linhas:
        achados = [x for x in (tr.tempo_da_frase(linhas, f, voz_fim - 25) for f in FRASES_CTA) if x is not None]
        if achados:
            cta_ini = min(achados) - CTA_ANTES_DA_FALA
    if cta_ini is None:
        cta_ini = voz_fim - 5.0
        print("AVISO: não achei a frase do CTA na voz; CTA posto 5 s antes do fim da voz. Confira.")
    cta_ini = round(max(cta_ini, 6.0), 3)
    total = round(voz_fim + float(spec.get("cauda", CAUDA)), 3)

    # ---- música: do início da timeline, a partir do ponto escolhido da faixa
    musica = None
    if spec.get("musica"):
        musica = {"inicio": float(spec.get("musica_inicio", 0.0))}
        preparar_musica((base / spec["musica"]).resolve(), out / "assets" / "musica.wav",
                        float(spec.get("musica_offset", 22.0)), total - musica["inicio"])

    # ---- b-roll
    arquivos = []
    for d in spec.get("broll_dirs", [spec.get("broll_dir", "broll")]):
        p = (base / d).resolve()
        arquivos += sorted(f for f in p.iterdir() if f.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v") and tem_video(f))
    copias = []
    for f in arquivos:
        dst = out / "assets" / "broll" / seguro(f.name)
        if not dst.exists():
            shutil.copy(f, dst)
        copias.append(dst)
    pool = Pool(copias, rng)

    gancho = [seguro(g) for g in spec.get("gancho", [])] or [n for n, c in pool.clips.items() if c["cat"] == "gancho"]
    if not gancho:
        print("ATENÇÃO: nenhum clipe de gancho (spec 'gancho' ou arquivo 'gancho_*'). O hook visual TEM que mostrar "
              "o que a primeira frase fala — usando 'final_*' como substituto.")
        gancho = [n for n, c in pool.clips.items() if c["cat"] == "final"][:2]

    ancoras = []
    for a in spec.get("sincronia", []):
        nome = seguro(a["broll"])
        if nome not in pool.clips:
            sys.exit(f"Âncora aponta para b-roll inexistente: {a['broll']}")
        ta = a.get("tempo")
        if ta is None and linhas:
            ta = tr.tempo_da_frase(linhas, a["fala"])
        if ta is None:
            print(f"AVISO: não achei \"{a.get('fala')}\" na fala; âncora ignorada."); continue
        ancoras.append((float(ta), nome))
    flashes = [round(x - 0.3, 2) for x in (tr.tempo_da_frase(linhas, f) for f in spec.get("flash_em", [])) if x is not None]
    ancoras += [(f + 0.07, None) for f in flashes]       # corte escondido no pico do flash
    ancoras.sort(key=lambda a: a[0])

    if spec.get("clips"):   # EDL manual tem prioridade total
        cenas, t = [], 0.0
        for c in spec["clips"]:
            clip = pool.clips[seguro(c["src"])]
            d = min(float(c["dur"]), MAX_CENA)
            cenas.append({"inicio": t, "dur": d, "clip": clip, "in": float(c.get("in", 0)), "motivo": "manual"})
            t += d
        total = round(t, 3)
    else:
        cenas = planejar(total, cta_ini, pool, ancoras, gancho, rng)
    t = 0.0
    for c in cenas:   # recompacta (algum b-roll pode ter sido mais curto que o pedido)
        c["inicio"] = round(t, 3); c["dur"] = round(c["dur"], 3); t += c["dur"]
    total = round(t, 3)

    (out / "index.html").write_text(html(cenas, total, cta_ini, spec.get("cta_linhas", CTA_PADRAO.get(idioma, CTA_PADRAO["pt"])),
                                         spec.get("cta_entrada", "pop"), musica, flashes))
    (out / "hyperframes.json").write_text(json.dumps({"skill": "general-video"}, indent=2))
    edl = [{"inicio": c["inicio"], "dur": c["dur"], "src": c["clip"]["src"].name, "in": c["in"], "motivo": c["motivo"]}
           for c in cenas]
    (out / "edl.json").write_text(json.dumps({"total": total, "voz_fim": voz_fim, "cta_inicio": cta_ini,
                                              "ancoras": ancoras, "cenas": edl}, indent=2, ensure_ascii=False))

    # ---- relatório de conformidade
    durs = [c["dur"] for c in cenas]
    seguidos = sum(1 for a, b in zip(cenas, cenas[1:]) if a["clip"]["src"] == b["clip"]["src"] and a["motivo"] != "gancho")
    usos = {}
    for c in cenas:
        usos[c["clip"]["src"].name] = usos.get(c["clip"]["src"].name, 0) + 1
    print(f"Projeto: {out}")
    print(f"Total {total:.2f}s | voz {VOZ_INICIO:.2f}→{voz_fim:.2f}s | cauda só música {total - voz_fim:.2f}s | "
          f"CTA visual {cta_ini:.2f}s | música {'desde ' + str(musica['inicio']) + 's (offset ' + str(spec.get('musica_offset', 22.0)) + 's)' if musica else '—'}")
    print(f"{len(cenas)} cenas | média {sum(durs)/len(durs):.2f}s | máx {max(durs):.2f}s | mesmo b-roll em sequência "
          f"(fora do gancho): {seguidos} | b-rolls reaproveitados {sum(v > 1 for v in usos.values())}/{len(usos)} | "
          f"âncoras de sincronia {sum(c['motivo'] == 'sincronia' for c in cenas)}/{sum(1 for a in ancoras if a[1])}")
    banco = sum(c["dur"] for c in pool.clips.values())
    print(f"Banco de b-roll: {banco:.0f}s de material para {total:.0f}s de vídeo | trechos repetidos: {pool.repetidos}")
    if pool.repetidos or banco < 1.3 * total:
        print(f"ATENÇÃO: b-roll insuficiente — o método não repete trecho. Peça/busque mais b-roll "
              f"(mínimo ~{1.3 * total:.0f}s no total, ideal 15–25 clipes de 5–20 s com variações diferentes).")
    if linhas:
        print("Gancho falado:", linhas[0][2][:110])

    if "--render" in sys.argv:
        subprocess.run(["npx", "-y", "hyperframes@latest", "lint"], cwd=out)
        subprocess.run(["npx", "-y", "hyperframes@latest", "render", "-o", f"{out.name}.mp4"], cwd=out, check=True)


if __name__ == "__main__":
    main()
