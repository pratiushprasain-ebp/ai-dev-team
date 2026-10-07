---
name: team-review
description: Parallel multi-agent review of the current changes (or a given branch, range, or paths) by code-reviewer, security-auditor, and performance-engineer in audit mode, merged into one de-duplicated, severity-ranked report.
argument-hint: "[base branch | commit range | paths] (default: uncommitted changes + branch vs main)"
disable-model-invocation: true
---

# Team review

Scope: $ARGUMENTS

Load the `team-standards` skill first if it isn't loaded.

1. **Resolve the scope.** Default: uncommitted changes plus the commits on this branch since its merge-base with the default branch. Show the file list with `git diff --stat`. If there's nothing to review, say so and stop.
2. **Find the intent**: related story and design docs (from the branch name, commit messages, or changed paths). Pass their paths to the reviewers.
3. **Delegate in parallel**, in one message, with the same scope and intent:
   - **code-reviewer**: full review.
   - **security-auditor**: audit of the diff, including the entry points that reach it.
   - **performance-engineer** in AUDIT mode (no edits). Skip it when the change is only docs, tests, or config.
   - **qa-lead** (optional, when tests changed or a story is referenced): do the tests cover the acceptance criteria?
4. **Merge.** De-duplicate overlapping findings, keeping the most severe and most specific version. Read the code yourself to check any finding that looks doubtful. Rank by severity and group by file.
5. **Output**:
   - Verdict: APPROVE, APPROVE WITH NITS, or REQUEST CHANGES (any Critical or High).
   - Findings: `[Severity] path:line — problem → impact → fix (source agent)`.
   - Checks run, with results.
   - Then offer to fix the findings with the owning agents. Don't fix anything until the user agrees.
