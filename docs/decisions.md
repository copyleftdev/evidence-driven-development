# Decisions

## Local application and deterministic observations

Use a task list with only add/list commands so the development method remains visible.
Python's standard library keeps the runnable example accessible and independent of a
model vendor. The application itself has no LLM.

## Persistent request identity

Bind a request ID to one normalized title and one stored task. Trim surrounding title
whitespace before comparison. Different request IDs can legitimately create equal titles.
A conflicting reuse is an error; it must not overwrite the original task.

## Evidence before promotion

The pre-implementation contract declares the workloads and failure conditions. The run
`20261010T042729Z-633b0705` supports the SQLite implementation within the documented local
scope. Both deliberately broken implementations fail their targeted claims; zero exercise
counts fail the gate. No performance or hardware-failure claim is promoted.

## Publication boundary

Use original code, synthetic tasks, newly generated evidence and primary-source citations.
The author authorized the public companion repository and gist assets on `copyleftdev`.
The DEV.to article remains an unpublished draft. A distribution license and any author
biography remain editorial choices; no license has been inferred from the account name.

## Validate the reason a negative control failed

Review identified that the first gate could accept an unrelated child-process failure as
evidence that a deliberate defect was detected. Require nonzero counts for controls and
the targeted assertion reason, with regression tests. Retain the first run, excluded
from the stronger gate claim; its observed application results are not rewritten.

## Stable article references and embeddable mirrors

Host all teaching assets in the companion repository. Pin cover, source and evidence links
to the initial source commit; keep gists as exact mirrors of the two referenced files.
The DEV draft uses the supported universal embed syntax, with pinned source links as a
fallback. The local reading copy renders source snapshots without third-party scripts;
it is an editorial preview, not a claim that DEV rendered the embeds.
