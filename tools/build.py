import base64, json, sys, os
S=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(S,'..','kepchik-story.src.html')).read()
W=json.load(open(S+'/words.json'))
V={k:'data:audio/mpeg;base64,'+base64.b64encode(open(f'{S}/voice/{k}.mp3','rb').read()).decode() for k in W}
M=''
if os.path.exists(S+'/music.mp3'): M='data:audio/mpeg;base64,'+base64.b64encode(open(S+'/music.mp3','rb').read()).decode()
src=src.replace('/*VOICE*/{}',json.dumps(V)).replace('/*WORDS*/{}',json.dumps(W,ensure_ascii=False)).replace('/*MUSIC*/""',json.dumps(M))
open(os.path.join(S,'..','kepchik-story.html'),'w').write(src); print('built', len(src))
