import subprocess, re, json
T={'n1':'А что если ты — Иван Кепчик…','i1':'Чёт оброс я. Зайду-ка к Герману.','n2':'…и ты пришёл в барбершоп к Герману.',
'g1':'Заходи, брат! Садись. Как стрижём?','i2':'Чуть-чуть по бокам. Сверху вообще не трогай.','g2':'Понял. Доверься профессионалу.',
'n3':'Через пятнадцать минут…','i3':'Герман, ты что делаешь?!','g3':'Готово! Красавчик!','n4':'…и он подстриг тебя хуже всех в этом городе.',
'i4':'Герман… это что вообще такое?','g4':'Это модно. С тебя тысяча пятьсот.','n5':'Вот поэтому он теперь и Кепчик.',
'i5':'Цибудин. Шмырдяк. Окей.','g5':'Сегодня в меню — стрижка «Кракабуля» с соусом цибудин.','i6':'Чё? Какой ещё цибудин?',
'g6':'Тихо. Машинка чувствует страх. Бжмырк.','g7':'Причёска называется «Жмыхарь Бурундукович». Цибудин в подарок.','n6':'Цибудин.'}
out={}
import os
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
    words=[w for w in txt.split() if w not in ('—',)]
    total=sum(b-a for a,b in segs); wl=[len(re.sub(r'[^\wё-]','',w,flags=re.I)) or 1 for w in words]; W=sum(wl)
    res=[]; acc=0
    def at(x):  # map speech-time x to clip time
        for a,b in segs:
            if x<=b-a: return a+x
            x-=b-a
        return segs[-1][1]
    for w,l in zip(words,wl):
        s=at(acc/W*total); acc+=l; e=at(acc/W*total)
        res.append([w,round(s,3),round(e,3)])
    out[k]={'d':round(D,3),'w':res}
json.dump(out,open('words.json','w'),ensure_ascii=False)
for k,v in out.items(): print(k,v['w'][:2],v['w'][-1])
