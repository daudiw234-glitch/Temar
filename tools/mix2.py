import json, wave, subprocess, numpy as np
tl=json.load(open('timeline.json')); sr=44100; L=tl['total']/1000+0.3; n=int(L*sr)
out=np.zeros(n)
def rd(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',path,'-f','s16le','-ac','1','-ar',str(sr),'-'])
    return np.frombuffer(raw,np.int16).astype(float)/32768
def add(sig,t,g=1.0):
    i=int(t*sr); j=min(n,i+len(sig)); out[i:j]+=g*sig[:j-i]
def blip(f0,f1,dur,vol,typ='square'):
    t=np.arange(int(dur*sr))/sr; f=f0*(f1/f0)**(t/dur); ph=np.cumsum(f)/sr
    w=np.where(ph%1<.5,1.,-1.) if typ=='square' else 2*np.abs(2*(ph%1)-1)-1
    return vol*w*np.exp(np.log(.001/1)*t/dur)
music=rd('music.wav'); add(music,0,0.16)
buzz_on=None
for e in tl['events']:
    t=e['t']/1000
    if e['type']=='voice': add(rd(f"voice/{e['k']}.mp3"),t,1.0)
    elif e['type']=='pop': add(blip(520,1040,.09,.12),t)
    elif e['type']=='whoosh': add(blip(900,200,.18,.10,'tri'),t)
    elif e['type']=='ding': add(blip(220,90,.7,.35,'tri'),t)
    elif e['type']=='alarm': add(blip(880,440,.25,.12),t)
    elif e['type']=='buzzOn': buzz_on=t
    elif e['type']=='buzzOff' and buzz_on is not None:
        d=t-buzz_on; tt=np.arange(int(d*sr))/sr; f=118+14*np.sin(2*np.pi*9*tt); ph=np.cumsum(f)/sr
        saw=2*(ph%1)-1; a=np.exp(-2*np.pi*1400/sr); y=np.zeros_like(saw); acc=0
        for k in range(len(saw)): acc=(1-a)*saw[k]+a*acc; y[k]=acc
        env=np.minimum(1,np.minimum(tt/.1,(tt[-1]-tt)/.15)); add(0.16*y/np.max(np.abs(y))*env,buzz_on)
out=out/max(1,np.max(np.abs(out))/0.95)
w=wave.open('mix_story.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print('len',L)
