# Evidence-Driven Development: Tiny Tasks

A standalone companion project for **Evidence-Driven Development: Give Your Coding Agent
Something to Prove**. A tiny local task list teaches explicit claims, negative controls,
fresh-process experiments, nonzero exercise gates and reproducible evidence.

![Evidence-Driven Development: Give your coding agent something to prove.](article/cover-particles-v3.png)

## Run

Requires Python 3.10+ with its standard SQLite module. No application dependencies,
API keys, model account, network service or cloud resources are required.

```sh
git clone https://github.com/copyleftdev/evidence-driven-development.git
cd evidence-driven-development
python3 -m tiny_tasks add "Water plants" --request-id plant-1
python3 -m tiny_tasks add "Water plants" --request-id plant-1
python3 -m tiny_tasks list
python3 -m unittest discover -s tests -v
python3 scripts/prove.py
```

The second create returns the original task with `created: false`. Use a new request ID
for a genuinely new action. Titles are compared after trimming surrounding whitespace.
Default data: `.local/tasks.sqlite`; set a different file using `--db PATH` before the
`add` or `list` subcommand. Conflicting request reuse and invalid input return JSON errors
with exit status 2. A successful command returns exit status 0.

## Read

- [DEV.to article draft](article/devto.md)
- [Styled local reading copy](article/preview.html)
- [Research and terminology](article/research.md)
- [Experiment and actual results](experiments/001-reliable-tasks/README.md)
- [Publishing handoff](article/PUBLISHING.md)
- [Agent instructions](AGENTS.md) and [working plan](docs/plan.md)

The experiment runner always creates a new run directory. It never edits old evidence.
Its overall exit status is 0 only if the real candidate passes, both bad controls fail
their targeted claims, repeated scenario outcomes/counts agree and zero activity is refused.
Subprocess trace ordering may differ under concurrency; no latency claim is made.

## Boundaries

This is an educational local application with two commands. It has no authentication,
multi-user service, deletion, editing or runtime LLM. The experiment tests process-boundary
persistence and request retries; it does not establish power-loss survival, storage-fault
tolerance, scalability, security or comparative model quality.

All example data and captured results were created specifically for this project.
The `lab/` implementations are deliberately broken controls and never used by the normal CLI.
The companion source and assets are public on GitHub; the DEV.to article remains an unpublished draft.
No distribution license has been selected. Public availability does not supply a reuse license.
See [the asset index](article/assets.json) for the cover, gist mirrors and commit-pinned source links.
