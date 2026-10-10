# Research notes: evidence-driven development

Research date: 2026-10-10 UTC. These are attribution and editorial notes, not a systematic
literature review. Search terms included the exact phrase, agent workflows and related
evaluation-driven development. No claim of first use or exhaustive coverage is warranted.

## Findings from primary sources

| Source | What it supports | What it does not establish |
|---|---|---|
| [Jan Bosch, *Speed, Data, and Ecosystems*, CRC Press/Routledge, 2017](https://www.routledge.com/Speed-Data-and-Ecosystems-Succeeding-in-a-Software-Centric-World/Bosch/p/book/9781315270685) | Publisher's indexed catalog lists Evidence-Driven Development and requirements-to-hypotheses topics; the phrase predates today's coding-agent discussion | We did not read the full book or establish the phrase's first use. Direct full-page retrieval failed; the indexed publisher catalog was available |
| [Xia et al., EDDOps, arXiv:2411.13768v3](https://arxiv.org/abs/2411.13768v3) | A process model and reference architecture for continuing offline/online evaluation of LLM agents | This is broader than our deterministic application tutorial; it is not evidence that our example improves model quality. The page labels the paper under review |
| [AWS, AgentCore Evaluations](https://aws.amazon.com/blogs/machine-learning/build-reliable-ai-agents-with-amazon-bedrock-agentcore-evaluations/) | AWS explicitly uses evidence-driven development for measured agent improvement and connects development evaluation to ongoing monitoring | It is a vendor implementation and perspective, not a universal EDD standard |
| [AWS Samples, GEDD](https://github.com/aws-samples/sample-GEDD) | A related named workflow uses expert-curated evidence to calibrate LLM judges and response gates | Its runtime judging focus differs from our coding-process example; no endorsement or equivalence is implied |
| [Agile Alliance, TDD](https://agilealliance.org/glossary/tdd/) and [Given–When–Then](https://agilealliance.org/glossary/given-when-then/) | Existing test-first and acceptance-example practices belong in the lineage | EDD does not supersede these practices or claim that earlier testing lacked evidence |
| [OpenAI, current skills and prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Focused task routing and maintained project instructions are useful for coding agents | Markdown alone does not enforce security, prove behavior or replace observed tests |
| [University of Twente, EVI](https://www.utwente.nl/en/eemcs/evi/) | Evidence-driven black-box checking combines expected behavior with observations from executed tests | The tutorial does not implement that research project's techniques |

EDDOps version chronology: first submission 2024-11-21; the referenced v3 revision is
2025-11-17. Use the versioned citation when discussing that title/abstract. Do not confuse
evidence-driven development with evaluation-driven development solely because both can
abbreviate to EDD.

## Editorial position

Call this a practical evidence-driven workflow for agent-assisted software development.
Attribute the earlier terminology. The contribution is the runnable demonstration:
falsifiable claims, small implementation, known-bad controls, fresh-process observation,
exercise counts, retained artifacts and a decision with an explicit boundary.

Avoid invention claims, a proprietary framework name, universal reliability claims or
claims that a passing test suite proves an AI model trustworthy. This is a deterministic
application built with assistance; model-to-model comparisons are not part of its evidence.

## Implementation and publishing references

- [SQLite transactions](https://www.sqlite.org/lang_transaction.html): transaction behavior
  and `BEGIN IMMEDIATE`; retain the app's bounded busy timeout and explicit error outcome.
- [DEV editor guide](https://dev.to/p/editor_guide): unpublished front matter, at most four
  tags, heading levels and a suggested 1000 × 420 cover. Local preview styling will not
  carry into DEV's own layout.
