# Game Stats — Agent Instructions

Scope: `illia-yehorov/public-personal-lab/game-stats/` only.
These instructions do **not** authorize direct commits for other folders or repositories.

## Source and refresh
- The private Google Doc "Рубилово" is the source of truth; read it through the connected Google Drive plugin.
- Only update when the user explicitly requests a statistics refresh. Never set up background synchronization.
- Compare all source rows with `game-stats/games.csv` and `game-stats/README.md`. Preserve existing IDs, avoid duplicates, validate counts, winner, game type, date, clock rules, and public notes.
- If the source is ambiguous or incompatible with the schema, do not invent values. Ask for clarification before publishing unverified statistics.

## GitHub workflow and authorization
- **Routine verified game data updates** that only change `game-stats/games.csv` (and optionally its existing statistics documentation within `game-stats/`) may commit directly to `main`, with **one commit per user-requested iteration**, and **no Pull Request**. The user has already authorized this; do not ask again.
- User explicitly permits committing verified, user-requested UI changes *entirely within* `game-stats/` directly to `main` in one commit without a Pull Request. For changes to schema, validation, deployment, or substantial frontend redesign beyond this explicitly authorized directory, follow the repository rule: use a feature branch and Pull Request. If the user requested the change and all relevant CI checks pass, **merge the Pull Request yourself**, preferably with squash merge, without asking the user for a manual GitHub action.
- Never merge when checks fail or when game data are unverified; report the blocker. Do not force-push or rewrite shared history.
- Do **not** apply the direct-`main` exception outside this folder, including `.github/` or any other repository.

## Site and data timestamp
- `index.html` and `chess.html` both load `games.csv` and calculate statistics dynamically.
- The GitHub Pages deployment inserts the last **CSV commit timestamp** (not the page-view time) into both HTML pages. Show this as `CSV обновлён` in the `Europe/Kyiv` timezone only for automatically loaded deployment data.
- Also show the latest result date from the CSV and the time the browser loaded the file. Never conflate those times.
- Keep the published site static, without a separate backend or scheduled source-sync job.

## Dedicated game views
- Overall dashboard: `index.html`; it includes all game records, **including old chess Three-check games**.
- Chess-specific views and summary panels must use `game=chess AND variant=standard` only. Historical `three_check` remains unchanged in CSV and visible in overall statistics, but never enters the current chess duel, chess timers, or chess detail timeline.
- Checkers-specific view is `index.html?view=checkers`, using the same deployed HTML/CSV; this avoids modifying the deployment workflow outside the authorized folder. Include every checkers variant in checkers-only views.
- On the overview page, both checkers and current-chess summary cards are independent of global filters; dedicated views respond to their own filters.
