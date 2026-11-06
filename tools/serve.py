"""Local preview of the Apache/Vercel route map (no PHP execution)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import os
os.chdir(Path(__file__).resolve().parents[1])
class Handler(SimpleHTTPRequestHandler):
 extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.php':'application/xml'}
 def do_GET(self):
  path=urlsplit(self.path).path
  redirects={'/spectrum':'/spectrum/','/spectrum-tv/':'/spectrum/','/spectrum-tv/index.htm':'/spectrum/','/index.htm':'/','/xfinity':'/xfinity/','/xfinity/index.htm':'/xfinity/','/xfinity/index.html':'/xfinity/'}
  if path in redirects:
   self.send_response(301);self.send_header('Location',redirects[path]);self.end_headers();return
  if path=='/spectrum/':self.path='/spectrum-tv/index.htm'
  elif path.endswith('/') and Path('.'+path,'index.htm').is_file():self.path=path+'index.htm'
  super().do_GET()
 def guess_type(self,path):
  if Path(path).name in ('css','css2'):return 'text/css'
  return super().guess_type(path)
if __name__=='__main__':
 print('Preview: http://127.0.0.1:8080',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8080),Handler).serve_forever()
