---
title: "Evidence-Driven Development: Give Your Coding Agent Something to Prove"
published: false
description: "Build a tiny task list, break it on purpose, and leave behind evidence another developer can reproduce."
tags: ai, testing, tutorial, python
---

An AI coding agent finishes the feature. The tests pass. The explanation sounds reasonable.

Then someone asks a small question: **“What happens if I run that request again?”**

That question can change the shape of a project. Now “done” needs to mean something observable. The answer needs an experiment, and the experiment needs a way to be wrong.

This tutorial builds a tiny task list around that idea. By the end, you will have a working application, two deliberately broken versions, and a folder of evidence showing which promises each version keeps.

I use **evidence-driven development** to describe this working habit: write down a claim, decide what would disprove it, run the relevant experiment, and let the result govern the next decision.

The coding agent can help at every step. The evidence must remain inspectable without trusting the agent's summary.

## First, some credit for the idea

The name predates coding agents. Jan Bosch's 2017 book, *Speed, Data, and Ecosystems*, includes an Evidence-Driven Development chapter. Its contents connect requirements, hypotheses and experiments. I'm using the term for a practical agent-assisted workflow, without claiming to have invented a methodology. [Publisher's catalog](https://www.routledge.com/Speed-Data-and-Ecosystems-Succeeding-in-a-Software-Centric-World/Bosch/p/book/9781315270685).

There is related work in AI, too. Xia and colleagues describe evaluation-driven development and operations, or EDDOps, as a continuing feedback loop for LLM agents. Their paper addresses a broader agent lifecycle than the small application we will build here. [EDDOps paper](https://arxiv.org/abs/2411.13768).

TDD still gives us a useful red–green–refactor loop. BDD helps express behavior through examples people can discuss. In this tutorial, EDD names the discipline of keeping the claim, execution conditions, observed result and resulting decision connected. Those practices fit together. [TDD](https://agilealliance.org/glossary/tdd/), [Given–When–Then](https://agilealliance.org/glossary/given-when-then/).

## A small application with a real promise

Our app is **Tiny Tasks**. It adds tasks and lists them. Python and SQLite are enough; the application and experiment runner use only the Python standard library. Use Python 3.10 or newer with SQLite support.

The companion project contains the complete source and the evidence runner. From its directory:

```sh
python3 -m tiny_tasks add "Water plants" --request-id plant-1
python3 -m tiny_tasks list
```

The first command returns a task. The second starts a new process and reads it back. The default database lives at `.local/tasks.sqlite`.

The request ID belongs to the user's intended action. When the caller retries that same action, it sends the same ID. A genuinely new task gets a new ID—even if the title happens to match.

That small distinction gives us something worth proving.

## 1. Write a claim that can lose

“Make the task list reliable” leaves too much room for interpretation.

Here is the experiment contract we wrote before implementing the application:

| Claim | A result that disproves it |
|---|---|
| Acknowledged tasks survive a process ending | A new process cannot read the saved task |
| Repeating a create request returns the original task | A retry creates another task or returns a different ID |
| A request ID cannot silently acquire a different meaning | Reusing it with a different title succeeds or changes saved data |
| Invalid input leaves the list alone | An empty title adds a task |

The repository records those claims in `experiments/001-reliable-tasks/experiment.json`. It also declares three restart rounds, eight concurrent retry processes, two independent repetitions, and the scenarios that must actually execute.

These numbers are a small teaching workload. They are not a statistical reliability estimate or a throughput target.

Before asking an agent for code, give it this kind of task:

```text
Build a local task list that adds and lists tasks.

First propose observable claims and the outcomes that would disprove them.
Preserve acknowledged tasks across fresh processes.
Bind each create request ID to one normalized title and one task.
Exercise concurrent retries and conflicting reuse.

Keep the application small. Use local synthetic data.
Do not claim properties the experiment does not exercise.
```

Review the claims yourself. An agent that quietly narrows “survives interruption” into “works twice in the same object” can produce a beautiful test for the wrong promise.

## 2. Give the agent a place to leave evidence

The project has a few small documents with distinct jobs:

```text
AGENTS.md                         working rules and commands
docs/plan.md                      task progress and handoff
docs/decisions.md                 decisions and their reasons
experiments/001-reliable-tasks/
  experiment.json                claims written before code
  README.md                      findings and limitations
  runs/<run-id>/                  actual outputs and source hashes
```

`AGENTS.md` tells an agent where these things live. The experiment file defines the claim. The run directory records what happened. The decision document explains what we chose because of it.

You can start with a short instruction:

```text
Read the experiment contract before changing behavior.
Run the declared scenarios and keep failed outputs.
Create a new run directory; never replace an earlier run.
Report which claims passed, which failed, and what was not tested.
```

Instructions need maintenance. If a useful constraint already lives in a canonical document, link to it. A growing pile of repeated instructions can make the next agent's job harder. OpenAI's current guidance similarly favors focused instructions and task-specific context. [Guidance on skills and project instructions](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## 3. Implement the smallest useful design

Tiny Tasks stores each task alongside its request ID. A unique database constraint prevents two stored rows from sharing that ID.

Creation uses one transaction. It looks for the ID, compares the normalized title if the ID exists, and inserts only when it is new. The command returns success after the transaction commits.

The central part of `tiny_tasks/store.py` looks like this:

```python
db.execute("BEGIN IMMEDIATE")
try:
    old = db.execute(
        "SELECT id, title FROM tasks WHERE request_id = ?",
        (request_id,),
    ).fetchone()

    if old:
        if old["title"] != title:
            raise Conflict("request ID was already used with another title")
        result = {"task": dict(old), "created": False}
    else:
        cursor = db.execute(
            "INSERT INTO tasks(request_id, title) VALUES (?, ?)",
            (request_id, title),
        )
        result = {
            "task": {"id": cursor.lastrowid, "title": title},
            "created": True,
        }

    db.execute("COMMIT")
    return result
except BaseException:
    db.execute("ROLLBACK")
    raise
```

“Normalized” has an explicit meaning here: the app removes leading and trailing whitespace before comparing titles. The database connection, schema and validation live in the complete source; the excerpt shows the transaction boundary.

That boundary matters because checking in one transaction and inserting later would leave room for another process to intervene. SQLite documents the write-transaction behavior of `BEGIN IMMEDIATE` in its [transaction reference](https://www.sqlite.org/lang_transaction.html). Still, plausible code is only a candidate explanation. We have to run the workload we promised to support.

## 4. Cross the boundary you are making a claim about

A test can create a `Store`, add a task and immediately list it. That is useful. It does not establish what happens in a new process.

Our experiment runner invokes the actual CLI in subprocesses. Every command starts fresh. For the restart scenario, it adds three tasks in sequence, checking after each successful create that a separate process can read the expected list.

For retries, it exercises two different situations:

- A create succeeds, its caller ignores the response, and a fresh process repeats the request.
- Eight processes submit the same request, launched through a synchronization barrier.

The second scenario checks the returned identities, the number of `created: true` responses and the rows actually saved. Exactly one task should exist.

The ignored response is a controlled stand-in for a caller that is unsure whether an action succeeded. We did not cut a network connection or kill a process during a commit. Keeping that distinction visible makes the result useful.

## 5. Break the application on purpose

Now comes my favorite part: establish that the experiment can catch the defect it claims to detect.

The `lab/` directory contains two intentionally wrong implementations. They use the same command shape as the real app:

- **Volatile:** returns successful creates but keeps no durable tasks.
- **Duplicates:** saves tasks but ignores request identity, inserting a row on every retry.

These are negative controls: known-bad examples that the checks must reject for a specific reason. They are teaching fixtures, not bugs we are pretending to have discovered accidentally.

The volatile version must fail the restart claim. The duplicate-accepting version must fail the concurrent retry claim. A syntax error in a broken version would not establish either property, so inspect the saved responses and failure reasons.

Review caught a weakness in the first version of the gate: it accepted a control's failure without checking its reason. A child-process crash could have masqueraded as a successful bug detection. We added regression tests, required nonzero exercise counts for the controls, and made the gate check the targeted failure reason. The earlier run remains in the repository, with that gate limitation recorded.

There is another way to get a misleading green result: execute nothing.

Our runner tracks how many times each required scenario ran. This intentionally incomplete report must fail even though every claimed outcome says `true`:

```python
empty = {
    "claims": {name: True for name in required_scenarios},
    "exercised": {name: 0 for name in required_scenarios},
}
```

A check that refuses zero activity is an **exercise gate**. It answers a basic question before interpreting success: did we actually attempt the scenarios our conclusion depends on?

## 6. Run it and keep the receipts

From the companion project:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/prove.py
```

The first command runs nine tests: six for application behavior and three for the harness. The second runs the process-boundary experiment, both negative-control implementations and the empty-exercise control.

In the recorded run, the results were:

| Implementation | Restart | Retry after ignored response | Concurrent retry | Conflicting reuse | Invalid input |
|---|---|---|---|---|---|
| Volatile control | Fail | Fail | Fail | Fail | Pass |
| Duplicate-accepting control | Pass | Fail | Fail | Fail | Pass |
| SQLite candidate | Pass | Pass | Pass | Pass | Pass |

Each implementation ran twice. The pass/fail outcomes and exercise counts matched between repetitions. The SQLite candidate exercised three restart rounds, one ignored-response retry, eight concurrent submissions, one conflicting reuse and one invalid-input scenario per repetition.

The two controls failed where intended. The report with zero exercised scenarios was rejected. Those facts allow the overall experiment gate to pass.

You will find a new directory under `experiments/001-reliable-tasks/runs/`. It contains:

- A manifest with Python and SQLite versions and hashes of the application, harness and contract.
- A response trace and scenario outcomes for each implementation and repetition.
- A summary with the overall decision and its scope.

The captured run used for this article is `20261010T042729Z-633b0705`. Your run will have its own ID. The project preserves the original directory so you can inspect the evidence behind this table.

The hashes help identify the source files used in a run. They do not establish who performed it, and someone who can rewrite both the files and their manifest can forge a matching set. This is reproducible local evidence, not a signed attestation system.

## 7. Make a decision the evidence supports

We can now choose SQLite for this local application's declared process and retry behavior.

We have not tested power failure, a corrupt disk, a network filesystem, large task volumes, security boundaries or sustained throughput. We have not measured how often different coding models produce a correct implementation. Those would be separate questions with different experiments.

This is also where you resist rounding a result into the outcome you wanted. If a target is missed, keep the result and the original threshold visible. A follow-up experiment can ask a better question; it should have a new identity.

A useful agent handoff looks like this:

```text
Implemented: persistent task creation and payload-bound retries.
Verified: the recorded process-boundary scenarios and negative controls.
Evidence: the named run directory and source manifest.
Not tested: power loss, disk corruption, throughput or model reliability.
Decision: use this implementation for the documented local scope.
```

That is enough for another developer—or another agent—to pick up the work without inheriting an unsupported “everything works.”

## What changes when agents do more of the work?

An agent can propose the claims, build the application, write the harness and summarize the run. That is convenient, but all four can share the same mistaken assumption.

Give the claim a review before implementation. Inspect the failure cases. Keep an external observation boundary: a subprocess, an HTTP client, an independently written reference calculation, or a recorded user journey appropriate to the property. Check the actual artifacts when an agent reports success.

A second model may help review the work. Its approval is another judgment to examine. For this tutorial, deterministic process results carry the decision; no model judge is needed.

The app itself does not use an LLM. That is deliberate. You can practice this development workflow with your preferred coding agent while keeping the example's behavior easy to inspect and its runs inexpensive to repeat.

## Try it on your next feature

Choose one promise your users care about. Describe an observation that would prove it wrong. Run a test that crosses the relevant boundary. Feed that test a known-bad case. Save the result with enough context that somebody else can challenge it.

Then ask your coding agent for the evidence directory.
