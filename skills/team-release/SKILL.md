---
name: team-release
description: Release readiness check with the team. Full regression and QA sign-off, security and dependency audit, performance check, deploy and mobile release plan, release notes, and a go/no-go decision. Prepares only; never deploys or submits without explicit approval.
argument-hint: "<version, e.g. 1.2.0> [web|mobile|all]"
disable-model-invocation: true
---

# Team release

Input: $ARGUMENTS

Load the `team-standards` skill first if it isn't loaded. This command prepares a release and recommends GO or NO-GO. It never deploys, publishes OTA updates, or submits to stores unless the user explicitly instructs that exact action after reading the report.

1. **Scope.** Version and targets (web, API, mobile). Collect the changes since the last release tag (`git log <last-tag>..HEAD --oneline`), the stories marked done, and the open bugs in `docs/qa/bugs/`. Run the full check suite once yourself (lint, typecheck, unit and integration tests, builds) and note the results.
2. **Delegate in parallel**, in one message:
   - **qa-lead**: regression over all MVP journeys and this release's stories across the device and browser matrix; write `docs/qa/release/<version>.md` with GO, GO WITH RISKS, or NO-GO.
   - **security-auditor**: release audit covering dependencies, a secrets scan, auth and permission changes since the last release, mobile storage and deep links, and privacy declarations compared with actual data collection.
   - **performance-engineer** in AUDIT mode: budgets for the key routes, endpoints, and screens compared with the last release.
   - **devops-engineer**: the release plan: pipeline status, migrations and their order, env vars and secrets needed (names only), rollback plan, mobile build type (OTA-safe or new native build), EAS profiles and channels, the store checklist, and the exact commands. Prepare only; run nothing outward-facing.
3. **Then tech-writer**: CHANGELOG entry, `docs/releases/<version>.md`, store "What's new" text for mobile, and handover and runbook updates.
4. **Decide.** NO-GO if there is any open Critical, any High the user hasn't explicitly accepted, failing checks, or no rollback plan. Present the verdict, blockers, risks needing the user's sign-off, numbered release steps with commands, post-release checks (smoke tests, dashboards, error rates), and the criteria that trigger a rollback.
5. **Only on the user's explicit instruction**, run the approved steps one at a time, confirming each irreversible step (production deploy, store submission, production OTA update) before running it.
