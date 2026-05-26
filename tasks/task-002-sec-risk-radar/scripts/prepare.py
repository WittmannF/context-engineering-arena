from pathlib import Path
import json, csv
root=Path(__file__).resolve().parents[3]; raw=root/'data/raw/task-002-sec-risk-radar'; out=root/'data/processed/task-002-sec-risk-radar'; out.mkdir(parents=True, exist_ok=True)
rows=[]
for f in raw.rglob('submissions.json'):
    data=json.loads(f.read_text()); recent=data.get('filings',{}).get('recent',{})
    for i, form in enumerate(recent.get('form',[])[:20]): rows.append({'ticker':f.parent.name,'form':form,'filing_date':recent.get('filingDate',[''])[i],'accession':recent.get('accessionNumber',[''])[i],'primary_doc':recent.get('primaryDocument',[''])[i]})
if not rows: rows=[{'ticker':'SAMPLE','form':'10-K','filing_date':'2024-01-01','accession':'sample','primary_doc':'sample.htm'}]
with (out/'filings.csv').open('w', newline='', encoding='utf-8') as fh: writer=csv.DictWriter(fh, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
(out/'manifest.json').write_text(json.dumps({'filings':rows}, indent=2), encoding='utf-8'); print('Prepared', len(rows), 'filings')
