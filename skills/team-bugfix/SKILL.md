---
name: team-bugfix
description: Fix a bug with the team. The debugger reproduces it, proves the root cause, and applies a minimal fix with a regression test; then code review and QA re-verification with nearby regression checks.
argument-hint: "<bug description, BUG-ID, error message, or failing test>"
disable-model-invocation: true
---

# Team bugfix

Bug: $ARGUMENTS

Load the `team-standards` skill first if it isn't loaded.

1. **Collect evidence.** For a BUG-ID, read `docs/qa/bugs/<ID>*.md`. Gather the error text, logs, failing test names, environment, and recent commits (`git log -10 --oneline`). If key facts are missing (environment, steps, expected vs actual) and the repo can't answer them, ask the user once.
2. **Debug (debugger).** Hand over everything you collected. Expect a reproduction, the root cause with evidence, a minimal fix, a regression test, and verification results.
   - `NEEDS_INPUT` (can't reproduce, needs data): ask the user, then continue the same agent with SendMessage if available, or delegate again with the new information.
   - If the fix crosses ownership or carries risk (contract, migration, auth), present the options to the user before it's applied.
3. **Verify (parallel).** code-reviewer on the fix diff, and qa-lead to re-run the reproduction steps plus nearby regression checks (same screen, endpoint, or flow; both platforms when the code is shared). Add security-auditor when the bug has a security angle.
4. **Fix loop.** Critical or High findings go back to the debugger. After 2 rounds, escalate to the user.
5. **Update the bug file** if one exists: status Fixed, root cause, and a summary of the fix.
6. **Report**: the root cause in 1–2 sentences, the fix, the regression test, verification results, the same-pattern search results, and a suggested commit message (`fix(<scope>): …`). Don't commit unless asked.
