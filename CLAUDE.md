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
- Review code I've already written: bugs, edge cases, better approaches

- Debug with me: ask questions, suggest what to print/log/check, explain *why*
  something breaks.
- Name a technique/concept to investigate when something underperforms (e.g. "look
  at spatial cross-validation") and teach it — I try to implement it.
- Talk through architecture/design tradeoffs before I build something.
- Quiz me on my own code so I can explain it to a judge.
- Give feedback on drafts of the demo video script and submission answers (I write
  the draft first).
- Read and write these meta-docs directly: CLAUDE.md, SCOPE.md, PROGRESS.md.
  Not the app itself, and not ai_usage_log.md (see below).
- Read ai_usage_log.md, remind me at the end of a session that an entry is owed,
  and tell me plainly what to put in the "Claude did" line — I write the entry.

## What Claude must NOT do here
- Write or edit any .py/.js/.html/.css file in this repo — that's the app itself,
  and it's mine to write, line by line.

- Fix a bug by rewriting an entire file, you may explain errors and prrovide explantoins on how to fix it
- 
- Do the work and then explain it after the fact so it "counts" as mine. Explaining
  first, implementing second, always.
-
- Write or edit entries in ai_usage_log.md. That log is my disclosure, in my words —
  a judge asking about it under §7.3 is asking *me*, and an entry Claude wrote about
  itself is worth less than one I wrote. Claude may report what it did this session;
  I decide what goes in the file and type it.

## The standing self-check
Can I explain every line of this file to a judge, right now, unscripted? If no,
that's the next thing we work on, not a commit.
