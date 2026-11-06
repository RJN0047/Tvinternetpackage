"""Check served entry pages, assets (including CSS fonts), and local navigation."""
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin,urlsplit
from collections import deque
import json,re
ORIGIN='http://127.0.0.1:8080'
queue=deque((ORIGIN+p,'page') for p in ('/','/spectrum/','/xfinity/'))
seen=set(); failures=[]; placeholders=0
class Parser(HTMLParser):
 def handle_starttag(self,tag,attrs):
  global placeholders
  d=dict(attrs)
  for key in ('src','data-src','href','poster'):
   val=d.get(key,'')
   if tag=='a' and val=='#':placeholders+=1
   if not val or val.startswith(('#','data:','tel:','mailto:','javascript:')):continue
   if key=='href' and tag=='link' and not set(d.get('rel','').split())&{'stylesheet','icon','apple-touch-icon'}:continue
   url=urljoin(current,val)
   if urlsplit(url).netloc==urlsplit(ORIGIN).netloc:queue.append((url,'page' if tag=='a' else 'asset'))
while queue:
 current,kind=queue.popleft();current=current.split('#')[0]
 if current in seen:continue
 seen.add(current)
 try:
  with urlopen(current,timeout=10) as r: body=r.read();typ=r.headers.get('Content-Type','')
  if 'text/html' in typ:Parser().feed(body.decode('utf-8-sig'))
  elif 'text/css' in typ:
   for val in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',body.decode('utf-8-sig')):
    url=urljoin(current,val)
    if urlsplit(url).netloc==urlsplit(ORIGIN).netloc:queue.append((url,'asset'))
 except Exception as e:failures.append({'url':current,'kind':kind,'error':str(e)})
result={'checked':len(seen),'failures':failures,'existingHashPlaceholderLinks':placeholders}
print(json.dumps(result,indent=2));open('route-check.json','w').write(json.dumps(result,indent=2)+'\n')
raise SystemExit(bool(failures))
