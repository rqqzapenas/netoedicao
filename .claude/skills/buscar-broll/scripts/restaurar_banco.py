#!/usr/bin/env python3
"""Reconstrói um banco de b-roll aprovado a partir do catálogo salvo no repositório.

Os vídeos não ficam no git (o ambiente é efêmero e o repositório ficaria pesado). Fica só o catálogo
(`banco.tsv`: id do TikTok, url, nome final com prefixo de categoria, trecho útil, notas) e a folha de
contato de cada clipe. Este script baixa de novo, pelo id, só o que está aprovado, já com o nome certo.

Uso: python3 restaurar_banco.py projetos/finger-foods/banco.tsv destino/broll/ [--categoria=gancho_mesa_boteco]
Os clipes do catálogo já passaram pela checagem anti-texto; se o TikTok tiver removido algum, ele é avisado.
"""
import csv, subprocess, sys
from pathlib import Path

YTDLP = ["yt-dlp", "--impersonate", "chrome", "--no-warnings", "--quiet", "-S", "res,vcodec:h264", "-f", "b"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    cat, dst = Path(args[0]), Path(args[1])
    dst.mkdir(parents=True, exist_ok=True)
    ok = falhou = 0
    for row in csv.DictReader(open(cat), delimiter="\t"):
        if row.get("status", "aprovado") != "aprovado":
            continue
        if opt.get("categoria") and not row["nome"].startswith(opt["categoria"]):
            continue
        alvo = dst / row["nome"]
        if alvo.exists():
            ok += 1; continue
        r = subprocess.run(YTDLP + ["-o", str(alvo), row["url"]], capture_output=True, text=True)
        if r.returncode == 0 and alvo.exists():
            ok += 1; print(f"  ✓ {row['nome']}")
        else:
            falhou += 1; print(f"  ✗ {row['nome']} ({row['url']}) — {r.stderr.strip()[:80]}")
    print(f"{ok} clipes em {dst} | {falhou} indisponíveis")


if __name__ == "__main__":
    main()
