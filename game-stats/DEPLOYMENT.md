# Game statistics: GitHub Pages deployment

The public website is a static copy of index.html and games.csv. GitHub Actions only validates and deploys these files. It does **not** access Google Docs or generate statistics.

## One-time setup

1. In this repository open **Settings → Pages**.
2. Under **Build and deployment**, select **Source: GitHub Actions**.
3. Merge the setup PR into main. A push to main runs the workflow in .github/workflows/deploy.yml. You can also run it manually from the **Actions** tab, selecting main.
4. Check the workflow's validate and deploy jobs. The final URL is shown in the deployment result and **Settings → Pages**. Expected site path: https://illia-yehorov.github.io/public-personal-lab/game-stats/ (confirm after the first successful deployment).

If the github-pages environment has deployment branch rules, ensure main is allowed. No custom domain, repository secrets, backend, database, or build tooling is required for the website.

## What triggers the workflow

- A pull request to main that changes the HTML, CSV, validator or workflow: **validate only** (no public deployment).
- A push to main that changes one of those files: **validate, then deploy**.
- A manual run on main: **validate, then deploy**.

The validation checks that HTML exists and the CSV matches the dashboard schema, with valid IDs, dates, games, winners, clock fields and counts. It is not a substitute for checking new entries against the private source document.

Only game-stats/index.html and game-stats/games.csv are copied to the Pages artifact. Do not put sensitive data into either public file; source_entry and notes in CSV are also public.

## Routine statistics updates

The private Google Docs document remains the source of truth. Only after the explicit request **«Обнови игровую статистику»**, ChatGPT should read it along with game-stats/README.md, compare with the existing CSV, retain IDs, avoid duplicates, verify results and clarify ambiguous entries. If there are no changes, there is no commit.

For **this repository only**, a validated routine update may use one direct commit to main, without a PR. This setup change uses one commit and a PR. All other repositories retain the branch-and-PR policy. GitHub Actions never updates CSV by itself.
