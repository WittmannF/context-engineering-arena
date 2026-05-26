# Brazil Public Money Trail

**Page concept:** “Follow the policy-to-money trail.”

**Benchmark question:** Trace one Brazilian public policy theme from legislative activity to federal public spending. What can be verified, which actors and agencies appear, what changed over time, and what questions remain open?

This task asks participants to connect public legislative activity to public spending without pretending that correlation proves causation. It should feel like civic data journalism powered by context engineering.

## Sources

- [Câmara dos Deputados Dados Abertos](https://dadosabertos.camara.leg.br/) — deputies, propositions, votes, tramitações, events, committees, themes and keywords.
- [Portal da Transparência API de Dados](https://portaldatransparencia.gov.br/api-de-dados) — federal spending, agencies, programs, beneficiaries, contracts/transfers/amendments where available. Real API calls require `TRANSPARENCIA_API_TOKEN`.
- [TCU Dados Abertos / Webservices](https://sites.tcu.gov.br/dados-abertos/) — optional enrichment for oversight, supplier, certification, and accountability signals.

## Suggested themes

health, education, environment, infrastructure, agriculture, public security, social assistance, science and technology.

## Required page sections

1. Executive Summary
2. Policy Theme and Scope
3. Legislative Activity Timeline
4. Public Spending Timeline
5. Actor and Institution Map
6. Money Flow Overview
7. Evidence-backed Claims
8. Direct Links vs Hypotheses
9. Red Flags and Accountability Questions
10. What Could Not Be Verified
11. Recommended Next Investigations
12. Context Engineering Strategy
13. Data and Ethics Limitations

## Visual affordances

- policy-to-money timeline
- actor → institution → program → spending graph placeholder
- map of Brazil placeholder when regional data is available
- spending breakdown cards
- claim/evidence table
- direct-vs-hypothetical link badges
- uncertainty panel
- “what is fact vs inference” section
- Context X-Ray panel

## Expected answer behavior

Submissions must distinguish verified facts, directly documented links, plausible analytical links, weak signals, and unsupported speculation. The page must not assert corruption, illegal conduct, or improper influence unless directly supported by authoritative evidence.

## Local commands

```bash
python -m arena_cli.cli download-data --task task-002-brazil-public-money-trail --sample
python -m arena_cli.cli prepare-data --task task-002-brazil-public-money-trail
```

Direct examples:

```bash
python tasks/task-002-brazil-public-money-trail/scripts/download.py --sample-only
python tasks/task-002-brazil-public-money-trail/scripts/download.py --theme health --year-start 2022 --year-end 2024
python tasks/task-002-brazil-public-money-trail/scripts/download.py --theme education --skip-transparencia
```

If `TRANSPARENCIA_API_TOKEN` is missing, sample mode creates a clearly marked mock transparency fixture for UI and schema testing only. It must not be used for official scoring.
