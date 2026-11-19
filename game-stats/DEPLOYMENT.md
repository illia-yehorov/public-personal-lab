# Public Personal Lab: GitHub Pages deployment

This repository publishes the [Game Statistics dashboard](https://illia-yehorov.github.io/public-personal-lab/game-stats/) from `game-stats/` through GitHub Pages.

GitHub Actions validates game statistics and publishes the static site. It does **not** access Google Docs or generate statistics.

## One-time setup

1. In this repository, open **Settings → Pages**.
2. Under **Build and deployment**, select **Source: GitHub Actions**.
3. Merge the setup PR into `main`. A push to `main` runs `.github/workflows/deploy.yml`. You can also run it manually from the **Actions** tab, selecting `main`.
4. Check the workflow's validate and deploy jobs. The final URL is shown in the deployment result and **Settings → Pages**. Expected site path: https://illia-yehorov.github.io/public-personal-lab/game-stats/.

If the `github-pages` environment has deployment branch rules, ensure `main` is allowed. No custom domain, repository secrets, backend, database, or build tooling is required for the website.

## What triggers the workflow

- A pull request to `main` that changes the game statistics HTML/CSV, validator, or workflow: **validate only** (no public deployment).
- A push to `main` that changes one of those paths: **validate, then deploy**.
- A manual run on `main`: **validate, then deploy**.

The validation checks that HTML exists and the CSV matches the dashboard schema, with valid IDs, dates, games, winners, clock fields and counts. It is not a substitute for checking new entries against the private source document.

The deployment copies `game-stats/index.html`, `game-stats/chess.html`, and `game-stats/games.csv` to the Pages artifact. It inserts the latest CSV commit timestamp into both dashboard pages during deployment.

Do not put sensitive data on the public site. The game statistics `source_entry` and `notes` CSV fields are public.

## Routine statistics updates

The private Google Docs document remains the source of truth. Game statistics are refreshed by the separately configured scheduled task or on an explicit user request. The updater reads the source and `game-stats/README.md`, compares with the existing CSV, retains IDs, avoids duplicates, and validates results. If there are no changes, there is no commit.

For **this repository only**, a validated routine data update may use one direct commit to `main`, without a PR. Other changes to the deployment workflow use a feature branch and PR. GitHub Actions never updates CSV by itself.
