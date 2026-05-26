from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

Confidence = Literal['high','medium','low']

class Task(BaseModel):
    id: str
    title: str
    short_description: str
    long_description: str = ''
    benchmark_question: str
    domain: str = 'general'
    difficulty: str = 'medium'
    corpus_size: str = 'unknown'
    tags: list[str] = []
    dataset: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    scoring: dict[str, Any] = {}
    safety: dict[str, Any] = {}

class DataManifest(BaseModel):
    task_id: str
    sources: list[dict[str, Any]]
    license: str = ''
    expected_size: str = ''
    sample_mode: dict[str, Any] = {}
    pipeline: list[str] = []
    ethics: list[str] = []

class Participant(BaseModel):
    id: str
    display_name: str
    type: str = 'participant'
    website: str | None = None
    github: str | None = None
    description: str = ''
    contact: str | None = None

class Evidence(BaseModel):
    id: str
    source_type: str
    source_id: str = ''
    title: str = ''
    date: str | None = None
    excerpt: str = ''
    location: str | None = None
    url: str | None = None
    metadata: dict[str, Any] = {}

class Claim(BaseModel):
    id: str
    claim: str
    claim_type: Literal['fact','interpretation','recommendation','uncertainty']
    confidence: Confidence
    evidence_ids: list[str] = []
    notes: str = ''

class TimelineItem(BaseModel):
    date: str
    title: str
    description: str = ''
    evidence_ids: list[str] = []

class Entity(BaseModel):
    id: str
    name: str
    type: str = 'other'
    description: str = ''
    evidence_ids: list[str] = []

class Risk(BaseModel):
    id: str
    title: str
    severity: Confidence
    likelihood: Confidence
    description: str = ''
    evidence_ids: list[str] = []

class Recommendation(BaseModel):
    id: str
    title: str
    priority: Confidence
    description: str = ''
    rationale: str = ''
    evidence_ids: list[str] = []

class Answer(BaseModel):
    task_id: str
    participant_id: str
    title: str
    executive_summary: str
    sections: list[dict[str, Any]] = []
    claims: list[Claim] = []
    evidence: list[Evidence] = []
    timeline: list[TimelineItem] = []
    entities: list[Entity] = []
    risks: list[Risk] = []
    uncertainties: list[dict[str, Any]] = []
    recommendations: list[Recommendation] = []
    limitations: list[str] = []

class ContextTrace(BaseModel):
    task_id: str
    participant_id: str
    strategy_name: str
    strategy_summary: str
    methods: dict[str, bool]
    models: list[dict[str, Any]] = []
    context_stats: dict[str, float | int] = {}
    retrieval_trace: list[dict[str, Any]] = []
    compression_trace: list[dict[str, Any]] = []
    what_was_ignored: list[dict[str, Any]] = []
    known_failure_modes: list[str] = []

class Score(BaseModel):
    task_id: str
    participant_id: str
    overall_score: float | None = None
    scores: dict[str, float] = {}
    notes: str = ''
    scored_by: Literal['manual','auto','llm_judge','hybrid'] = 'manual'
    scored_at: str | None = None
