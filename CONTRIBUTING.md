# Contributing

Thanks for improving Context Engineering Arena. You can contribute tasks, submissions, scoring code, docs, or UI improvements.

## Before opening a PR

1. Run `./scripts/bootstrap.sh` once.
2. Run `python -m arena_cli.cli validate`.
3. Run `python -m arena_cli.cli build-catalog`.
4. Run `cd packages/site && npm run build`.
5. Confirm you did not commit raw datasets or secrets.

## Submission PRs

Place files under `submissions/<participant-id>/<task-id>/` and include `answer.json`, `context_trace.json`, and `strategy.md`. Every major claim should cite evidence.

## Task PRs

Add a folder under `tasks/`, include `task.yaml`, `data_manifest.yaml`, `rubric.md`, `expected_answer_schema.json`, scripts, sample mode, and ethics notes.
