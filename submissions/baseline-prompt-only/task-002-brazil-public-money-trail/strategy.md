# Baseline Prompt Only for Brazil Public Money Trail

This weak baseline is designed to make the task visible in the arena, not to be competitive.

It uses a tiny sample and task metadata to produce a conservative civic brief. It explicitly avoids claims of corruption, influence, or causality. The baseline is useful because it shows the expected structure: policy scope, legislative and spending timelines, actor/institution mapping, claim/evidence tables, direct-vs-hypothetical link framing, and limitations.

## What it tried

- Identify official data sources.
- State a default theme: health.
- Explain how legislative records and spending records could be connected.
- Mark missing evidence and unresolved questions.

## What it did not do

- It did not run robust entity resolution.
- It did not perform deterministic joins across all official APIs.
- It did not verify contracts, beneficiaries, or fiscalization data.
- It did not prove a causal path from a bill to a spending record.

## Why this baseline is weak

Public accountability requires careful joins, source-specific coverage checks, and human review. A prompt-only strategy can write a readable summary, but it cannot safely establish a policy-to-money trail without structured data preparation.
