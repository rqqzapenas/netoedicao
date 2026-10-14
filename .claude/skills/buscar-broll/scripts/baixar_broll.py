#!/usr/bin/env python3
"""Baixa candidatos a b-roll do TikTok (sem marca d'água, melhor qualidade) e gera uma folha de contato de
cada um para triagem visual.

Uso:
  python3 baixar_broll.py resultados.jsonl pasta/ [--max=40] [--min-plays=20000]   # saída do tiktok_busca.mjs
  python3 baixar_broll.py @perfil pasta/ [--max=30]                                # vídeos de um perfil
  python3 baixar_broll.py URL [URL ...] pasta/                                     # links soltos

Filtros (busca/perfil): vertical, 6–180 s, ordenado por plays. Gera em <pasta>/:
  videos/<id>.mp4, folhas/<id>.png (12 quadros) e candidatos.tsv (id, autor, plays, duração, legenda, url).
REGRA DO DONO: NUNCA baixar b-roll com legenda/texto na imagem. Antes do download em 1080p, cada vídeo passa
pela checagem anti-texto: uma cópia de baixa resolução vai para um diretório temporário, o OCR lê 12 quadros
do vídeo inteiro, e a cópia é apagada. Teve texto → rejeitado (rejeitados.tsv), nada fica salvo.
A triagem final (é b-roll? tem gente falando pra câmera? texto queimado? bate com a copy?) é visual: abra
as folhas e renomeie os aprovados com o prefixo de categoria antes de passar ao montador.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

YTDLP = ["yt-dlp", "--impersonate", "chrome", "--no-warnings", "--quiet"]


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def listar_perfil(handle, n):
    r = sh(YTDLP + ["--flat-playlist", "--playlist-end", str(n * 2), "-j", f"https://www.tiktok.com/{handle}"])
    itens = []
    for l in r.stdout.splitlines():
        try:
            d = json.loads(l)
        except json.JSONDecodeError:
            continue
        itens.append({"id": d.get("id"), "url": d.get("url") or d.get("webpage_url"), "autor": handle.lstrip("@"),
                      "legenda": (d.get("title") or "")[:200], "plays": d.get("view_count"),
                      "duracao": d.get("duration")})
    return itens


_OCR = None


def texto_na_tela(url, n=12):
    """(tem_texto, exemplos). Baixa a menor resolução num temp, lê n quadros com OCR e apaga tudo."""
    global _OCR
    if _OCR is None:
        from rapidocr_onnxruntime import RapidOCR
        _OCR = RapidOCR()
    tmp = Path(tempfile.mkdtemp(prefix="ocr_"))
    try:
        r = sh(YTDLP + ["-S", "+res", "-f", "b", "-o", str(tmp / "baixa.%(ext)s"), url])
        arq = next(tmp.glob("baixa.*"), None)
        if r.returncode != 0 or not arq:
            return None, ["não consegui checar"]
        dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)]).stdout or 0)
        larg = 540
        achados = {}       # texto normalizado -> nº de quadros
        grandes = []
        for i in range(n):
            t = 0.3 + (max(dur - 0.6, 0.1)) * i / max(n - 1, 1)
            png = tmp / f"q{i}.png"
            sh(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(arq), "-frames:v", "1",
                "-vf", f"scale={larg}:-2", str(png)])
            if not png.exists():
                continue
            res, _ = _OCR(str(png))
            for box, txt, conf in (res or []):
                conf = float(conf)
                if conf < 0.6 or len(txt.strip()) < 3:
                    continue
                w = max(p[0] for p in box) - min(p[0] for p in box)
                achados[txt.strip().lower()] = achados.get(txt.strip().lower(), 0) + 1
                if w >= 0.18 * larg:
                    grandes.append(txt.strip())
        repetido = [t for t, c in achados.items() if c >= 2]
        tem = bool(grandes or repetido or len(achados) >= 3)
        return tem, (grandes + repetido + list(achados))[:5]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


COMIDA = set("""receita receta recipe recipes comida food foods cozinha cocina cooking cook kitchen salgado salgados
salgadinho salgadinhos festa fiesta party appetizer appetizers aperitivo aperitivos canape canapes canapé canapés
petisco petiscos bocadito bocaditos botana botanas snack snacks lanche finger fingerfood fingerfoods mini minis
coxinha coxinhas empada empadas esfiha quiche tartelete tartaleta tapas bruschetta crostini dip queijo queso cheese
frango pollo chicken carne beef massa masa dough forno horno oven frito frita fried airfryer assado bake baked
doce dulce sweet bolo pastel pasteles pastelito torta tortilla taco tacos salsa molho sauce gelato sorvete helado
pão pan bread pizza sanduiche sandwich wrap rolinho rollitos croquete croqueta bolinha bolinhas
foodie foodtiktok comidatiktok recetasfaciles receitafacil receitas recetas easyrecipe homemade caseiro casero
mozzarella sticks bites cups platter board charcuterie hosting host make making bake baking cheesy crispy
delicious yummy tasty sabor delicia delicioso gostoso""".split())


def relevante(it, extra=()):
    """Legenda/hashtags com alguma palavra de comida (ou do termo buscado). Sem legenda → deixa passar."""
    leg = (it.get("legenda") or "").lower()
    if not leg.strip():
        return True
    palavras = set(w.strip("#.,!?:;()[]\"'") for w in leg.replace("#", " #").split())
    termos = set(w for t in [it.get("termo", "")] + list(extra) for w in t.lower().replace("#", "").split())
    return bool(palavras & (COMIDA | termos)) or any(t in leg.replace(" ", "") for t in termos if len(t) > 4)


def folha(video, png):
    dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)]).stdout or 0)
    if dur <= 0:
        return 0.0
    fps = 12 / dur
    sh(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-vf",
        f"fps={fps:.4f},scale=160:284,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='%{{pts\\:hms}}':x=3:y=3:fontsize=12:fontcolor=yellow:box=1:boxcolor=black,tile=6x2",
        "-frames:v", "1", str(png)])
    return dur


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    pasta = Path(args[-1]); fontes = args[:-1]
    mx, min_plays = int(opt.get("max", 40)), int(opt.get("min-plays", 0))
    (pasta / "videos").mkdir(parents=True, exist_ok=True); (pasta / "folhas").mkdir(exist_ok=True)

    itens = []
    for f in fontes:
        if f.endswith(".jsonl"):
            itens += [json.loads(l) for l in Path(f).read_text().splitlines() if l.strip()]
        elif f.startswith("@"):
            itens += listar_perfil(f, mx)
        else:
            itens.append({"id": f.rstrip("/").split("/")[-1].split("?")[0], "url": f})
    vistos, fila = set(), []
    for it in itens:
        if not it.get("id") or it["id"] in vistos:
            continue
        vistos.add(it["id"])
        if it.get("largura") and it.get("altura") and it["altura"] < it["largura"]:
            continue                                   # horizontal fora
        if it.get("duracao") and not (6 <= float(it["duracao"]) <= 180):
            continue
        if min_plays and (it.get("plays") or 0) < min_plays:
            continue
        if "termo" in it and not relevante(it):
            continue                                   # legenda sem nada de comida → fora
        fila.append(it)
    fila.sort(key=lambda x: -(x.get("plays") or 0))
    fila = fila[:mx]
    print(f"{len(fila)} candidatos para baixar")

    linhas, rejeitados = [], []
    for it in fila:
        dst = pasta / "videos" / f"{it['id']}.mp4"
        if not dst.exists():
            tem, ex = texto_na_tela(it["url"])
            if tem is None or tem:
                motivo = "texto na tela: " + " | ".join(ex) if tem else "checagem falhou (não baixado por segurança)"
                rejeitados.append([it["id"], it["url"], motivo.replace("\t", " ")])
                print(f"  ⛔ {it['id']} rejeitado — {motivo[:90]}"); continue
            # maior resolução (normalmente 1080x1920 em h265, que o render aceita); empate → h264
            r = sh(YTDLP + ["-S", "res,vcodec:h264", "-f", "b",
                            "--merge-output-format", "mp4", "-o", str(dst), it["url"]])
            if r.returncode != 0 or not dst.exists():
                print(f"  ✗ {it['url']} — {r.stderr.strip()[:100]}"); continue
        dur = folha(dst, pasta / "folhas" / f"{it['id']}.png")
        wh = sh(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(dst)]).stdout.strip()
        linhas.append([it["id"], it.get("autor", ""), str(it.get("plays", "")), f"{dur:.1f}", wh,
                       (it.get("legenda") or "").replace("\t", " ").replace("\n", " ")[:120], it["url"], it.get("termo", "")])
        print(f"  ✓ {it['id']} {wh} {dur:.0f}s plays={it.get('plays')}")
    with open(pasta / "candidatos.tsv", "w") as f:
        f.write("id\tautor\tplays\tduracao\tresolucao\tlegenda\turl\ttermo\n")
        f.writelines("\t".join(l) + "\n" for l in linhas)
    with open(pasta / "rejeitados.tsv", "a") as f:
        f.writelines("\t".join(l) + "\n" for l in rejeitados)
    print(f"{len(linhas)} baixados (sem texto na tela) | {len(rejeitados)} rejeitados por texto → {pasta}/candidatos.tsv, rejeitados.tsv e folhas/")


if __name__ == "__main__":
    main()
