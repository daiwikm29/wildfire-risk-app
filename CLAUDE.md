# CLAUDE.md — Wildfire Risk Checker (Congressional App Challenge 2026)

## Session start
Read PROGRESS.md first (private, gitignored) for full context on this project and
where things stand. Then check SCOPE.md's phase checkpoints and ai_usage_log.md's
last entry before doing anything else.

## Constraint this whole project runs under

2026 CAC Rules (https://www.congressionalappchallenge.us/wp-content/uploads/2026/05/2026-CAC-Rules.pdf), §3:

> ORIGINALITY: All coding and technical development must be done by the student or
> student team.
> AI USAGE: AI may only be used to support specific aspects of the project and must
> not constitute the entirety of the technical development.

§7.3: judges may request source code and question the student on it; failing to
account for it is immediate disqualification. Deadline: Oct 26, 2026, 12:00pm EDT.

This file exists to get maximum genuine help *inside* that line, not the minimum
required to comply.

## What Claude MAY do here
- Explain concepts, libraries, errors, algorithms, stack traces, docs.
- Review code I've already written: bugs, edge cases, better approaches — as
  prose/pointers, not rewritten code.
- Debug with me: ask questions, suggest what to print/log/check, explain *why*
  something breaks. I write the fix.
- Name a technique/concept to investigate when something underperforms (e.g. "look
  at spatial cross-validation") and teach it — I implement it.
- Talk through architecture/design tradeoffs before I build something.
- Quiz me on my own code so I can explain it to a judge.
- Give feedback on drafts of the demo video script and submission answers (I write
  the draft first).
- Read and write this repo's meta-docs directly: CLAUDE.md, SCOPE.md,
  ai_usage_log.md, PROGRESS.md. Not the app itself.

## What Claude must NOT do here
- Write or edit any .py/.js/.html/.css file in this repo — that's the app itself,
  and it's mine to write, line by line.
- Generate a whole function, class, snippet, or file "to paste in," even a small
  one, even as a "just this once" starting point.
- Fix a bug by rewriting the broken file — point at what's wrong and why, I make
  the edit.
- Choose the model, hyperparameters, feature set, or architecture for me — explain
  the tradeoffs, I decide.
- Do the work and then explain it after the fact so it "counts" as mine. Explaining
  first, implementing second, always.
- Write code inside a chat reply "just for reference" that ends up copy-pasted
  wholesale.

## The standing self-check
Can I explain every line of this file to a judge, right now, unscripted? If no,
that's the next thing we work on, not a commit.
