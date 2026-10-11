from pathlib import Path
import json,re,csv
R=Path(__file__).resolve().parents[1]; fichas=json.loads((R/'data/fichas_bbva.json').read_text()); fees=[]
for f in fichas:
 text=((R/'results'/'fichas_temporales')/(f['fondo'].replace('+','plus')+'.txt')).read_text()
 for m in re.finditer(r'Pagadas por el Fondo de Inversión\s+Serie:\s*(\S+)(.*?)(?=Políticas para|Prestadores de Servicios|$)',text,re.S):
  serie,block=m.groups(); total=re.search(r'Totales\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)',block)
  admin=re.search(r'Administración de activos\s+(\d+(?:\.\d+)?)',block)
  dist=re.search(r'Distribución de acciones\s+(\d+(?:\.\d+)?)',block)
  if total:fees.append(dict(fondo=f['fondo'],serie=serie,total_publicado_pct=float(total[1]),administracion_pct=float(admin[1]) if admin else '',distribucion_pct=float(dist[1]) if dist else '',url_dici=f['url_dici'],fecha_consulta='2026-10-11',nota='Tasa publicada de gastos pagados por el fondo; confirmar periodicidad, vigencia y serie en DICI. No equivale a ingreso neto del banco ni a corretaje.'))
 # Replace long copyright text extracts with factual record metadata.
 f.pop('extracto_comisiones',None)
 f['series_comisiones_extraidas']=sum(x['fondo']==f['fondo'] for x in fees)
(R/'data/fichas_bbva.json').write_text(json.dumps(fichas,ensure_ascii=False,indent=2))
for name,rows in [('fichas_bbva.csv',fichas),('comisiones_por_serie.csv',fees)]:
 with (R/'data'/name).open('w',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('series',len(fees),'fondos',len(set(f['fondo'] for f in fees)),'sin extracción',[f['fondo'] for f in fichas if not f['series_comisiones_extraidas']])
print([f for f in fees if f['fondo']=='BBVACOR' and f['serie']=='P'])
