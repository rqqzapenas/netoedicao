#!/usr/bin/env bash
# Prepara uma sessão nova (container efêmero): render do HyperFrames + ferramentas de análise de áudio.
#   bash scripts/setup.sh          → render + transcritor (≈ 1,2 GB, ~2 min)
#   bash scripts/setup.sh --tudo   → + separador voz/música (spleeter, ≈ 1,5 GB a mais)
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
npx -y hyperframes@latest browser ensure                     # Chrome headless do render
command -v ffmpeg >/dev/null || echo "AVISO: ffmpeg não encontrado"

# Transcrição local (Whisper small via sherpa-onnx). Modelos vêm do GitHub (HuggingFace é bloqueado aqui).
pip install -q --break-system-packages numpy scipy librosa soundfile sherpa-onnx 2>&1 | grep -v -i warning
mkdir -p /opt/ml && cd /opt/ml
if [ ! -d sherpa-onnx-whisper-small ]; then
  curl -sSL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 | tar xj
  rm -f sherpa-onnx-whisper-small/small-encoder.onnx sherpa-onnx-whisper-small/small-decoder.onnx  # usamos o int8
fi
[ -f silero_vad.onnx ] || curl -sSL -o silero_vad.onnx https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx

# Busca/download de b-roll no TikTok (skill buscar-broll)
pip install -q --break-system-packages -U yt-dlp curl_cffi 2>&1 | grep -v -i warning
(cd "$REPO/.claude/skills/buscar-broll/scripts" && npm i --silent)

if [ "${1:-}" = "--tudo" ]; then   # separação voz/música (spleeter precisa de Python 3.11)
  [ -d sp ] || { python3.11 -m venv sp && sp/bin/pip install -q spleeter; }
  if [ ! -d pretrained_models/2stems ]; then
    mkdir -p pretrained_models/2stems
    curl -sSL https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz | tar xz -C pretrained_models/2stems
  fi
fi
echo "Setup pronto."
