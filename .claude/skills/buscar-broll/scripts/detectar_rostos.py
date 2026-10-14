#!/usr/bin/env python3
"""Acha os trechos com rosto em cada b-roll e devolve no formato `evitar` do spec.

Folha de contato de 12 quadros não pega rosto que aparece por 1–2 s (cortes rápidos, "provando" no meio da
receita). Este script lê 4 quadros por segundo de cada vídeo com o detector YuNet (OpenCV) e marca os
trechos com rosto, com folga de 0,3 s.

Uso: python3 detectar_rostos.py pasta_ou_mp4 [...] [--saida=rostos.json] [--fps=4] [--min=0.06]
  --min: largura mínima do rosto em fração da largura do quadro (ignora gente bem ao fundo).
Saída: {"clipe.mp4": [[ini, fim], ...]} — junte ao `evitar` do spec (ou ao evitar_banco.json do produto).
Modelo: /opt/ml/face/yunet.onnx (scripts/setup.sh baixa).
"""
import json, subprocess, sys
from pathlib import Path

import cv2
import numpy as np

MODELO = "/opt/ml/face/yunet.onnx"
LARG = 320


def trechos_com_rosto(video, fps=4.0, min_frac=0.06, folga=0.3):
    w, h = LARG, 0
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                           "-of", "csv=p=0", str(video)], capture_output=True, text=True).stdout.strip().split(",")
    W, H = int(info[0]), int(info[1])
    h = int(round(H * LARG / W / 2) * 2)
    det = cv2.FaceDetectorYN.create(MODELO, "", (w, h), 0.85)
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(video), "-vf", f"fps={fps},scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    tam, i, tempos = w * h * 3, 0, []
    while True:
        buf = p.stdout.read(tam)
        if len(buf) < tam:
            break
        img = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        _, faces = det.detect(img)
        if faces is not None and any(f[2] >= min_frac * w for f in faces):
            tempos.append(i / fps)
        i += 1
    p.wait()
    faixas = []
    for t in tempos:
        a, b = max(0.0, t - folga), t + 1 / fps + folga
        if faixas and a <= faixas[-1][1]:
            faixas[-1][1] = round(b, 2)
        else:
            faixas.append([round(a, 2), round(b, 2)])
    return faixas


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    arqs = []
    for a in args:
        pa = Path(a)
        arqs += sorted(pa.glob("*.mp4")) if pa.is_dir() else [pa]
    res = {}
    for v in arqs:
        f = trechos_com_rosto(v, float(opt.get("fps", 4)), float(opt.get("min", 0.06)))
        if f:
            res[v.name] = f
            print(f"  rosto  {v.name}: {f}")
    Path(opt.get("saida", "rostos.json")).write_text(json.dumps(res, indent=1))
    print(f"{len(res)}/{len(arqs)} clipes com rosto → {opt.get('saida', 'rostos.json')}")


if __name__ == "__main__":
    main()
