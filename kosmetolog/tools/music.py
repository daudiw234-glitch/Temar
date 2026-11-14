# Soft, warm background loop: electric-piano style broken chords over a quiet pad.
import numpy as np, wave, sys
L=float(sys.argv[1]); out=sys.argv[2]
sr=44100; bpm=76; beat=60/bpm; n=int(L*sr)
y=np.zeros(n)
N=lambda m: 440*2**((m-69)/12)
# Fmaj7 - Em7 - Dm7 - Cmaj7 (one bar each)
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]
def ep(f,dur,vol):
    t=np.arange(int(dur*sr))/sr
    w=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
    env=np.minimum(1,t/.008)*np.exp(-t*1.6)*(1+.12*np.sin(2*np.pi*4.5*t))
    return vol*w*env
def add(sig,t0):
    i=int(t0*sr); j=min(n,i+len(sig)); 
    if i<n: y[i:j]+=sig[:j-i]
bar=4*beat; t=0.0; k=0
pattern=[0,2,1,3,2,1,3,2]   # eighth-note broken chord
while t<L:
    ch=chords[k%4]
    add(ep(N(ch[0]-12),bar*1.1,.30),t)                       # bass
    tt=np.arange(int(bar*1.2*sr))/sr                         # pad
    pad=sum(np.sin(2*np.pi*N(m+12)*tt) for m in ch)/4
    add(.05*pad*np.minimum(1,tt/.6)*np.minimum(1,(bar*1.2-tt)/.6),t)
    for i,p in enumerate(pattern):
        add(ep(N(ch[p]+12),beat*1.5,.10 if i%2 else .14),t+i*beat/2)
    t+=bar; k+=1
fade=int(2*sr); y[-fade:]*=np.linspace(1,0,fade); y[:int(.3*sr)]*=np.linspace(0,1,int(.3*sr))
# gentle low-pass to keep it warm
a=np.exp(-2*np.pi*3500/sr); acc=0.0; out_y=np.empty_like(y)
for i in range(n): acc=(1-a)*y[i]+a*acc; out_y[i]=acc
out_y=out_y/np.max(np.abs(out_y))*0.9
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out_y*32767).astype(np.int16).tobytes()); w.close()
