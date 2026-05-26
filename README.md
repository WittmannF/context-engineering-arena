# Context Engineering Arena

**Build the clearest page from the messiest context.**

Context Engineering Arena is an open benchmark where developers compete to turn huge, noisy, fragmented datasets into clear, visual, evidence-backed pages. It compares not only the final answer, but also the context engineering strategy used to assemble, retrieve, compress, isolate, cite, and inspect context.

## What this is

A production-ready starter monorepo for a public benchmark/gallery:

- maintainers add **tasks** with corpora, benchmark questions, schemas, rubrics, and data scripts;
- participants submit **structured answers** plus **context traces** under `submissions/`;
- validation and catalog generation turn those files into static JSON;
- a Vite + React + Tailwind site renders every submission as an inspectable public page on GitHub Pages.

## Why context engineering needs an arena

The best LLM systems are not just better prompts. They are better context systems: retrieval, compression, memory, citation, graph extraction, summarization, ranking, and careful refusal to overclaim. This arena evaluates the transformation from messy real-world information into useful understanding.

## How it works

1. Pick a task from `tasks/`.
2. Download or sample data using the task scripts.
3. Run any strategy you like: prompt-only, long context, RAG, reranking, multi-agent, graph extraction, human-in-the-loop, or something new.
4. Submit `answer.json`, `context_trace.json`, and `strategy.md`.
5. The site renders your submission into a standardized evidence-backed page and leaderboard entry.

## Quickstart

```bash
git clone https://github.com/your-org/context-engineering-arena.git
cd context-engineering-arena
./scripts/bootstrap.sh
python -m arena_cli.cli validate
python -m arena_cli.cli build-catalog
cd packages/site
npm run dev
```

## Data quickstart

```bash
python -m arena_cli.cli download-data --task task-001-enron-investigation --sample
python -m arena_cli.cli prepare-data --task task-001-enron-investigation
```

SEC downloads require a fair-access user agent:

```bash
export SEC_USER_AGENT="ContextEngineeringArena/0.1 your-email@example.com"
```

## Submission quickstart

```bash
cp -r submissions/baseline-prompt-only submissions/my-team
edit submissions/my-team/participant.yaml
edit submissions/my-team/task-001-enron-investigation/answer.json
edit submissions/my-team/task-001-enron-investigation/context_trace.json
python -m arena_cli.cli validate-submission --participant my-team --task task-001-enron-investigation
python -m arena_cli.cli build-catalog
```

## Included kickstart tasks

- **The Enron Investigation Brief** — corporate email investigation and evidentiary synthesis.
- **SEC Risk Radar** — longitudinal analysis of risk language and filing narratives.
- **Open Source Ecosystem Radar** — GH Archive trend, momentum, and fragility analysis.

## Repository structure

- `.github/` — validation, GitHub Pages deployment, issue and PR templates.
- `arena/` — Python CLI for validation, scoring stubs, data script dispatch, and catalog generation.
- `docs/` — philosophy, scoring, task authoring, submissions, data policy, ethics, local development.
- `packages/site/` — static React site.
- `schemas/` — JSON schemas for tasks, submissions, traces, scores, and data manifests.
- `tasks/` — benchmark definitions and data pipelines.
- `submissions/` — participant folders.
- `data/` — ignored local raw/processed data plus small legal samples.

## Scoring overview

MVP scoring is manual or placeholder via `score.json`. The architecture supports future automatic metrics: claim accuracy against hidden labels, evidence precision/recall, hallucination detection, contradiction detection, cost-adjusted score, and human usefulness score.

## Data policy

Do not commit large raw datasets. Tasks include scripts and manifests for reproducible local download, sampling, indexing, and preparation. Small processed samples may be committed only when legally safe.

## Ethics and safety

Submissions must distinguish directly supported facts from interpretations, weak signals, and speculation. Avoid defamatory claims, fabricated evidence, privacy violations, and unsafe medical/legal/financial overclaims.

## Roadmap

- richer automatic scoring and hidden gold labels;
- React Flow / D3 evidence maps;
- artifact previews and reproducible run logs;
- LLM-as-judge experiments with transparent judge traces;
- task marketplace and maintainer dashboards.
