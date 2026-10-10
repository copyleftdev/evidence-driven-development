# Tiny Tasks working agreement

Keep this educational project small and reproducible. Read the experiment contract in
`experiments/001-reliable-tasks/experiment.json` before changing claimed behavior.

- Runtime code and the experiment use Python's standard library; no network or API key is needed.
- State claims and disconfirming observations before implementing an architectural change.
- Preserve old runs. Each execution writes a fresh timestamped directory.
- A test harness must reject a targeted broken example and refuse an unexercised scenario.
- Keep application code separate from `lab/` controls. Do not relax checks to accept a defect.
- Use synthetic task titles. Do not add private context, credentials or unrelated project material.
- Keep source hashes and Python/SQLite versions with results; hashes are not attestations.
- Report observed results and untested scope separately. Never present a model's review as proof.
- Run `python3 -m unittest discover -s tests -v` and `python3 scripts/prove.py` for behavior changes.
- For writing-only changes, check citations, commands and consistency with saved results.
- Keep the article's `published: false`. Commit, publish or upload only when requested.

The article explains the workflow. `docs/plan.md` records task state and
`docs/decisions.md` records decisions. Do not duplicate these into a growing memory file.
