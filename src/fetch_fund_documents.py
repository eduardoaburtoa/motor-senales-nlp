from pathlib import Path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import requests, csv, hashlib, io, json
from bs4 import BeautifulSoup
from pypdf import PdfReader
base='https://www.bbva.mx'
out=Path(__file__).resolve().parents[1]; tmp=out/'results'/'fichas_temporales'; tmp.mkdir(parents=True,exist_ok=True)
s=BeautifulSoup(requests.get(base+'/personas/productos/inversion/normativa-de-fondos.html',timeout=40).text,'html.parser')
urls=list(dict.fromkeys(urljoin(base,a['href']) for a in s.select('a[href]') if '/normativa-de-fondos/' in a['href']))
rows=[]
for u in urls:
 h=requests.get(u,timeout=40); soup=BeautifulSoup(h.text,'html.parser')
 for tr in soup.select('tr'):
  cells=tr.find_all(['td','th']); aa=tr.select('a[href]')
  if len(aa)>=2 and cells:
   name=cells[0].get_text(' ',strip=True).removeprefix('FONDO ').strip()
   if name.startswith(('BBVA','B+')):
    rows.append(dict(fondo=name,url_pagina=u,url_prospecto=urljoin(base,aa[0]['href']),url_dici=urljoin(base,aa[1]['href'])))
rows=list({r['fondo']:r for r in rows}.values())
def get(r):
 try:
  b=requests.get(r['url_dici'],timeout=45);b.raise_for_status()
  pdf=PdfReader(io.BytesIO(b.content));text='\n'.join(p.extract_text() or '' for p in pdf.pages)
  (tmp/(r['fondo'].replace('+','plus')+'.txt')).write_text(text)
  r.update(estado='consultado',sha256=hashlib.sha256(b.content).hexdigest(),paginas=len(pdf.pages),fecha_consulta='2026-10-11')
  lines=text.splitlines(); snippets=[]
  for i,l in enumerate(lines):
   if any(x in l.lower() for x in ['comisiones','remuneraci','administración de activos']):snippets.append('\n'.join(lines[max(0,i-1):i+14]))
  r['extracto_comisiones']=''  # No redistribuir texto extenso de terceros
 except Exception as e:r.update(estado=type(e).__name__,sha256='',paginas='',fecha_consulta='2026-10-11',extracto_comisiones='')
 return r
with ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(get,rows))
(out/'data/fichas_bbva.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (out/'data/fichas_bbva.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Fichas',len(rows),'leidas',sum(r['estado']=='consultado' for r in rows))
cat={r['fondo'] for r in csv.DictReader((out/'data/catalogo_fondos.csv').open())};found={r['fondo'] for r in rows};print('Sin ficha en indice',sorted(cat-found))
