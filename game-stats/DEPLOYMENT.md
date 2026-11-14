# Public Personal Lab: GitHub Pages deployment

This repository hosts two independent static sites under a single GitHub Pages deployment:

- [Game statistics](https://illia-yehorov.github.io/public-personal-lab/game-stats/) from `game-stats/`
- [Chess Mixes](https://illia-yehorov.github.io/public-personal-lab/chess-mixes/) from `chess-mixes/`

GitHub Actions validates the game statistics and publishes both folders. It does **not** access Google Docs, generate statistics or generate chess puzzles. The Chess Mixes site is built locally in the separate `chess-mixes` repository and pushed here using a write-enabled, repository-scoped SSH deploy key.

## One-time setup

1. In this repository open **Settings → Pages**.
2. Under **Build and deployment**, select **Source: GitHub Actions**.
3. Merge the setup PR into main. A push to main runs the workflow in .github/workflows/deploy.yml. You can also run it manually from the **Actions** tab, selecting main.
4. Check the workflow's validate and deploy jobs. The final URL is shown in the deployment result and **Settings → Pages**. Expected site path: https://illia-yehorov.github.io/public-personal-lab/game-stats/ (confirm after the first successful deployment).

If the github-pages environment has deployment branch rules, ensure main is allowed. No custom domain, repository secrets, backend, database, or build tooling is required for the website.

## What triggers the workflow

- A pull request to main that changes game statistics, `chess-mixes/**`, the validator or workflow: **validate only** (no public deployment).
- A push to main that changes one of those paths: **validate, then deploy both sites**.
- A manual run on main: **validate, then deploy**.

The validation checks that HTML exists and the CSV matches the dashboard schema, with valid IDs, dates, games, winners, clock fields and counts. It is not a substitute for checking new entries against the private source document.

The deployment copies `game-stats/index.html`, `game-stats/chess.html`, and `game-stats/games.csv` to the Pages artifact, and copies the entire `chess-mixes/` folder when it exists. The latter is optional during migration, so deploying statistics continues to work before the first chess publication. Both sites are always included in each deploy, regardless of which folder triggered it.

The local Chess Mixes publisher owns **only** the `chess-mixes/` directory. It does not modify `game-stats/` or this workflow. It pushes directly to `main` using an SSH deploy key registered on this public repository; no GitHub Actions secret is needed here. A commit under `chess-mixes/` triggers this workflow automatically.

Do not put sensitive data in either public site. The game statistics `source_entry` and `notes` CSV fields are public.

## Routine statistics updates

The private Google Docs document remains the source of truth. Game statistics are refreshed by the separately configured scheduled task or on an explicit user request. The updater reads the source and game-stats/README.md, compares with the existing CSV, retains IDs, avoids duplicates, and validates results. If there are no changes, there is no commit.

For **this repository only**, a validated routine update may use one direct commit to main, without a PR. This setup change uses one commit and a PR. All other repositories retain the branch-and-PR policy. GitHub Actions never updates CSV by itself.
