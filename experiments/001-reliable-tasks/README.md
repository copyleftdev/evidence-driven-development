# Reliable tasks across fresh processes

**Supported within the declared local scope by the corrected second run.** The SQLite candidate passed five scenarios
in both independent repetitions. The volatile control failed persistence and retry claims;
the duplicate-accepting control preserved tasks but failed retry and conflict claims.
The gate rejected an otherwise-positive report with zero exercised scenarios.

| Run | Result | Scope |
|---|---|---|
| [20261010T042154Z-926973ba](runs/20261010T042154Z-926973ba/summary.json) | Excluded from final gate claim | Initial gate did not reject unrelated control failures; raw observations retained |
| [20261010T042729Z-633b0705](runs/20261010T042729Z-633b0705/summary.json) | Corrected gate passed | Control failure reasons and nonzero counts verified; three variants, two repetitions each |
| [20261010T042935Z-a7cca3e6](runs/20261010T042935Z-a7cca3e6/summary.json) | Portable-copy gate passed | Fresh copy, cleared environment, standard system Python; same corrected source |

Each SQLite repetition exercised three restart rounds, one ignored-response retry,
eight concurrent submissions, one conflicting reuse and one invalid-input case.
The concurrent scenario initializes the schema first. Trace order can vary; repeated
claims and exercise counts are the deterministic comparison, not scheduling order.

`manifest.json` identifies application, harness and hypothesis hashes and Python/SQLite
versions. Per-variant JSON files retain each command's safe synthetic inputs, exit code,
response, scenario results and failures. The two broken implementations are intentional
controls, not discovered production defects.

Run `python3 scripts/prove.py` from the project root to add a new result. A zero exit status
requires all declared checks; it does not overwrite or automatically promote old evidence.

## Limits

All boundaries are local CLI process boundaries with SQLite-backed files. Ignoring a
successful response is not a network-disconnection or process-kill test. We did not test
power loss, corruption, interrupted commits, network filesystems, performance or model
reliability. Source hashes identify inputs but do not provide independent attestation.

## Harness correction

The initial run observed the expected defects, but its gate was too permissive about why
a broken control failed. Source review found this gap; three harness regression tests now
reject zero activity and unrelated failure reasons. The second run supersedes the first
gate verdict. No original artifact was changed or deleted.
