from __future__ import annotations
from pathlib import Path
from pydantic import ValidationError
from .schemas import Task, DataManifest, Participant, Answer, ContextTrace, Score
from .utils import repo_root, read_yaml, read_json

VALID_METHODS = {'prompt_only','long_context','rag','hybrid_retrieval','bm25','dense_embeddings','reranking','contextual_retrieval','memory','llm_generated_wiki','multi_agent','summarization','compression','graph_extraction','human_in_the_loop'}

class ValidationReport:
    def __init__(self): self.errors=[]; self.warnings=[]
    def error(self,msg): self.errors.append(msg)
    def warn(self,msg): self.warnings.append(msg)
    @property
    def ok(self): return not self.errors
    def print(self):
        for w in self.warnings: print('WARN:', w)
        for e in self.errors: print('ERROR:', e)
        print(f'Validation: {"PASS" if self.ok else "FAIL"} ({len(self.errors)} errors, {len(self.warnings)} warnings)')

def _load_model(report, model, path, yaml_file=False):
    try:
        data = read_yaml(path) if yaml_file else read_json(path)
        return model.model_validate(data)
    except FileNotFoundError: report.error(f'Missing {path}'); return None
    except (ValidationError, ValueError) as e: report.error(f'{path}: {e}'); return None

def validate_task(task_path: Path, report=None):
    report = report or ValidationReport()
    task = _load_model(report, Task, task_path/'task.yaml', True)
    manifest = _load_model(report, DataManifest, task_path/'data_manifest.yaml', True)
    if task and task.id != task_path.name: report.error(f'{task_path}: task id must match folder name')
    if manifest and task and manifest.task_id != task.id: report.error(f'{task_path}: manifest task_id mismatch')
    for required in ['README.md','rubric.md','expected_answer_schema.json']:
        if not (task_path/required).exists(): report.error(f'Missing {task_path/required}')
    return report

def check_evidence_references(answer: Answer, report: ValidationReport, prefix: str):
    ids = {e.id for e in answer.evidence}
    def check(refs, where):
        for rid in refs:
            if rid not in ids: report.error(f'{prefix}: {where} references missing evidence id {rid}')
    for c in answer.claims: check(c.evidence_ids, f'claim {c.id}')
    for t in answer.timeline: check(t.evidence_ids, f'timeline {t.title}')
    for r in answer.recommendations: check(r.evidence_ids, f'recommendation {r.id}')
    for e in answer.entities: check(e.evidence_ids, f'entity {e.id}')
    for r in answer.risks: check(r.evidence_ids, f'risk {r.id}')

def validate_submission(submission_path: Path, report=None):
    report = report or ValidationReport()
    participant_dir = submission_path.parent
    participant = _load_model(report, Participant, participant_dir/'participant.yaml', True)
    answer = _load_model(report, Answer, submission_path/'answer.json')
    trace = _load_model(report, ContextTrace, submission_path/'context_trace.json')
    if not (submission_path/'strategy.md').exists(): report.error(f'Missing {submission_path}/strategy.md')
    if participant and participant.id != participant_dir.name: report.error(f'{participant_dir}: participant id must match folder')
    if answer:
        if answer.task_id != submission_path.name: report.error(f'{submission_path}: answer task_id mismatch')
        if participant and answer.participant_id != participant.id: report.error(f'{submission_path}: answer participant_id mismatch')
        check_evidence_references(answer, report, str(submission_path))
    if trace:
        if trace.task_id != submission_path.name: report.error(f'{submission_path}: trace task_id mismatch')
        if participant and trace.participant_id != participant.id: report.error(f'{submission_path}: trace participant_id mismatch')
        unknown = set(trace.methods) - VALID_METHODS
        if unknown: report.error(f'{submission_path}: unknown context methods {sorted(unknown)}')
    if (submission_path/'score.json').exists(): _load_model(report, Score, submission_path/'score.json')
    return report

def check_data_files(report):
    root = repo_root(); raw=root/'data/raw'; processed=root/'data/processed'
    for base in [raw, processed]:
        if not base.exists(): continue
        for p in base.rglob('*'):
            if p.is_file() and p.name != '.gitkeep': report.error(f'Raw/processed data file should not be committed: {p.relative_to(root)}')
    ignored_parts = {'.git', '.venv', 'node_modules', 'dist', '__pycache__'}
    for p in root.rglob('*'):
        if p.is_file() and not (ignored_parts & set(p.parts)) and p.stat().st_size > 20_000_000:
            report.warn(f'Large file detected: {p.relative_to(root)}')

def validate_all():
    root = repo_root(); report = ValidationReport()
    for task_path in sorted((root/'tasks').glob('task-*')): validate_task(task_path, report)
    for participant in sorted((root/'submissions').glob('*')):
        if not participant.is_dir(): continue
        for sub in sorted(participant.glob('task-*')):
            if sub.is_dir(): validate_submission(sub, report)
    check_data_files(report)
    return report
