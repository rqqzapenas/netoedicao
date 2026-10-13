#!/usr/bin/env bash
# Prepara o ambiente de render do HyperFrames numa sessão nova (container efêmero).
set -euo pipefail
npx -y hyperframes@latest browser ensure   # baixa o Chrome headless usado no render
command -v ffmpeg >/dev/null || echo "AVISO: ffmpeg não encontrado"
