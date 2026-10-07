---
name: team-kickoff
description: Start a new client project with the team. Produces requirements (PRD, backlog, first stories), architecture and ADRs, design system, delivery plan, and the project CLAUDE.md, with approval gates between phases, then optionally scaffolds the repo, CI, and a walking skeleton.
argument-hint: "[brief text or path] (optional when docs/product/PRD.md exists)"
disable-model-invocation: true
---

# Team kickoff

Input: $ARGUMENTS

You are the tech lead. Load the `team-standards` skill first if it isn't loaded. Run the phases in order and stop at each gate until the user approves. Post one short progress line per phase.

## Phase 0: Context

- Inspect the repo: empty, or existing code? Existing `docs/product/`, `docs/architecture/`, `CLAUDE.md`?
- Reuse a PRD from `/team-estimate` if one exists. Otherwise you need the brief, from the input or by asking the user.

## Phase 1: Requirements (product-analyst)

Delegate: finalize `docs/product/PRD.md` and `docs/product/backlog.md` with the MVP marked, and write stories for the first milestone in `docs/product/stories/`.

**Gate 1.** Show the user the scope (in and out), the MVP list, assumptions that need client confirmation, and open questions. Wait. Route requested changes back to product-analyst until the user approves.

## Phase 2: Architecture and UX foundations (parallel)

In one message, delegate to both:

- **solution-architect**: `docs/architecture/overview.md`; ADRs for stack, repo layout, API style and hosting, database and ORM, auth, mobile build and release, observability, and environments; a contract skeleton in `docs/architecture/api/`; `docs/architecture/delivery-plan.md` (walking skeleton first, riskiest work early).
- **ui-ux-designer**: `docs/ux/design-system.md` and token definitions (in `packages/tokens` unless told otherwise), navigation and information architecture per surface, and flows for the MVP journeys.

Then reconcile: check that the two outputs agree (token location, navigation vs routes, platform list). Send conflicts back to the relevant agent.

**Gate 2.** Present the stack decisions (with running-cost notes for paid services), the repo layout, the delivery milestones, and a design system summary. Paid services and vendor lock-in need the user's explicit approval. Wait.

## Phase 3: Project CLAUDE.md

Write `CLAUDE.md` at the repo root from the template at `${CLAUDE_SKILL_DIR}/templates/CLAUDE.md`, filled in from the approved docs. Keep it under about 150 lines and link to docs instead of copying them. If a CLAUDE.md already exists, merge into it; never discard the user's content.

## Phase 4: Scaffold (optional; ask first)

Ask whether to scaffold now. If yes:

1. **devops-engineer**: monorepo skeleton per the ADRs (apps, packages, tooling, scripts), CI pipeline, `.env.example`, `docs/runbooks/setup.md`.
2. **backend-engineer**: health endpoint, database connection, and one shared schema in `packages/shared`.
3. In parallel: **frontend-engineer** (home page calling the health endpoint through the shared client) and **mobile-engineer** (one screen making the same call).
4. Verify it yourself: install, lint, typecheck, test, and build all pass. Report the actual output.

Don't commit unless the user asks; suggest an initial commit message instead.

## Finish

Summarize: artifacts created (paths), decisions made, open questions for the client, and the next command: `/team-feature <first story ID>`.
