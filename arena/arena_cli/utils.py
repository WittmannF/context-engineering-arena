from __future__ import annotations
from pathlib import Path
import json, yaml

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def read_yaml(path: Path):
    with path.open('r', encoding='utf-8') as f: return yaml.safe_load(f) or {}

def read_json(path: Path):
    with path.open('r', encoding='utf-8') as f: return json.load(f)

def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def slug_name(path: Path) -> str: return path.name
