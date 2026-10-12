"""Loopback-only website, durable progress, and bounded personal Python judge."""
import argparse, hashlib, json, os, threading, time, uuid
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
from judge import run
ROOT=Path(__file__).resolve().parent
LOCK=threading.Lock()
DATA=ROOT/'data'/'progress.json'
EXPORTS={}
STYLE_NONCE=uuid.uuid4().hex
def revision(state):
    if state is None: return None
    return hashlib.sha256(json.dumps(state,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'static'),**kwargs)
    def valid_host(self):
        host=self.headers.get('Host','')
        return host in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
    def send_json(self,obj,status=200):
        data=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',f"default-src 'self'; script-src 'self'; style-src 'self' 'nonce-{STYLE_NONCE}'; style-src-attr 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        super().end_headers()
    def do_GET(self):
        if not self.valid_host(): return self.send_json({'error':'Use the loopback address.'},403)
        path=urlsplit(self.path).path
        if path.startswith('/api/download/'):
            key=path.rsplit('/',1)[-1]
            with LOCK: entry=EXPORTS.get(key)
            if not entry or time.time()-entry[0]>900: return self.send_json({'error':'Backup link expired. Reopen Progress & data.'},404)
            payload=entry[1]
            self.send_response(200); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Disposition',f'attachment; filename="{entry[2]}"'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(payload))); self.end_headers(); self.wfile.write(payload); return
        if path=='/api/progress':
            with LOCK:
                try: state=json.loads(DATA.read_text()) if DATA.exists() else None
                except (OSError,ValueError): return self.send_json({'error':'Saved progress could not be read; export browser progress before restarting.'},500)
            return self.send_json({'state':state,'revision':revision(state)})
        if path.startswith('/api/'): return self.send_json({'error':'Not found'},404)
        if path in {'/','/index.html'}:
            # CodeMirror creates style sheets. Permit only this server's nonce-bearing
            # styles, while retaining the existing restriction on inline scripts.
            html=(ROOT/'static/index.html').read_text().replace('__EDITOR_STYLE_NONCE__',STYLE_NONCE).encode()
            self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(html)))
            self.end_headers(); self.wfile.write(html); return
        return super().do_GET()
    def do_POST(self):
        if not self.valid_host(): return self.send_json({'error':'Use the loopback address.'},403)
        origin=self.headers.get('Origin')
        if origin and origin not in {f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}:
            return self.send_json({'error':'Cross-site requests are unavailable.'},403)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size < 1 or size > 2_000_000: raise ValueError('Invalid request size.')
            obj=json.loads(self.rfile.read(size))
            if not isinstance(obj,dict): raise ValueError('Expected an object.')
        except (ValueError,UnicodeError) as error: return self.send_json({'error':str(error)},400)
        path=urlsplit(self.path).path
        if path=='/api/export':
            if obj.get('version')!=1 or not all(isinstance(obj.get(k),dict) for k in ['questions','coding','lessons','drafts']) or not isinstance(obj.get('trainers'),list):
                return self.send_json({'error':'Invalid backup format.'},400)
            key=uuid.uuid4().hex
            with LOCK:
                for old in [k for k,v in EXPORTS.items() if time.time()-v[0]>900]: del EXPORTS[old]
                while len(EXPORTS)>=32: del EXPORTS[next(iter(EXPORTS))]
                filename=('quant-atelier-test-preview-' if obj.get('workspace')=='preview' else 'quant-atelier-progress-')+time.strftime('%Y-%m-%d',time.gmtime())+'.json'
                EXPORTS[key]=(time.time(),json.dumps(obj,ensure_ascii=False,indent=2).encode(),filename)
            return self.send_json({'url':'/api/download/'+key})
        if path=='/api/judge':
            if not isinstance(obj.get('code'),str): return self.send_json({'error':'Missing code.'},400)
            return self.send_json(run(obj.get('id'),obj['code'],obj.get('mode','submit')))
        if path=='/api/progress':
            envelope='state' in obj and 'revision' in obj
            expected=obj.get('revision') if envelope else None
            obj=obj.get('state') if envelope else obj
            if not isinstance(obj,dict): return self.send_json({'error':'Invalid progress format.'},400)
            if obj.get('version')!=1 or not all(isinstance(obj.get(k),dict) for k in ['questions','coding','lessons','drafts']):
                return self.send_json({'error':'Invalid progress format.'},400)
            with LOCK:
                try:
                    current=json.loads(DATA.read_text()) if DATA.exists() else None
                    current_revision=revision(current)
                    # Unchanged requests are safe even after another tab's save.
                    if revision(obj)==current_revision: return self.send_json({'saved':True,'revision':current_revision})
                    if expected!=current_revision:
                        return self.send_json({'error':'Progress changed in another tab.','state':current,'revision':current_revision},409)
                    DATA.parent.mkdir(exist_ok=True)
                    temp=DATA.with_suffix('.tmp'); temp.write_text(json.dumps(obj,ensure_ascii=False)); os.replace(temp,DATA)
                except (OSError,ValueError): return self.send_json({'error':'Could not safely save progress to disk.'},500)
            return self.send_json({'saved':True,'revision':revision(obj)})
        return self.send_json({'error':'Not found'},404)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8768); args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Quant Atelier → http://127.0.0.1:{args.port}',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
