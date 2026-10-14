#!/usr/bin/env python3
"""Baixa candidatos a b-roll do TikTok (sem marca d'água, melhor qualidade) e gera uma folha de contato de
cada um para triagem visual.

Uso:
  python3 baixar_broll.py resultados.jsonl pasta/ [--max=40] [--min-plays=20000]   # saída do tiktok_busca.mjs
  python3 baixar_broll.py @perfil pasta/ [--max=30]                                # vídeos de um perfil
  python3 baixar_broll.py URL [URL ...] pasta/                                     # links soltos

Filtros (busca/perfil): vertical, 6–180 s, ordenado por plays. Gera em <pasta>/:
  videos/<id>.mp4, folhas/<id>.png (12 quadros) e candidatos.tsv (id, autor, plays, duração, legenda, url).
A triagem final (é b-roll? tem gente falando pra câmera? texto queimado? bate com a copy?) é visual: abra
as folhas e renomeie os aprovados com o prefixo de categoria antes de passar ao montador.
"""
import json, subprocess, sys
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
        fila.append(it)
    fila.sort(key=lambda x: -(x.get("plays") or 0))
    fila = fila[:mx]
    print(f"{len(fila)} candidatos para baixar")

    linhas = []
    for it in fila:
        dst = pasta / "videos" / f"{it['id']}.mp4"
        if not dst.exists():
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
    print(f"{len(linhas)} baixados → {pasta}/candidatos.tsv e {pasta}/folhas/")


if __name__ == "__main__":
    main()
