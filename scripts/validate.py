#!/usr/bin/env python3
"""Lint the team's agent and skill files.

`claude plugin validate` accepts malformed frontmatter, so this checks what
Claude Code actually reads: YAML frontmatter, field names, allowed values,
names matching file names, and preloaded skills that exist.

Usage: python3 scripts/validate.py   (exits 1 on errors; needs PyYAML)
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is missing: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent

AGENT_FIELDS = {
    "name", "description", "tools", "disallowedTools", "model", "permissionMode",
    "maxTurns", "skills", "mcpServers", "hooks", "memory", "background",
    "omitClaudeMd", "effort", "isolation", "color", "initialPrompt", "experimental",
}
SKILL_FIELDS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools", "disallowed-tools",
    "model", "effort", "context", "agent", "background", "hooks", "paths", "shell",
    "metadata", "license", "compatibility",
}
MODELS = {"sonnet", "opus", "haiku", "fable", "inherit"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
MEMORY = {"user", "project", "local"}
KNOWN_TOOLS = {
    "Agent", "Bash", "Edit", "Glob", "Grep", "LSP", "NotebookEdit", "Read",
    "Skill", "TodoWrite", "ToolSearch", "WebFetch", "WebSearch", "Write",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []
warnings = []


def report(bucket, path, msg):
    bucket.append("{}: {}".format(path.relative_to(ROOT), msg))


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        report(errors, path, "missing YAML frontmatter between --- lines")
        return None, ""
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        report(errors, path, "invalid YAML: " + " ".join(str(exc).split()))
        return None, ""
    if not isinstance(data, dict):
        report(errors, path, "frontmatter is not a mapping")
        return None, ""
    return data, match.group(2)


def tool_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    if isinstance(value, list):
        return [str(t).strip() for t in value]
    return None


skill_names = {p.parent.name for p in ROOT.glob("skills/*/SKILL.md")}
agent_paths = sorted(ROOT.glob("agents/*.md"))

for path in agent_paths:
    fm, body = read_frontmatter(path)
    if fm is None:
        continue
    for key in sorted(set(fm) - AGENT_FIELDS):
        report(errors, path, "unknown field '{}'".format(key))
    name = fm.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name):
        report(errors, path, "name must be kebab-case")
    elif name != path.stem:
        report(errors, path, "name '{}' doesn't match the file name".format(name))
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report(errors, path, "description is required")
    elif len(desc) > 600:
        report(warnings, path, "description is {} chars; all agent descriptions share one context budget".format(len(desc)))
    model = fm.get("model")
    if model is not None and model not in MODELS and not str(model).startswith("claude-"):
        report(errors, path, "model '{}' is not one of {} or a claude-* model ID".format(model, sorted(MODELS)))
    for key, allowed in (("effort", EFFORTS), ("color", COLORS), ("memory", MEMORY)):
        if key in fm and fm[key] not in allowed:
            report(errors, path, "{} '{}' is not one of {}".format(key, fm[key], sorted(allowed)))
    for key in ("tools", "disallowedTools"):
        tools = tool_list(fm.get(key))
        if tools is None:
            report(errors, path, "{} must be a comma-separated string or a list".format(key))
            continue
        for tool in tools:
            base = tool.split("(")[0]
            if base not in KNOWN_TOOLS and not base.startswith("mcp__"):
                report(warnings, path, "{}: unknown tool '{}'".format(key, tool))
    explicit = tool_list(fm.get("tools"))
    if "memory" in fm and explicit and "Write" not in explicit:
        report(warnings, path, "memory auto-enables Write/Edit, which breaks this agent's read-only tool list")
    skills = fm.get("skills") or []
    if not isinstance(skills, list):
        report(errors, path, "skills must be a list")
    else:
        for skill in skills:
            if skill not in skill_names:
                report(warnings, path, "preloaded skill '{}' isn't in skills/ (fine only if installed elsewhere)".format(skill))
    if not body.strip():
        report(errors, path, "empty system prompt")

for path in sorted(ROOT.glob("skills/*/SKILL.md")):
    fm, body = read_frontmatter(path)
    if fm is None:
        continue
    for key in sorted(set(fm) - SKILL_FIELDS):
        report(errors, path, "unknown field '{}'".format(key))
    if fm.get("name", path.parent.name) != path.parent.name:
        report(errors, path, "name '{}' doesn't match the directory name".format(fm.get("name")))
    desc = str(fm.get("description") or "") + str(fm.get("when_to_use") or "")
    if not desc.strip():
        report(errors, path, "description is required")
    elif len(desc) > 1536:
        report(errors, path, "description + when_to_use is {} chars; Claude Code truncates at 1536".format(len(desc)))
    if "argument-hint" in fm and not isinstance(fm["argument-hint"], str):
        report(errors, path, "argument-hint must be a string (quote values that start with [ or <)")
    if not body.strip():
        report(errors, path, "empty skill body")

for line in warnings:
    print("warning: " + line)
for line in errors:
    print("error:   " + line)
print("{} agents, {} skills: {} errors, {} warnings".format(
    len(agent_paths), len(skill_names), len(errors), len(warnings)))
sys.exit(1 if errors else 0)
