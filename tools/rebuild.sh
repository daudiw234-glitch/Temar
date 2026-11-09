#!/usr/bin/env bash
# Rebuild kepchik-story.html and kepchik-story-9x16.mp4 from tools/voice/*.mp3.
set -euo pipefail
cd "$(dirname "$0")"
python3 words.py >/dev/null            # word timings for every voice clip present
python3 build.py                       # inject voices/words (no music yet) to measure timeline
node tl.js                             # writes timeline.json
LEN=$(python3 -c "import json;print(json.load(open('timeline.json'))['total']/1000+0.6)")
python3 music.py "$LEN" music.wav && ffmpeg -v error -y -i music.wav -b:a 64k music.mp3
python3 build.py && node tl.js         # final HTML with music
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
    if prev is not None and abs(m-prev)>12:
        print(1+(int(f[-7:-4])-1)/20); break
    prev=m
PY
)
python3 mix2.py
DUR=$(python3 -c "import json;print(json.load(open('timeline.json'))['total']/1000+0.2)")
ffmpeg -v error -y -ss "$START" -t "$DUR" -i "$V" -i mix_story.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 20 \
  -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -af loudnorm=I=-14:TP=-1.5 -shortest -movflags +faststart ../kepchik-story-9x16.mp4
echo "start=$START dur=$DUR"
