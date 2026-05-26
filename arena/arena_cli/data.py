from __future__ import annotations
from pathlib import Path
import subprocess, sys
from .utils import repo_root

def discover_task_script(task_id: str, script_name: str) -> Path:
    p=repo_root()/'tasks'/task_id/'scripts'/f'{script_name}.py'
    if not p.exists(): raise FileNotFoundError(f'No {script_name}.py for {task_id}')
    return p

def _run(script: Path, args: list[str]):
    cmd=[sys.executable, str(script), *args]
    print('Running', ' '.join(cmd))
    raise SystemExit(subprocess.call(cmd, cwd=repo_root()))

def download_task_data(task_id: str, sample=False):
    _run(discover_task_script(task_id, 'download'), ['--sample-only'] if sample else [])

def prepare_task_data(task_id: str):
    _run(discover_task_script(task_id, 'prepare'), [])
