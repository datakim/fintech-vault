# Casebook weekly update

This is the runbook for the weekly casebook update (a scheduled cloud run). The casebook page is
`/cases/` on https://www.financialailab.com, built from `src/content/cases/cases.json`.
Read `tools/casebook/BRIEF.md` first: it defines what counts as a case, the five domains, the fixed
method vocabulary, the entry schema and the verification rules. Everything below follows it.

## Steps

1. **Candidates.** Run `python3 tools/casebook/candidates.py --days 21 > /tmp/candidates.json`.
   It lists posts from the RSS feeds in `sources.json` from the last 21 days that are not already in
   `cases.json` or `seen.json`. If most feeds fail with network errors, fetch the feed URLs with
   WebFetch instead and work from those.
2. **Review feed candidates.** Read every candidate title (entries with `"hint": true` first). Open
   (WebFetch) anything that might describe an ML/AI system in one of the five domains, and apply the
   BRIEF rules strictly: first-party, a real system in production or a serious pilot, date confirmed
   on the page, facts only from the post. When unsure, skip it. Entries go live without review.
3. **Pages and search.** For each item in `pages` (blogs without a usable feed), open the index page
   and look for posts from the last 21 days. Then run the `searches` queries (WebSearch, add the
   current month and year) to catch companies outside the list. If you find a first-party blog with a
   working RSS feed that is not in `sources.json`, add it to `feeds`.
4. **Write the batch.** Save accepted entries as a JSON array in `/tmp/new.json` using the BRIEF
   schema. `note_ko` is plain declarative Korean (~다), `note_en` is plain English, both at most 30
   words, no em dashes, no hype. Keep the original post title.
5. **Remember rejections.** Append every candidate you opened and rejected to
   `tools/casebook/seen.json` as `{"url": ..., "date": "<today>", "reason": "<few words>"}` so later
   runs skip it. Do not add candidates you only skimmed by title.
6. **Merge.** `python3 tools/casebook/merge.py src/content/cases/cases.json /tmp/new.json`.
   Read its warnings and fix anything it dropped for a fixable reason.
7. **Check.** Install with `pnpm install --frozen-lockfile` (if pnpm is missing: `corepack enable`
   or `npm i -g pnpm`), then run `pnpm astro check`; it must report 0 errors. Also run
   `pnpm build` if the network allows it (font downloads may be blocked in the sandbox; that alone is
   not a reason to stop).
8. **Publish.** If nothing was added and `seen.json`/`sources.json` did not change, stop without
   committing. Otherwise commit only `src/content/cases/cases.json`, `tools/casebook/seen.json` and
   `tools/casebook/sources.json` (never `git add -A`):
   `git -c user.name=datakim -c user.email=37095012+datakim@users.noreply.github.com commit -m "Casebook: add N posts (YYYY-MM-DD)"`.
   Do not add any Co-Authored-By or "Generated with" lines. Push to `main`; Vercel deploys it.
   If the push to `main` is refused, push the same commit to a branch named
   `casebook/weekly-YYYY-MM-DD` and say so in the final reply.
9. **Report.** Final reply: how many posts were added (title, company, domain each), how many
   candidates were rejected, failed feeds or pages, and whether the push went to `main`.
