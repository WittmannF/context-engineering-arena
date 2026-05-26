#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, time, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
TASK_ID='task-002-brazil-public-money-trail'; ROOT=Path(__file__).resolve().parents[3]; RAW=ROOT/'data/raw'/TASK_ID; CAMARA_BASE='https://dadosabertos.camara.leg.br/api/v2'
THEME_TERMS={'health':'saúde','education':'educação','environment':'meio ambiente','infrastructure':'infraestrutura','agriculture':'agricultura','public security':'segurança pública','social assistance':'assistência social','science and technology':'ciência e tecnologia'}
def fetch_json(url):
    req=urllib.request.Request(url, headers={'User-Agent':'ContextEngineeringArena/0.1 (public accountability benchmark)'})
    with urllib.request.urlopen(req, timeout=30) as resp: return json.loads(resp.read().decode('utf-8','replace'))
def write_json(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def camara_url(endpoint, **params): return f"{CAMARA_BASE}/{endpoint}?{urllib.parse.urlencode({k:v for k,v in params.items() if v is not None})}"
def download_camara(theme, year_start, year_end, sample_only, force):
    out=RAW/'camara'; out.mkdir(parents=True, exist_ok=True); term=THEME_TERMS.get(theme, theme); limit=10 if sample_only else 100
    prop_path=out/f'proposicoes_{theme}_{year_start}_{year_end}.json'
    if force or not prop_path.exists():
        url=camara_url('proposicoes', keywords=term, ano=year_start, itens=limit, ordem='ASC', ordenarPor='id'); print('Downloading Câmara propositions:', url); write_json(prop_path, {'source_url':url,'theme':theme,'term':term,'sample_only':sample_only,'downloaded_at':datetime.utcnow().isoformat()+'Z','response':fetch_json(url)}); time.sleep(.5)
    dep_path=out/'deputados.json'
    if force or not dep_path.exists():
        url=camara_url('deputados', itens=20 if sample_only else 100); print('Downloading Câmara deputies:', url); write_json(dep_path, {'source_url':url,'sample_only':sample_only,'downloaded_at':datetime.utcnow().isoformat()+'Z','response':fetch_json(url)}); time.sleep(.5)
def write_transparencia_sample(theme, year_start, year_end, mock):
    sample={'source':'MOCK_TRANSPARENCY_SAMPLE_FOR_LOCAL_TESTING_ONLY' if mock else 'Portal da Transparência API de Dados','mock':mock,'theme':theme,'year_start':year_start,'year_end':year_end,'records':[{'id':'sample-expense-001','year':year_start,'agency':'Ministério da Saúde' if theme=='health' else 'Órgão federal relacionado ao tema','program':'Atenção Primária em Saúde' if theme=='health' else f'Programa público de {theme}','amount_brl':1250000.0,'beneficiary':'Município de Exemplo','region':'DF','link_classification':'same_theme_link'},{'id':'sample-expense-002','year':year_end,'agency':'Fundo Nacional de Saúde' if theme=='health' else 'Fundo público de exemplo','program':'Transferência fundo a fundo' if theme=='health' else f'Transferência pública de {theme}','amount_brl':860000.0,'beneficiary':'Entidade Pública de Exemplo','region':'GO','link_classification':'same_time_window_link'}],'warning':'Synthetic sample for UI/schema testing only. Do not use for official scoring.' if mock else 'Real API sample placeholder; verify endpoint-specific coverage.'}
    write_json(RAW/'transparencia'/f'expenses_{theme}_{year_start}_{year_end}.json', sample)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--theme',default='health'); ap.add_argument('--year-start',type=int,default=2023); ap.add_argument('--year-end',type=int,default=2024); ap.add_argument('--sample-only',action='store_true'); ap.add_argument('--force',action='store_true'); ap.add_argument('--skip-transparencia',action='store_true'); ap.add_argument('--skip-tcu',action='store_true'); args=ap.parse_args(); RAW.mkdir(parents=True, exist_ok=True)
    print('ETHICS NOTICE: public accountability, not accusation. Do not infer wrongdoing without direct authoritative evidence.')
    download_camara(args.theme,args.year_start,args.year_end,args.sample_only,args.force)
    token=os.getenv('TRANSPARENCIA_API_TOKEN')
    if args.skip_transparencia: print('Skipping Portal da Transparência by request.')
    elif not token: print('TRANSPARENCIA_API_TOKEN missing. Get access via https://api.portaldatransparencia.gov.br/ . Writing mock local fixture.'); write_transparencia_sample(args.theme,args.year_start,args.year_end,True)
    else: print('TRANSPARENCIA_API_TOKEN detected. MVP writes token-aware sample cache; extend endpoint-specific queries per theme.'); write_transparencia_sample(args.theme,args.year_start,args.year_end,False)
    if args.skip_tcu: print('Skipping optional TCU enrichment.')
    else: write_json(RAW/'tcu'/'manifest.json', {'source_url':'https://sites.tcu.gov.br/dados-abertos/','optional':True,'note':'Optional enrichment placeholder; pipeline does not require TCU.'})
    write_json(RAW/'source_manifest.json', {'task_id':TASK_ID,'theme':args.theme,'year_start':args.year_start,'year_end':args.year_end,'sample_only':args.sample_only,'created_at':datetime.utcnow().isoformat()+'Z'}); print('Wrote raw cache under', RAW)
if __name__=='__main__': main()
