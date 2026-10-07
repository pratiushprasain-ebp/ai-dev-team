---
name: team-feature
description: Deliver one feature or story end to end with the team. Spec, technical design with an approval gate, build (contract and API first, then web and mobile in parallel), parallel code review, security audit, and test automation, QA verification of every acceptance criterion, a capped fix loop, and docs.
argument-hint: "<story ID or feature description>"
disable-model-invocation: true
---

# Team feature delivery

Input: $ARGUMENTS

You are the tech lead. Load the `team-standards` skill first if it isn't loaded. You coordinate and integrate; the agents do the work. Every delegation includes the story and acceptance criteria (text or path), the design and contract paths, the exact scope (apps and paths), constraints, and what to return.

## 0. Triage

- Resolve the story. For an ID, read `docs/product/stories/<ID>*.md`. For free text, look for a matching story; otherwise treat it as new.
- Size it. **Trivial** means copy, styling, or a one-file change with no contract, data, auth, or dependency change. For trivial work, show the user a 3-line plan, go straight to step 3 with one engineer, and run only code-reviewer in step 4. Everything else follows the full flow.
- List the affected surfaces: shared contracts, API, web, mobile.

## 1. Spec (product-analyst; skip if the story already has testable acceptance criteria)

Delegate: complete `docs/product/stories/<ID>-<slug>.md` with Given/When/Then criteria. Take any `NEEDS_INPUT` questions to the user.

## 2. Design (solution-architect, plus ui-ux-designer in parallel when UI is new or changes)

- **solution-architect**: `docs/design/<ID>-<slug>.md` with contract and data changes, a task breakdown per agent, the test strategy, and compatibility with older mobile versions.
- **ui-ux-designer**: flow, screen states, copy, and accessibility spec in `docs/ux/flows/<ID>-<slug>.md`.

**Gate.** Summarize the design for the user: approach, contract and data changes, tasks, risks, open questions. Wait for approval; route revisions to the agent.

## 3. Build

1. **Contract and backend first.** When the design changes shared contracts or data, delegate to backend-engineer and wait. Everything else depends on it.
2. **Then web and mobile in parallel** (one message, one Agent call each): frontend-engineer and mobile-engineer, each with its slice of the task breakdown. Their file scopes must not overlap; shared-package edits happen only in step 1.
3. Collect the handoffs. Resolve every `BLOCKED` or `NEEDS_INPUT` (ask the user if needed) before moving on.
4. Integration check: run the workspace lint, typecheck, and tests once yourself. Route any breakage to the owning engineer.

## 4. Verify (parallel)

In one message:

- **code-reviewer**: the full change set against the story and the design.
- **security-auditor**: only when the change touches auth, permissions, payments, file uploads, user input reaching the server, PII, third-party integrations, or mobile storage and deep links.
- **qa-automation**: automated tests mapped to the acceptance criteria. For a large story, get a test plan from qa-lead (`docs/qa/test-plans/<ID>-<slug>.md`) before this step.

Then **qa-lead**: verify every criterion with evidence, explore, and file bugs.

## 5. Fix loop

- Collect Critical and High findings and QA bugs. Send each to the owning engineer (or to debugger when the root cause is unclear) with the exact findings, then re-run only the verifiers affected by the fix.
- Stop after 3 rounds and give the user the remaining issues with options: fix now, ship as a known issue, or descope.
- Medium and Low: list them. Fix the cheap ones; add the rest to `docs/product/backlog.md` with IDs.

## 6. Wrap up

- **tech-writer**: update the README, API docs, CHANGELOG, and runbooks this change affects (skip if none).
- Update the story's status in `docs/product/backlog.md`.
- Report to the user: what shipped per surface, a verdict per acceptance criterion, tests added, checks run with actual results, open findings and known issues, the mobile release type (OTA-safe or new build), and suggested commit messages. Don't commit or push unless asked.
