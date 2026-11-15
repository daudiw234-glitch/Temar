# Builds seg/chaos.mp4: a ~10 s frenzy of the round videos popping up everywhere — rotated, flipped, stacked, with flashes and words.
import random, subprocess, os
random.seed(7)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.0
CLIPS = {'c1': 9.2, 'c2': 14.6, 'c3': 17.4, 'c4': 13.8}
inputs, filters = [], []
def inp(args):
    inputs.extend(args); return len(inputs_idx) if False else None
idx = 0
def add_input(args):
    global idx
    inputs.extend(args); idx += 1; return idx - 1

# background: rapid cuts of full-frame footage with alternating colour effects
fx = ['', 'negate', 'hue=h=120:s=3', 'hue=h=260:s=2.5', 'eq=contrast=1.6:saturation=2.5', 'hflip', 'vflip,hue=h=60:s=2']
bg_parts = []
t = 0.0; n = 0
while t < DUR:
    d = random.choice([0.25, 0.33, 0.4, 0.5])
    c = random.choice(list(CLIPS)); st = random.uniform(0, CLIPS[c] - d - .1)
    i = add_input(['-ss', f'{st:.2f}', '-t', f'{d:.2f}', '-i', f'../clips/{c}.mp4'])
    e = random.choice(fx)
    filters.append(f'[{i}:v]fps=30,scale=1920:1920,crop=1080:1920,setsar=1{","+e if e else ""},trim=duration={d},setpts=PTS-STARTPTS[bg{n}]')
    bg_parts.append(f'[bg{n}]'); t += d; n += 1
filters.append(f'{"".join(bg_parts)}concat=n={n}:v=1:a=0,trim=duration={DUR}[bgall]')
mask = add_input(['-i', 'ov/mask.png'])
# circle pops
pops = []
for k in range(18):
    s = random.uniform(0, DUR - 0.8); d = random.uniform(0.6, 1.6)
    c = random.choice(list(CLIPS)); st = random.uniform(0, CLIPS[c] - d - .1)
    size = random.choice([320, 420, 520, 640, 760])
    ang = random.choice([0, 15, -20, 35, 90, 180, -45, 160])
    flip = random.choice(['', 'hflip,', 'vflip,', ''])
    x = random.randint(-120, 1080 - size + 120); y = random.randint(80, 1920 - size - 80)
    i = add_input(['-ss', f'{st:.2f}', '-t', f'{d:.2f}', '-i', f'../clips/{c}.mp4'])
    filters.append(f'[{mask}:v]scale={size}:{size},format=gray[m{k}]')
    filters.append(f'[{i}:v]fps=30,{flip}scale={size}:{size},format=rgba,setpts=PTS-STARTPTS+{s:.2f}/TB[f{k}];[f{k}][m{k}]alphamerge,rotate={ang}*PI/180:c=none:ow=rotw({ang}*PI/180):oh=roth({ang}*PI/180)[p{k}]')
    pops.append((k, s, d, x, y))
cur = 'bgall'
for k, s, d, x, y in pops:
    filters.append(f'[{cur}][p{k}]overlay={x}:{y}:eof_action=pass:enable=\'between(t,{s:.2f},{s+d:.2f})\'[o{k}]'); cur = f'o{k}'
# words
for j, w in enumerate(['w1', 'w2', 'w3', 'w4', 'w5', 'w1', 'w2']):
    s = 0.4 + j * 1.35; d = 0.7
    ang = random.choice([-12, 8, -6, 14, -18])
    i = add_input(['-loop', '1', '-t', f'{DUR}', '-i', f'ov/{w}.png'])
    filters.append(f'[{i}:v]format=rgba,rotate={ang}*PI/180:c=none:ow=rotw({ang}*PI/180):oh=roth({ang}*PI/180)[wd{j}]')
    y = random.choice([260, 700, 1200, 1500])
    filters.append(f'[{cur}][wd{j}]overlay=(W-w)/2:{y}:enable=\'between(t,{s:.2f},{s+d:.2f})\'[ow{j}]'); cur = f'ow{j}'
# white flashes + shake-zoom
flashes = '+'.join(f'between(t,{f:.2f},{f+0.07:.2f})' for f in [random.uniform(0, DUR) for _ in range(12)])
filters.append(f'[{cur}]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.85:t=fill:enable=\'{flashes}\',scale=1180:2098,crop=1080:1920:\'50+40*sin(t*37)\':\'89+40*cos(t*29)\',format=yuv420p[v]')
# audio: the track keeps going
a = add_input(['-ss', '8.0', '-t', f'{DUR}', '-i', '../clips/c3.mp4'])
filters.append(f'[{a}:a]aresample=44100,aformat=channel_layouts=mono,afade=t=in:d=0.1[a]')
cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]', '-t', f'{DUR}',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '1', 'seg/chaos.mp4']
subprocess.run(cmd, check=True)
print('chaos done')
