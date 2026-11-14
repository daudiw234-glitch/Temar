import subprocess, re, json, os
T={'n1':'Ты только что вышла от косметолога.',
'p1':'М-м-м… Как заново родилась.',
'n2':'Вечером — ужин с подругой. Вам обеим по пятьдесят.',
'f1':'Светочка?! Это ты? Я тебя не узнала!',
'f2':'Как ты так молодо выглядишь? Мы же ровесницы!',
'p2':'Ой, да ничего особенного… Правильное питание. Генетика. И масочки из огурчика.',
'n3':'Масочки из огурчика. Ну-ну.',
'f3':'Всё. Завтра же иду за огурцами!',
'n4':'Огурцы не помогут. Записывайся к косметологу — запись в профиле.'}
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
print(sorted(out))
