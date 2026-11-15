import subprocess, re, json, os
T={'a1':'В нашем компьютерном клубе ИЗИ появился новый вечерний админ.',
'a2':'Его зовут Михаил. Но для своих — Мифутка.',
'a3':'Однажды мы с Кентом случайно нашли его ютуб-канал.',
'a4':'А там — его трек.',
'a5':'Мы послушали. Потом ещё раз. И ещё.',
'a6':'С тех пор каждый день мы тихо включаем его песню, пока он не видит.',
'a7':'А сегодня мы врубили её в подъезде.',
'a8':'И пошёл лютый флекс!'}
out={}
for k,txt in T.items():
    f=f'voice/{k}.mp3'
    if not os.path.exists(f): continue
    D=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    log=subprocess.run(['ffmpeg','-v','info','-i',f,'-af','silencedetect=n=-38dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
    ev=[(m.group(1),float(m.group(2))) for m in re.finditer(r'silence_(start|end): ([0-9.]+)',log)]
    segs=[]; cur=0.0
    for typ,t in ev:
        if typ=='start':
            if t-cur>0.05: segs.append([cur,t])
        else: cur=t
    if D-cur>0.15 and (not ev or ev[-1][0]=='end'): segs.append([cur,D])
    if not segs: segs=[[0,D]]
    words=[w for w in txt.split() if w not in ('—',)]
    total=sum(b-a for a,b in segs); wl=[len(re.sub(r'[^\wё-]','',w,flags=re.I)) or 1 for w in words]; W=sum(wl)
    def at(x):
        for a,b in segs:
            if x<=b-a: return a+x
            x-=b-a
        return segs[-1][1]
    res=[]; acc=0
    for w,l in zip(words,wl):
        s=at(acc/W*total); acc+=l; e=at(acc/W*total)
        res.append([w,round(s,3),round(e,3)])
    out[k]={'d':round(D,3),'w':res}
json.dump(out,open('words.json','w'),ensure_ascii=False)
print({k:v['d'] for k,v in out.items()})
