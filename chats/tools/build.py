import base64, json, os
S=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(S,'..','chats.src.html')).read()
M=''
if os.path.exists(S+'/music.mp3'): M='data:audio/mpeg;base64,'+base64.b64encode(open(S+'/music.mp3','rb').read()).decode()
src=src.replace('/*MUSIC*/""',json.dumps(M))
open(os.path.join(S,'..','chats.html'),'w').write(src); print('built', len(src))
