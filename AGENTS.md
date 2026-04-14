# AGENTS Notes

- Use `bash playwright.sh ...` instead of calling `playwright-cli` directly. The wrapper relocates Playwright cache and browser paths into the repo at `.cache/` and `.playwright-browsers/`. `./playwright.sh` may also work in normal shells, but `bash playwright.sh ...` is the safer form from the agent environment.
- Browser checks still need the docs site to be served over localhost. Start it with `./run.sh`, or allow a one-time approval to start a local HTTP server from the agent.
- For this repo, `./run.sh` serves `docs/` on `http://127.0.0.1:8080`.
