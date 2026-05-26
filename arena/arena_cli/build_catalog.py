from __future__ import annotations
from pathlib import Path
from .utils import repo_root, read_yaml, read_json, write_json
from .validate import validate_all

SITE_DATA = Path('packages/site/src/data/generated')

def load_tasks():
    root=repo_root(); tasks=[]
    for d in sorted((root/'tasks').glob('task-*')):
        t=read_yaml(d/'task.yaml'); t['path']=str(d.relative_to(root)); tasks.append(t)
    return tasks

def load_submissions():
    root=repo_root(); submissions=[]
    for participant_dir in sorted((root/'submissions').glob('*')):
        if not participant_dir.is_dir(): continue
        participant=read_yaml(participant_dir/'participant.yaml') if (participant_dir/'participant.yaml').exists() else {'id': participant_dir.name, 'display_name': participant_dir.name}
        for subdir in sorted(participant_dir.glob('task-*')):
            if not subdir.is_dir(): continue
            item={'participant': participant, 'participant_id': participant.get('id', participant_dir.name), 'task_id': subdir.name, 'path': str(subdir.relative_to(root))}
            for name in ['answer','context_trace','score']:
                p=subdir/f'{name}.json'
                if p.exists(): item[name]=read_json(p)
            sp=subdir/'strategy.md'
            item['strategy_md']=sp.read_text(encoding='utf-8') if sp.exists() else ''
            submissions.append(item)
    return submissions

def build_leaderboard(tasks, submissions):
    boards=[]
    for t in tasks:
        entries=[]
        for s in submissions:
            if s['task_id'] != t['id']: continue
            score=s.get('score', {})
            entries.append({'task_id': t['id'], 'participant_id': s['participant_id'], 'participant_name': s['participant'].get('display_name', s['participant_id']), 'overall_score': score.get('overall_score'), 'scores': score.get('scores', {}), 'scored_by': score.get('scored_by'), 'notes': score.get('notes', '')})
        entries.sort(key=lambda e: (e['overall_score'] is None, -(e['overall_score'] or 0)))
        for i,e in enumerate(entries,1): e['rank']=i
        boards.append({'task_id': t['id'], 'entries': entries})
    return boards

def write_site_data():
    report=validate_all()
    if not report.ok:
        report.print(); raise SystemExit(1)
    root=repo_root(); out=root/SITE_DATA
    tasks=load_tasks(); submissions=load_submissions(); leaderboard=build_leaderboard(tasks, submissions)
    write_json(out/'tasks.json', tasks)
    write_json(out/'submissions.json', submissions)
    write_json(out/'leaderboard.json', leaderboard)
    print(f'Wrote {out}: {len(tasks)} tasks, {len(submissions)} submissions')
