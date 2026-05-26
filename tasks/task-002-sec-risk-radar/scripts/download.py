import argparse, json, os, time, urllib.request
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--ticker', default='AAPL'); parser.add_argument('--sample-only', action='store_true'); parser.add_argument('--force', action='store_true'); args=parser.parse_args()
ua=os.getenv('SEC_USER_AGENT')
if not ua: raise SystemExit('Set SEC_USER_AGENT="ContextEngineeringArena/0.1 your-email@example.com"')
root=Path(__file__).resolve().parents[3]; out=root/'data/raw/task-002-sec-risk-radar'/args.ticker.upper(); out.mkdir(parents=True, exist_ok=True)
req=urllib.request.Request('https://www.sec.gov/files/company_tickers.json', headers={'User-Agent':ua})
tickers=json.loads(urllib.request.urlopen(req, timeout=30).read())
match=next(v for v in tickers.values() if v['ticker'].upper()==args.ticker.upper()); cik=str(match['cik_str']).zfill(10)
url=f'https://data.sec.gov/submissions/CIK{cik}.json'; req=urllib.request.Request(url, headers={'User-Agent':ua})
(out/'submissions.json').write_bytes(urllib.request.urlopen(req, timeout=30).read()); print('Downloaded metadata for', args.ticker, cik)
time.sleep(0.2)
