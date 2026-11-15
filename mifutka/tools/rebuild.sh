#!/usr/bin/env bash
# Full build: cartoon part (recorded in the browser + mixed audio) followed by the real round-video part.
set -euo pipefail
cd "$(dirname "$0")"
python3 words.py >/dev/null
python3 build.py && node tl.js
LEN=$(python3 -c "import json;print(json.load(open('timeline.json'))['total']/1000+0.6)")
python3 music.py "$LEN" music.wav && ffmpeg -v error -y -i music.wav -b:a 64k music.mp3
python3 build.py && node tl.js
rm -rf vid4 fr5 && mkdir -p vid4 fr5
node srec.js
V=$(ls vid4/*.webm)
ffmpeg -v error -ss 1 -t 3 -i "$V" -vf fps=20,scale=36:64 fr5/%03d.png
START=$(python3 - <<'PY'
from PIL import Image, ImageStat
import glob
prev=None
for f in sorted(glob.glob('fr5/*.png')):
    m=ImageStat.Stat(Image.open(f).convert('L')).mean[0]
    if prev is not None and abs(m-prev)>8:
        print(1+(int(f[-7:-4])-1)/20); break
    prev=m
PY
)
python3 mix2.py
DUR=$(python3 -c "import json;print(json.load(open('timeline.json'))['total']/1000)")
ffmpeg -v error -y -ss "$START" -t "$DUR" -i "$V" -i mix_story.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 160k -ar 44100 -ac 1 -af "loudnorm=I=-14:TP=-1.5" -shortest -movflags +faststart seg/partA.mp4
./partb.sh
for f in c1 c2 c3 c4 end; do ffmpeg -v error -y -i seg/$f.mp4 -af "loudnorm=I=-14:TP=-1.5,volume=2dB,alimiter=limit=0.95" -c:v copy -c:a aac -b:a 160k -ar 44100 -ac 1 seg/n_$f.mp4; done
printf "file 'partA.mp4'\nfile 'n_c1.mp4'\nfile 'n_c2.mp4'\nfile 'n_c3.mp4'\nfile 'n_c4.mp4'\nfile 'n_end.mp4'\n" > seg/list.txt
ffmpeg -v error -y -f concat -safe 0 -i seg/list.txt -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -ar 44100 -movflags +faststart ../mifutka-9x16.mp4
echo "start=$START partA=$DUR"
