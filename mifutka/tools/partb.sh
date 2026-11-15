#!/usr/bin/env bash
# Builds the real-footage part: each round video in a big circle over its own blurred copy, plus overlays, then an end card.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p seg
# trimmed to the best moments of each round video
FROM=(0.5 2.0 3.0 0.0)
D=(6.0 7.0 7.0 7.0)
END=4.0
TB=$(python3 -c "print(${D[0]}+${D[1]}+${D[2]}+${D[3]}+$END)")
O=0
for i in 1 2 3 4; do
  d=${D[$((i-1))]}; fr=${FROM[$((i-1))]}
  ffmpeg -v error -y -ss $fr -t $d -i ../clips/c$i.mp4 -i ov/mask.png -i ov/c$i.png -i ov/dot.png -filter_complex "
    [0:v]fps=30,setsar=1,split[a][b];
    [a]scale=1920:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.2:saturation=1.25[bg];
    [b]scale=940:940:flags=lanczos,format=rgba[fg];[1:v]format=gray,scale=940:940[mk];[fg][mk]alphamerge[fgc];
    [bg][fgc]overlay=70:430[v1];[v1][2:v]overlay=0:0[v2];
    [v2][3:v]overlay=x='276+(t+$O)/$TB*624-13':y=272:eval=frame,fade=t=in:st=0:d=0.3:color=white,format=yuv420p[v];
    [0:a]aresample=44100,aformat=channel_layouts=mono[a0]" \
    -map "[v]" -map "[a0]" -c:v libx264 -preset medium -crf 20 -r 30 -c:a aac -b:a 160k -ar 44100 -ac 1 seg/c$i.mp4
  O=$(python3 -c "print($O+$d)")
done
# end card over a blurred last frame, with the track fading out
ffmpeg -v error -y -sseof -0.2 -i ../clips/c4.mp4 -frames:v 1 seg/last.png
ffmpeg -v error -y -loop 1 -t $END -i seg/last.png -i ov/end.png -ss 10 -t $END -i ../clips/c3.mp4 -filter_complex "
  [0:v]fps=30,scale=1920:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.3:saturation=1.3[bg];[bg][1:v]overlay=0:0,fade=t=in:st=0:d=0.3:color=white,format=yuv420p[v];
  [2:a]aresample=44100,aformat=channel_layouts=mono,afade=t=out:st=$(python3 -c "print($END-1.6)"):d=1.6[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -r 30 -c:a aac -b:a 160k -ar 44100 -ac 1 -shortest seg/end.mp4
echo "part B: $TB s"
