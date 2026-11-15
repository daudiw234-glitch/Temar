#!/usr/bin/env bash
# Lays the narrator's closing lines over the chaos montage and the end card (track ducked underneath).
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i seg/n_chaos.mp4 -i voice/e1.mp3 -i ov/sub_chaos.png -filter_complex "
  [0:v][2:v]overlay=0:1250:enable='between(t,0.9,3.8)'[v];
  [0:a]volume='if(between(t,0.8,3.9),0.45,1)':eval=frame[bgm];[1:a]adelay=900,volume=1.6[vo];[bgm][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 21 -r 30 -c:a aac -b:a 160k -ar 44100 -ac 1 seg/v_chaos.mp4
ffmpeg -v error -y -i seg/n_end.mp4 -i voice/e2.mp3 -filter_complex "
  [0:a]volume=0.45[bgm];[1:a]adelay=300,volume=1.6[vo];[bgm][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -ar 44100 -ac 1 seg/v_end.mp4
