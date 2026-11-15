# Hip-hop beat bed: boom-bap kick/snare, swung hats, 808-style bass, dark keys.
import numpy as np, wave, sys
L=float(sys.argv[1]); out=sys.argv[2]
sr=44100; bpm=92; beat=60/bpm; n=int(L*sr); y=np.zeros(n); rng=np.random.default_rng(5)
N=lambda m: 440*2**((m-69)/12)
def add(sig,t0,g=1.0):
    i=int(t0*sr); j=min(n,i+len(sig))
    if i<n: y[i:j]+=g*sig[:j-i]
def kick():
    t=np.arange(int(.35*sr))/sr; f=45+110*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*8)
def snare():
    t=np.arange(int(.22*sr))/sr; x=rng.uniform(-1,1,len(t)); hp=x-np.concatenate([[0],x[:-1]])
    return (.7*hp*np.exp(-t*18)+.4*np.sin(2*np.pi*190*t)*np.exp(-t*25))
def hat(): t=np.arange(int(.05*sr))/sr; x=rng.uniform(-1,1,len(t)); return (x-np.concatenate([[0],x[:-1]]))*np.exp(-t*80)*.3
def b808(f,dur): t=np.arange(int(dur*sr))/sr; return .8*np.tanh(2*np.sin(2*np.pi*f*t))*np.exp(-t*2.2)
def key(f,dur): t=np.arange(int(dur*sr))/sr; return .08*(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t))*np.exp(-t*1.4)*np.minimum(1,t/.01)
K,S,H=kick(),snare(),hat()
prog=[[45,52,57,60],[41,48,53,57],[43,50,55,59],[40,47,52,55]]
t=0.0; bar=0
while t<L:
    ch=prog[bar%4]
    for b in range(4):
        tb=t+b*beat
        if b in (0,2): add(K,tb,.95)
        if b==2: add(K,tb+beat*.75,.6)
        if b in (1,3): add(S,tb,.75)
        for h in range(2): add(H,tb+h*beat/2+(beat*.06 if h else 0),.8)
    add(b808(N(ch[0]-12),beat*2),t); add(b808(N(ch[0]-12),beat*1.5),t+beat*2.5)
    for m in ch[1:]: add(key(N(m+12),beat*4),t)
    t+=4*beat; bar+=1
fade=int(1.0*sr); y[-fade:]*=np.linspace(1,0,fade)
y=y/np.max(np.abs(y))*0.9
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
