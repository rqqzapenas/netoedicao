#!/usr/bin/env python3
"""Monta um criativo b-roll no método (voz IA + b-roll cortado ≤2s + música a partir de 22s +
cauda só de música com CTA) como projeto HyperFrames pronto para `npx hyperframes render`.

Uso:
  python3 montar_criativo.py spec.json [--render] [--seed N]

Veja ../SKILL.md (seção "Spec do criativo") para o formato do spec.json.
Depende só de python3 (stdlib), ffmpeg e ffprobe.
"""
import json, os, random, re, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"

# ---------------------------------------------------------------- regras do método (fonte: SKILL.md)
W, H, FPS = 1080, 1920, 30
MAX_CENA = 2.0          # nenhuma cena passa de 2 s
MIN_CENA = 0.2          # micro-corte (flash) mais curto permitido
VOZ_INICIO = 0.2        # a voz entra praticamente no frame 1
MUSICA_INICIO = 22.0    # música entra no segundo 22, corte seco
CAUDA = 11.0            # intervalo final só música + texto + b-roll
CTA_ANTECEDENCIA = 4.0  # CTA visual aparece ~4 s antes da voz acabar (quando a voz fala o CTA)
LUFS_VOZ, LUFS_MUSICA = -16.0, -27.0   # música ~11 LU abaixo da voz, nível constante, sem ducking

# Ritmo extraído do criativo de referência (gelato, 82,5 s, 54 cenas).
# (duração, categorias preferidas em ordem). Categorias: final, processo, textura, reacao, geral.
GANCHO = [  # 0 → ~5,5 s: só produto final / "money shot", cortes rápidos com um flash
    (1.43, ["final", "textura"]), (1.13, ["final"]), (0.83, ["final", "textura"]),
    (0.67, ["final", "textura"]), (0.27, ["final", "textura"]), (1.13, ["final"]),
]
CORPO = [  # ciclo do meio: processo calmo (1,6–2,0) intercalado com rajadas (0,6–0,9) e reação ~a cada 20 s
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
CAUDA_RITMO = [(2.0, ["textura", "final"]), (1.63, ["final"]), (2.0, ["textura"]), (1.77, ["final"]),
               (2.0, ["final", "textura"])]
CATEGORIAS = ["final", "processo", "textura", "reacao"]


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duracao(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(out.stdout.strip())


def tem_video(path):
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=codec_type",
              "-of", "csv=p=0", str(path)])
    return "video" in out.stdout


def categoria(nome):
    base = Path(nome).stem.lower()
    for c in CATEGORIAS:
        if base.startswith(c):
            return c
    return "geral"


# ---------------------------------------------------------------- áudio
def preparar_voz(src, dst, apertar_pausas=True):
    """Tira o silêncio do começo, encurta pausas longas para ~0,2 s e normaliza em LUFS_VOZ."""
    filtros = ["silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02"]
    if apertar_pausas:
        filtros.append("silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-45dB:stop_silence=0.2")
    filtros.append(f"loudnorm=I={LUFS_VOZ}:TP=-1.5:LRA=11")
    sh(["ffmpeg", "-y", "-i", str(src), "-af", ",".join(filtros), "-ar", "48000", "-ac", "2", str(dst)])


def preparar_musica(src, dst, offset, dur):
    """Trecho da música a partir de `offset`, com loop se for curta, nível constante em LUFS_MUSICA.
    Entrada e saída secas (só 15 ms anti-clique)."""
    sh(["ffmpeg", "-y", "-stream_loop", "-1", "-ss", f"{offset}", "-i", str(src), "-t", f"{dur:.3f}",
        "-af", f"loudnorm=I={LUFS_MUSICA}:TP=-2:LRA=11,afade=t=in:d=0.015,afade=t=out:st={max(dur-0.015,0):.3f}:d=0.015",
        "-ar", "48000", "-ac", "2", str(dst)])


# ---------------------------------------------------------------- plano de cortes
def ritmo(total, cta_ini):
    """Lista de (inicio, dur, categorias) cobrindo 0→total, sem cena > MAX_CENA."""
    cenas, t = [], 0.0
    fila_gancho, i_corpo, i_cauda = list(GANCHO), 0, 0
    while t < total - 1e-6:
        if fila_gancho:
            d, cats = fila_gancho.pop(0)
        elif t >= cta_ini:
            d, cats = CAUDA_RITMO[i_cauda % len(CAUDA_RITMO)]; i_cauda += 1
        else:
            d, cats = CORPO[i_corpo % len(CORPO)]; i_corpo += 1   # o CTA entra no meio de uma cena, não num corte
        d = min(d, MAX_CENA, total - t)
        if total - (t + d) < MIN_CENA:                  # não deixa sobrar um farelo no final
            d = total - t
            if d > MAX_CENA:                             # divide em duas
                d = d / 2
        cenas.append((round(t, 3), round(d, 3), cats))
        t += d
    return cenas


class Pool:
    def __init__(self, arquivos, rng):
        self.rng = rng
        self.clips = []
        for f in arquivos:
            D = duracao(f)
            if D < MIN_CENA + 0.1:
                continue
            self.clips.append({"src": f, "dur": D, "cat": categoria(f.name), "usos": []})
        if not self.clips:
            sys.exit("Nenhum b-roll utilizável encontrado.")

    def escolher(self, cats, dur, anterior):
        def score(c):
            cat_rank = cats.index(c["cat"]) if c["cat"] in cats else (len(cats) + (0 if c["cat"] == "geral" else 1))
            cabe = 0 if c["dur"] >= dur + 0.05 else 1
            return (cabe, c["src"] == anterior, cat_rank, len(c["usos"]), self.rng.random())
        c = min(self.clips, key=score)
        d = min(dur, c["dur"] - 0.05)
        # escolhe o trecho mais distante dos trechos já usados desse b-roll ("partes diferentes do mesmo b-roll")
        max_ini = max(c["dur"] - d - 0.05, 0)
        candidatos = [round(x * 0.1, 2) for x in range(int(max_ini * 10) + 1)] or [0.0]
        if c["usos"]:
            ini = max(candidatos, key=lambda s: (min(abs(s - u) for u in c["usos"]), -s))
        else:
            ini = candidatos[0] if c["cat"] in ("final", "textura") and len(candidatos) < 30 else \
                self.rng.choice(candidatos[: max(1, len(candidatos) // 2)])
        c["usos"].append(ini)
        return c, ini, d


# ---------------------------------------------------------------- HTML
def html(cenas, total, cta_ini, cta_linhas, musica_ok):
    vids = []
    for i, c in enumerate(cenas):
        vids.append(
            f'      <video id="cena{i+1:02d}" class="clip broll" src="{c["src"]}" muted playsinline '
            f'data-start="{c["inicio"]:.3f}" data-duration="{c["dur"]:.3f}" data-media-start="{c["in"]:.2f}" '
            f'data-track-index="{i % 2}"></video>')
    linhas = "\n".join(f'          <span class="linha"><span class="txt">{l}</span></span>' for l in cta_linhas)
    musica = (f'    <audio id="musica" src="assets/musica.wav" data-start="{MUSICA_INICIO:.3f}" '
              f'data-duration="{total - MUSICA_INICIO:.3f}" data-track-index="11" data-volume="1"></audio>'
              if musica_ok else "")
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
      /* CTA: texto branco com contorno preto sobre faixa verde de bordas "pinceladas" + sticker do WhatsApp */
      #cta {{ position: absolute; inset: 0; z-index: 10; }}
      #cta-grupo {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; transform-origin: 50% 47%; }}
      #cta-texto {{ position: absolute; top: 578px; left: 0; width: 100%; display: flex; flex-direction: column;
                    align-items: center; gap: 6px; font-family: "Montserrat", sans-serif; font-weight: 600;
                    font-size: 122px; line-height: 1.12; letter-spacing: -0.5px; }}
      .linha {{ position: relative; display: inline-block; padding: 0 22px; }}
      .linha::before {{ content: ""; position: absolute; inset: 10px 0 4px 0; background: #009407; filter: url(#pincel); }}
      .txt {{ position: relative; color: #fff; -webkit-text-stroke: 9px #000; paint-order: stroke fill; }}
      #cta-icone {{ position: absolute; left: 50%; top: 1050px; width: 380px; height: 380px; margin-left: -190px; }}
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
{musica}
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // CTA "pop": cresce do centro do grupo de 0 → 100% em ~0,33 s (10 frames), sem overshoot
      tl.fromTo("#cta-grupo", {{ scale: 0 }}, {{ scale: 1, duration: 0.33, ease: "power2.out" }}, {cta_ini:.3f});
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

    # voz/música padrão do produto (produtos.json na raiz do repo ou na skill)
    produtos = {}
    for p in [base / "produtos.json", Path.cwd() / "produtos.json", SKILL / "produtos.json"]:
        if p.exists():
            produtos = json.loads(p.read_text()); break
    padrao = produtos.get(spec.get("produto", ""), {})
    voz_src = spec.get("voz") or padrao.get("voz")
    mus_src = spec.get("musica") or padrao.get("musica")
    mus_off = float(spec.get("musica_offset", padrao.get("musica_offset", 0)))
    if not voz_src:
        sys.exit("Spec sem 'voz' (e produto sem voz padrão em produtos.json).")

    out = (base / spec.get("saida", spec.get("nome", "criativo"))).resolve()
    (out / "assets" / "broll").mkdir(parents=True, exist_ok=True)
    (out / "assets" / "fonts").mkdir(exist_ok=True)
    for f in ["gsap.min.js", "whatsapp_badge.svg"]:
        shutil.copy(ASSETS / f, out / "assets" / f)
    for f in (ASSETS / "fonts").glob("*.woff2"):
        shutil.copy(f, out / "assets" / "fonts" / f.name)

    # ---- áudio
    preparar_voz((base / voz_src).resolve(), out / "assets" / "voz.wav", spec.get("apertar_pausas", True))
    voz_dur = duracao(out / "assets" / "voz.wav")
    voz_fim = VOZ_INICIO + voz_dur
    cauda = float(spec.get("cauda", CAUDA))
    total = round(voz_fim + cauda, 3)
    cta_ini = round(max(voz_fim - float(spec.get("cta_antecedencia", CTA_ANTECEDENCIA)), 6.0), 3)
    musica_ok = bool(mus_src) and total > MUSICA_INICIO
    if musica_ok:
        preparar_musica((base / mus_src).resolve(), out / "assets" / "musica.wav", mus_off, total - MUSICA_INICIO)

    # ---- b-roll
    arquivos = []
    for d in spec.get("broll_dirs", [spec.get("broll_dir", "broll")]):
        p = (base / d).resolve()
        arquivos += sorted(f for f in p.iterdir() if f.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v")
                           and tem_video(f))
    copiados = {}
    for f in arquivos:
        dst = out / "assets" / "broll" / re.sub(r"[^\w.\-]", "_", f.name)
        if not dst.exists():
            shutil.copy(f, dst)
        copiados[f] = dst
    pool = Pool(list(copiados.values()), rng)

    if spec.get("clips"):   # EDL manual tem prioridade
        cenas, t = [], 0.0
        for c in spec["clips"]:
            d = min(float(c["dur"]), MAX_CENA)
            cenas.append({"inicio": round(t, 3), "dur": d, "src": f"assets/broll/{Path(c['src']).name}",
                          "in": float(c.get("in", 0)), "cat": categoria(c["src"])})
            t += d
        total = round(t, 3)
    else:
        cenas, anterior = [], None
        for ini, d, cats in ritmo(total, cta_ini):
            c, cin, dd = pool.escolher(cats, d, anterior)
            cenas.append({"inicio": ini, "dur": round(dd, 3), "src": f"assets/broll/{c['src'].name}",
                          "in": cin, "cat": c["cat"], "pedido": cats[0]})
            anterior = c["src"]
        # se algum b-roll era curto demais, recompacta os inícios
        t = 0.0
        for c in cenas:
            c["inicio"] = round(t, 3); t += c["dur"]
        total = round(t, 3)

    linhas = spec.get("cta_linhas", ["Clique no", "botão abaixo"])
    (out / "index.html").write_text(html(cenas, total, cta_ini, linhas, musica_ok))
    (out / "hyperframes.json").write_text(json.dumps({"skill": "general-video"}, indent=2))
    (out / "edl.json").write_text(json.dumps({"total": total, "voz_fim": voz_fim, "cta_inicio": cta_ini,
                                              "musica_inicio": MUSICA_INICIO if musica_ok else None,
                                              "cenas": cenas}, indent=2, ensure_ascii=False))

    # ---- relatório de conformidade com o método
    durs = [c["dur"] for c in cenas]
    seguidos = sum(1 for a, b in zip(cenas, cenas[1:]) if a["src"] == b["src"])
    reuso = {}
    for c in cenas:
        reuso[c["src"]] = reuso.get(c["src"], 0) + 1
    print(f"Projeto: {out}")
    print(f"Duração total {total:.2f}s | voz 0,20→{voz_fim:.2f}s | música {MUSICA_INICIO if musica_ok else '—'}→fim | "
          f"cauda só música {total - voz_fim:.2f}s | CTA a partir de {cta_ini:.2f}s")
    print(f"{len(cenas)} cenas | média {sum(durs)/len(durs):.2f}s | máx {max(durs):.2f}s | mín {min(durs):.2f}s | "
          f"mesmo b-roll em sequência: {seguidos} | b-rolls reaproveitados: {sum(1 for v in reuso.values() if v > 1)}/{len(reuso)}")
    if max(durs) > MAX_CENA + 1e-6:
        print("ATENÇÃO: cena acima de 2 s")
    if not musica_ok:
        print("ATENÇÃO: sem música (spec/produto sem 'musica' ou criativo com menos de 22 s)")

    if "--render" in sys.argv:
        subprocess.run(["npx", "-y", "hyperframes@latest", "lint"], cwd=out)
        subprocess.run(["npx", "-y", "hyperframes@latest", "render", "-o", f"{out.name}.mp4"], cwd=out, check=True)


if __name__ == "__main__":
    main()
