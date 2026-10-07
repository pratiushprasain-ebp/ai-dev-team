---
name: team-estimate
description: Turn a client brief into a scoped, assumption-backed effort estimate for a freelance quote, with work breakdown, three-point estimates, risks, exclusions, and milestones, using the product-analyst and solution-architect agents.
argument-hint: "<brief text, or path or URL to the brief>"
disable-model-invocation: true
---

# Team estimate

Brief: $ARGUMENTS

You are the tech lead running a pre-sales estimate. Load the `team-standards` skill first if it isn't loaded. Give each agent the full context it needs: it sees only CLAUDE.md, the standards, and your prompt.

## 1. Get the brief

- If the brief is a file path, read it. If it's a URL, fetch it. If it's empty, ask the user to paste the brief or give its path, then stop.
- In one AskUserQuestion call, ask only about what's missing and would change the cost: surfaces in scope (website, web app, admin panel, iOS, Android); design source (client's Figma, we design it, template); deadline; hourly rate (optional; without it the estimate stays in hours); mandatory tech or hosting; integrations (payments, maps, chat, CRM, others).

## 2. Scope (product-analyst)

Delegate: from the brief and answers, write a draft `docs/product/PRD.md` and `docs/product/backlog.md` at estimate granularity (epics and stories), with assumptions (A-xx), open questions (Q-xx), and app-store obligations.

## 3. Technical sizing (solution-architect)

Delegate with the PRD and backlog paths: propose the architecture that fits this brief (ADRs with status Proposed); list the technical risks and unknowns that move effort (integrations, real-time, offline, payments, data migration, compliance); list spikes worth doing before committing to a fixed price (don't run them); note the effort drivers per epic (reuse or new, complexity).

## 4. Estimate (product-analyst)

Delegate with both outputs: write `docs/product/estimates/<YYYY-MM-DD>-estimate.md` in your estimate format: breakdown per epic and discipline, three-point estimates with PERT, justified contingency, overheads (setup, environments and CI, store submission and review, QA and UAT, client feedback rounds, handover, warranty), exclusions, client dependencies, milestones with deliverables, and the risks that would change the number. Include a cost range only if the user gave a rate.

## 5. Present

Tell the user: the total range in hours (and cost, if a rate was given), the top assumptions, the biggest risks, exclusions, open questions for the client, recommended spikes, and the file paths. Suggest sending the client questions first and re-running the estimate once they're answered. Never send anything to the client yourself.
