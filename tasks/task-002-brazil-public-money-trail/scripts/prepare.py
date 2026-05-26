#!/usr/bin/env python3
from __future__ import annotations
import json, re, sqlite3
from datetime import datetime
from pathlib import Path
TASK_ID='task-002-brazil-public-money-trail'; ROOT=Path(__file__).resolve().parents[3]; RAW=ROOT/'data/raw'/TASK_ID; OUT=ROOT/'data/processed'/TASK_ID
def read_json(path): return json.loads(path.read_text(encoding='utf-8'))
def write_json(path,obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def write_jsonl(path,rows): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf-8')
def slug(s): return re.sub(r'\W+','-',str(s or '').lower()).strip('-') or 'unknown'
def load_camara():
    props=[]; deps=[]; evidence=[]; timeline=[]
    cam=RAW/'camara'
    if cam.exists():
        for path in cam.glob('proposicoes_*.json'):
            payload=read_json(path)
            for p in payload.get('response',{}).get('dados',[]):
                pid=str(p.get('id','')); title=str(p.get('ementa') or p.get('descricaoTipo') or p.get('siglaTipo') or '').strip()
                props.append({'id':pid,'source':'camara','theme':payload.get('theme'),'title':title,'type':p.get('siglaTipo'),'number':p.get('numero'),'year':p.get('ano'),'uri':p.get('uri'),'link_classification':'direct_documented_link'})
                evid=f'camara-prop-{pid}'; evidence.append({'id':evid,'source_type':'legislative_record','source_id':pid,'title':title[:120] or f'Proposição {pid}','date':str(p.get('ano') or ''),'excerpt':title,'location':'Câmara dos Deputados Dados Abertos','url':p.get('uri'),'metadata':{'theme':payload.get('theme')}}); timeline.append({'date':str(p.get('ano') or ''),'title':f"Proposição {p.get('siglaTipo','')} {p.get('numero','')}/{p.get('ano','')}",'description':title,'evidence_id':evid,'event_type':'legislative_activity'})
        dep=cam/'deputados.json'
        if dep.exists():
            for d in read_json(dep).get('response',{}).get('dados',[]): deps.append({'id':str(d.get('id','')),'name':d.get('nome'),'party':d.get('siglaPartido'),'state':d.get('siglaUf'),'uri':d.get('uri')})
    return props,deps,evidence,timeline
def load_transparencia():
    expenses=[]; agencies=[]; beneficiaries=[]; evidence=[]; timeline=[]
    tr=RAW/'transparencia'
    if tr.exists():
        for path in tr.glob('expenses_*.json'):
            payload=read_json(path)
            for r in payload.get('records',[]):
                rid=r.get('id'); mock=payload.get('mock',False); exp={'id':rid,'source':'transparencia','mock':mock,'year':r.get('year'),'agency':r.get('agency'),'program':r.get('program'),'amount_brl':r.get('amount_brl'),'beneficiary':r.get('beneficiary'),'region':r.get('region'),'link_classification':r.get('link_classification','same_theme_link')}; expenses.append(exp); agencies.append({'id':slug(r.get('agency')),'name':r.get('agency'),'mock':mock}); beneficiaries.append({'id':slug(r.get('beneficiary')),'name':r.get('beneficiary'),'region':r.get('region'),'mock':mock}); eid=f'transparencia-expense-{rid}'; evidence.append({'id':eid,'source_type':'spending_record','source_id':rid,'title':f"{r.get('program')} — {r.get('beneficiary')}",'date':str(r.get('year')),'excerpt':f"{r.get('agency')} / {r.get('program')} / R$ {r.get('amount_brl')} / {r.get('beneficiary')}",'location':'Mock transparency sample cache' if mock else 'Portal da Transparência sample cache','url':None,'metadata':{'mock':mock,'link_classification':exp['link_classification']}}); timeline.append({'date':str(r.get('year')),'title':f"Spending signal: {r.get('program')}",'description':f"{r.get('agency')} recorded R$ {r.get('amount_brl')} for {r.get('beneficiary')}",'evidence_id':eid,'event_type':'public_spending'})
    return expenses,agencies,beneficiaries,evidence,timeline
def create_db(outputs):
    db=OUT/'money_trail.sqlite'; db.unlink(missing_ok=True); con=sqlite3.connect(db)
    for name, rows in outputs.items():
        if not rows: continue
        keys=sorted({k for r in rows for k in r.keys()}); con.execute(f'CREATE TABLE {name} ({", ".join(k+" TEXT" for k in keys)})')
        for r in rows: con.execute(f'INSERT INTO {name} ({", ".join(keys)}) VALUES ({", ".join("?" for _ in keys)})', [json.dumps(r.get(k), ensure_ascii=False) if isinstance(r.get(k),(dict,list,bool)) else r.get(k) for k in keys])
    con.commit(); con.close()
def main():
    OUT.mkdir(parents=True, exist_ok=True); props,deps,ev1,tl1=load_camara(); exps,ags,bens,ev2,tl2=load_transparencia(); evidence=ev1+ev2; timeline=sorted(tl1+tl2,key=lambda x:x.get('date') or '')
    candidate_links=[{'from_id':p['id'],'to_id':e['id'],'from_type':'proposition','to_type':'expense','link_classification':'same_theme_link','rationale':'Same theme/time-window only; not causal evidence.'} for p in props[:20] for e in exps[:20]]
    outputs={'propositions':props,'votes':[],'deputies':deps,'agencies':ags,'expenses':exps,'suppliers_or_beneficiaries':bens,'timeline_events':timeline,'candidate_links':candidate_links,'evidence_index':evidence}
    for name, rows in outputs.items(): write_jsonl(OUT/f'{name}.jsonl', rows)
    stats={'task_id':TASK_ID,'created_at':datetime.utcnow().isoformat()+'Z','counts':{k:len(v) for k,v in outputs.items()},'mock_transparency_data':any(e.get('mock') for e in exps),'warning':'Candidate links are hypotheses unless direct_documented_link.'}; write_json(OUT/'dataset_stats.json', stats); create_db(outputs); print('Prepared', stats)
if __name__=='__main__': main()
