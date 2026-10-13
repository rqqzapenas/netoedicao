#!/usr/bin/env bash
# Disseca um criativo de referência: cortes/duração de cenas, folhas de contato com timestamp,
# espectrograma, níveis de voz x música, início da música, fim da voz e o quadro do CTA.
# Uso: analisar_referencia.sh video.mp4 [pasta_saida]
set -euo pipefail
V="$(realpath "$1")"; OUT="${2:-analise_$(basename "${1%.*}")}"
mkdir -p "$OUT/folhas"; cd "$OUT"
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

echo "== formato"; ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact=p=0 "$V"

echo "== cortes (scene > 0.22)"
ffmpeg -hide_banner -i "$V" -filter:v "select='gt(scene,0.22)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > cortes.txt
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
python3 - "$DUR" <<'EOF'
import sys, statistics
c=[0.0]+[float(x) for x in open('cortes.txt')]+[float(sys.argv[1])]
d=[c[i+1]-c[i] for i in range(len(c)-1)]
with open('cenas.tsv','w') as f:
    for i,x in enumerate(d): f.write(f"{i+1}\t{c[i]:.2f}\t{c[i+1]:.2f}\t{x:.2f}\n")
print(f"{len(d)} cenas | média {statistics.mean(d):.2f}s | mediana {statistics.median(d):.2f}s | máx {max(d):.2f}s")
print("cenas > 2 s:", [(round(c[i],2), round(x,2)) for i,x in enumerate(d) if x>2.0])
print("primeiros 5 s:", [round(x,2) for i,x in enumerate(d) if c[i] < 5])
EOF

echo "== folhas de contato (2 fps, 8x3 por folha) em folhas/"
ffmpeg -hide_banner -loglevel error -y -i "$V" -vf "fps=2,scale=270:480,drawtext=fontfile=$FONT:text='%{pts\:hms}':x=5:y=5:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=8x3" folhas/f_%02d.png

echo "== espectrograma (voz = harmônicos 500–3000 Hz; música = camada contínua)"
ffmpeg -hide_banner -loglevel error -y -i "$V" -lavfi "showspectrumpic=s=1800x600:legend=1:fscale=log:color=intensity:stop=8000" espectro.png
ffmpeg -hide_banner -loglevel error -y -i "$V" -ac 1 -ar 16000 audio.wav

echo "== loudness por trecho"
lufs(){ ffmpeg -hide_banner -nostats -ss "$1" -to "$2" -i "$V" -af ebur128=framelog=quiet -f null - 2>&1 | sed -n '/Summary/,$p' | grep ' I:' | tr -s ' '; }
echo "0–21.5 s (antes da música):$(lufs 0 21.5)"
echo "últimos 8 s (deve ser só música):$(lufs "$(python3 -c "print(max($DUR-8,0))")" "$DUR")"

python3 - <<'EOF' 2>/dev/null || echo "(instale numpy/librosa para a análise fina de voz: pip install librosa)"
import numpy as np, librosa
y,sr=librosa.load('audio.wav',sr=16000)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=160)); f=librosa.fft_frequencies(sr=sr,n_fft=2048); t=np.arange(S.shape[1])*0.01
voz=np.convolve(20*np.log10(S[(f>500)&(f<3000)].sum(0)+1e-9),np.ones(5)/5,'same')
mus=20*np.log10(S[(f>330)&(f<480)].sum(0)+1e-9)
base=np.median(voz[t>t[-1]-6])                       # nível da banda de voz na cauda (só música)
lento=np.convolve(voz,np.ones(50)/50,'same')           # média de 0,5 s: ignora picos isolados da música
ativo=np.where(lento>base+6)[0]
ini=np.where(voz>base+8)[0]
print(f"voz começa ~{t[ini[0]]:.2f}s | voz termina ~{t[ativo[-1]]:.2f}s | cauda só música ~{t[-1]-t[ativo[-1]]:.1f}s (confira no espectrograma)")
# salto de energia da camada musical entre 15 e 30 s
seg=[(a, mus[(t>=a)&(t<a+0.1)].mean()) for a in np.arange(15,30,0.1)]
salto=max(range(5,len(seg)), key=lambda i: seg[i][1]-np.mean([s[1] for s in seg[i-5:i]]))
print(f"provável entrada da música ~{seg[salto][0]:.1f}s")
tempo,_=librosa.beat.beat_track(y=y[-sr*8:],sr=sr); print(f"BPM da música (cauda) ~{float(np.atleast_1d(tempo)[0]):.0f}")
EOF
echo "Pronto: $(pwd)  (veja folhas/*.png, espectro.png, cenas.tsv)"
