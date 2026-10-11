"""Pruebas de integridad y casos límite. No simula métricas de modelos."""
import csv, json, hashlib, random, tempfile, ast
from pathlib import Path
import build_dataset as b
from evaluate import metricas, curva_umbral, normaliza_etiqueta
from portfolio_rules import evaluar_cambio
R=Path(__file__).resolve().parents[1]
def main():
    read=lambda name:list(csv.DictReader((R/'data'/name).open()))
    notes=read('notas_mercado.csv');clients=read('clientes_simulados.csv');cat=read('catalogo_fondos.csv')
    assert len(notes)==400 and len({r['texto'] for r in notes})==400
    assert {x:sum(r['impacto']==x for r in notes) for x in ['POSITIVO','NEGATIVO','NEUTRAL']}==dict(POSITIVO=158,NEGATIVO=158,NEUTRAL=84)
    random.seed(b.SEMILLA);assert b.construir_notas()==notes
    rebuilt=b.construir_clientes();assert [{k:str(v) for k,v in r.items()} for r in rebuilt]==clients
    assert len(clients)==150 and len({r['nombre'] for r in clients})==150
    assert all(5_000_000<=int(r['posicion_mxn'])<=20_000_000 for r in clients)
    assert sum(int(r['posicion_mxn']) for r in clients)==1_831_243_000
    assert len(cat)==484 and len({r['fondo'] for r in cat})==59
    assert metricas(['NEGATIVO','NEUTRAL','POSITIVO'],['NEGATIVO','NEUTRAL','POSITIVO'])['f1_macro']==1
    assert normaliza_etiqueta('5 stars')=='POSITIVO'
    z=curva_umbral(['POSITIVO'],['NEGATIVO'],[.4],[.9])[0]
    assert z['cobertura_pct']==0 and z['exactitud_aceptadas_pct'] is None
    assert evaluar_cambio(10_000_000,.03,True,True)['estado']=='BLOQUEADO'
    assert evaluar_cambio(10_000_000,.10,False,True)['estado']=='BLOQUEADO'
    assert evaluar_cambio(10_000_000,.10,True,False)['estado']=='BLOQUEADO'
    assert evaluar_cambio(10_000_000,.10,True,True,2)['estado']=='BLOQUEADO'
    assert evaluar_cambio(10_000_000,.10,True,True)['estado']=='REQUIERE_REVISION_HUMANA'
    assert not evaluar_cambio(10_000_000,.10,True,True)['orden_autorizada']
    for p in (R/'notebooks').glob('*.ipynb'):
        n=json.loads(p.read_text())
        for c in n['cells']:
            if c['cell_type']=='code':ast.parse('\n'.join(x for x in ''.join(c['source']).splitlines() if not x.startswith(('%','!'))))
    fichas=json.loads((R/'data/fichas_bbva.json').read_text())
    assert {r['fondo'] for r in cat}<={r['fondo'] for r in fichas if r['estado']=='consultado'}
    print('OK: corpus y clientes reproducidos; catálogo; cobertura DICI; métricas; abstención vacía; reglas económicas; sintaxis de notebook.')
if __name__=='__main__':main()
