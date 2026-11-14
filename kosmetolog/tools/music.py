# Upbeat glam-pop loop: four-on-the-floor kick, claps, hats, offbeat bass, electric-piano stabs.
import numpy as np, wave, sys
L=float(sys.argv[1]); out=sys.argv[2]
sr=44100; bpm=118; beat=60/bpm; n=int(L*sr); y=np.zeros(n)
rng=np.random.default_rng(3)
N=lambda m: 440*2**((m-69)/12)
def add(sig,t0,g=1.0):
    i=int(t0*sr); j=min(n,i+len(sig))
    if i<n: y[i:j]+=g*sig[:j-i]
def kick():
    t=np.arange(int(.25*sr))/sr; f=50+90*np.exp(-t*28); return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*12)
def clap():
    t=np.arange(int(.18*sr))/sr; x=rng.uniform(-1,1,len(t)); env=np.exp(-t*22)*(1+.6*(np.sin(2*np.pi*90*t)>0))
    hp=x-np.concatenate([[0],x[:-1]]); return hp*env*.6
def hat(open_=False):
    t=np.arange(int((.12 if open_ else .04)*sr))/sr; x=rng.uniform(-1,1,len(t)); hp=x-np.concatenate([[0],x[:-1]])
    return hp*np.exp(-t*(25 if open_ else 90))*.35
def ep(f,dur,vol):
    t=np.arange(int(dur*sr))/sr
    w=np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*2*f*t)*np.exp(-t*4)+.15*np.sin(2*np.pi*3*f*t)*np.exp(-t*8)
    return vol*w*np.minimum(1,t/.005)*np.exp(-t*3.2)
def bass(f,dur):
    t=np.arange(int(dur*sr))/sr; w=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t)
    return .55*w*np.minimum(1,t/.004)*np.exp(-t*5)
K,C,H=kick(),clap(),hat()
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,60],[55,59,62,67]]   # Am7 Fmaj7 C G
t=0.0; bar=0
while t<L:
    ch=chords[bar%4]
    for b in range(4):
        tb=t+b*beat
        add(K,tb,.9)
        if b in (1,3): add(C,tb,.8)
        add(H,tb+beat/2,.9); add(hat(b==3),tb+beat*0.75,.5)
        add(bass(N(ch[0]-24),beat*.45),tb+beat/2)
    for st in (0,1.5,2.5):
        for m in ch: add(ep(N(m+12),beat*1.2,.07),t+st*beat)
    t+=4*beat; bar+=1
fade=int(1.5*sr); y[-fade:]*=np.linspace(1,0,fade)
y=y/np.max(np.abs(y))*0.9
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
