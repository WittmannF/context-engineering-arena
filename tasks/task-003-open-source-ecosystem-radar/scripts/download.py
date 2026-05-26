import argparse, datetime as dt, urllib.request
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--start-date', default='2024-01-01'); p.add_argument('--end-date'); p.add_argument('--hours', type=int, default=2); p.add_argument('--max-files', type=int); p.add_argument('--sample-only', action='store_true'); args=p.parse_args()
root=Path(__file__).resolve().parents[3]; out=root/'data/raw/task-003-open-source-ecosystem-radar'; out.mkdir(parents=True, exist_ok=True)
start=dt.datetime.fromisoformat(args.start_date); n=args.max_files or (2 if args.sample_only else args.hours)
for i in range(n):
    d=start+dt.timedelta(hours=i); url=f'https://data.gharchive.org/{d:%Y-%m-%d}-{d.hour}.json.gz'; target=out/url.rsplit('/',1)[-1]
    if target.exists(): print('Cached', target); continue
    urllib.request.urlretrieve(url, target); print('Downloaded', target)
