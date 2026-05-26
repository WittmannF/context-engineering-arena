from __future__ import annotations
import argparse
from .utils import repo_root
from .validate import validate_all, validate_submission
from .build_catalog import write_site_data, load_tasks, load_submissions
from .data import download_task_data, prepare_task_data

def main(argv=None):
    p=argparse.ArgumentParser(prog='arena')
    sub=p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('validate')
    sub.add_parser('build-catalog')
    sub.add_parser('list-tasks')
    sub.add_parser('list-submissions')
    vs=sub.add_parser('validate-submission'); vs.add_argument('--participant', required=True); vs.add_argument('--task', required=True)
    dd=sub.add_parser('download-data'); dd.add_argument('--task', required=True); dd.add_argument('--sample', action='store_true')
    pd=sub.add_parser('prepare-data'); pd.add_argument('--task', required=True)
    a=p.parse_args(argv)
    if a.cmd=='validate':
        r=validate_all(); r.print(); raise SystemExit(0 if r.ok else 1)
    if a.cmd=='build-catalog': write_site_data(); return
    if a.cmd=='list-tasks':
        for t in load_tasks(): print(f"{t['id']}	{t['title']}")
    if a.cmd=='list-submissions':
        for s in load_submissions(): print(f"{s['participant_id']}	{s['task_id']}")
    if a.cmd=='validate-submission':
        r=validate_submission(repo_root()/'submissions'/a.participant/a.task); r.print(); raise SystemExit(0 if r.ok else 1)
    if a.cmd=='download-data': download_task_data(a.task, a.sample)
    if a.cmd=='prepare-data': prepare_task_data(a.task)

if __name__ == '__main__': main()
