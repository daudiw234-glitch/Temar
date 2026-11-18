import base64, json, os
S=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(S,'..','chats.src.html')).read()
M=''
if os.path.exists(S+'/music.mp3'): M='data:audio/mpeg;base64,'+base64.b64encode(open(S+'/music.mp3','rb').read()).decode()
import subprocess, glob
V={}; DUR={}
for p in sorted(glob.glob(S+'/voice/[vj]*.mp3')):
    k=os.path.basename(p)[:-4]
    V[k]='data:audio/mpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
    DUR[k]=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
src=src.replace('/*MUSIC*/""',json.dumps(M)).replace('/*VOICE*/{}',json.dumps(V)).replace('/*VDUR*/{}',json.dumps(DUR))
open(os.path.join(S,'..','chats.html'),'w').write(src); print('built', len(src))
