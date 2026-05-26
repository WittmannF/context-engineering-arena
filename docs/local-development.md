# Local Development

Run `./scripts/bootstrap.sh`, then `python -m arena_cli.cli validate`, `python -m arena_cli.cli build-catalog`, and `cd packages/site && npm run dev`. Data scripts write under ignored `data/` folders. The public site is static and requires no backend.
