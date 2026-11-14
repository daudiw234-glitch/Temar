import numpy as np, wave, sys
L=float(sys.argv[1]); out=sys.argv[2]
sr=44100; bpm=132; e=60/bpm/2  # eighth note
N=lambda m: 440*2**((m-69)/12)
# 2-bar phrases, 16 eighths each; None = rest
lead=[ [76,None,79,76,74,None,72,None, 74,76,None,72,69,None,None,None],
       [72,None,76,72,71,None,67,None, 69,71,72,74,76,None,79,None],
       [81,None,79,76,77,None,76,74, 72,None,74,None,76,None,None,None],
       [74,72,71,72,74,None,67,None, 69,None,None,72,69,None,None,None] ]
bass=[ [45,45,57,45,41,41,53,41, 43,43,55,43,45,45,57,45],
       [41,41,53,41,43,43,55,43, 45,45,57,45,40,40,52,40] ]
def sq(f,n,duty=.25):
    t=np.arange(n)/sr; return np.where((t*f)%1<duty,1.0,-1.0)
def tri(f,n):
    t=np.arange(n)/sr; return 2*np.abs(2*((t*f)%1)-1)-1
n=int(L*sr); y=np.zeros(n); step=int(e*sr); i=0; k=0
rng=np.random.default_rng(7)
while i<n:
    ph=lead[(k//16)%4]; bs=bass[(k//16)%2]; j=k%16
    seg=min(step,n-i); t=np.arange(seg)/sr
    m=ph[j]
    if m: env=np.exp(-t*6); y[i:i+seg]+=0.16*sq(N(m),seg)*env
    y[i:i+seg]+=0.20*tri(N(bs[j]),seg)*np.minimum(1,(seg-np.arange(seg))/400)
    if j%2==1: hn=min(int(.04*sr),seg); y[i:i+hn]+=0.05*rng.uniform(-1,1,hn)*np.exp(-np.arange(hn)/sr*80)
    if j%8==0: kn=min(int(.12*sr),seg); tt=np.arange(kn)/sr; y[i:i+kn]+=0.35*np.sin(2*np.pi*(150*np.exp(-tt*25)+45)*tt)*np.exp(-tt*18)
    i+=step; k+=1
fade=int(1.5*sr); y[-fade:]*=np.linspace(1,0,fade); y[:int(.05*sr)]*=np.linspace(0,1,int(.05*sr))
y=y/np.max(np.abs(y))*0.9
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
