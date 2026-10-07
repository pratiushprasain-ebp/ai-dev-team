#!/usr/bin/env bash
# Install the senior delivery team (agents + skills) for Claude Code.
#
#   ./install.sh                     symlink into ~/.claude (every project sees the team)
#   ./install.sh --project <path>    copy into <path>/.claude (commit it, customize per client)
#   ./install.sh --uninstall         remove the symlinks this repo created in ~/.claude
#   ./install.sh --dry-run [...]     show what would happen without changing anything
#
# Existing files are never overwritten: conflicts are reported and skipped.
# Honors CLAUDE_CONFIG_DIR if Claude Code's config lives somewhere else.
set -euo pipefail
shopt -s nullglob

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MODE=global
PROJECT=""
DRY_RUN=0
installed=0 present=0 conflicts=0 removed=0

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 ]] || { echo "error: --project needs a path" >&2; exit 2; }
      MODE=project; PROJECT="$2"; shift 2 ;;
    --uninstall) MODE=uninstall; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option $1" >&2; usage >&2; exit 2 ;;
  esac
done

run() {
  if [[ $DRY_RUN -eq 1 ]]; then echo "  (dry run) $*"; else "$@"; fi
}

# link <source> <target>: symlink unless the target already exists.
link() {
  local src=$1 dst=$2
  if [[ -L $dst && $(readlink "$dst") == "$src" ]]; then
    present=$((present + 1)); return
  fi
  if [[ -e $dst || -L $dst ]]; then
    echo "  conflict  $dst exists, left unchanged"; conflicts=$((conflicts + 1)); return
  fi
  run ln -s "$src" "$dst"
  echo "  linked    $dst"; installed=$((installed + 1))
}

# copy <source> <target>: copy unless the target already exists.
copy() {
  local src=$1 dst=$2
  if [[ -e $dst || -L $dst ]]; then
    echo "  conflict  $dst exists, left unchanged"; conflicts=$((conflicts + 1)); return
  fi
  run cp -R "$src" "$dst"
  echo "  copied    $dst"; installed=$((installed + 1))
}

# unlink_ours <target>: remove it only if it is a symlink pointing into this repo.
unlink_ours() {
  local dst=$1
  [[ -L $dst ]] || return 0
  case "$(readlink "$dst")" in
    "$REPO"/*) run rm "$dst"; echo "  removed   $dst"; removed=$((removed + 1)) ;;
  esac
}

case $MODE in
  global)
    echo "Linking the team into $CLAUDE_HOME"
    run mkdir -p "$CLAUDE_HOME/agents" "$CLAUDE_HOME/skills"
    for f in "$REPO"/agents/*.md; do link "$f" "$CLAUDE_HOME/agents/${f##*/}"; done
    for d in "$REPO"/skills/*/; do d=${d%/}; link "$d" "$CLAUDE_HOME/skills/${d##*/}"; done
    ;;
  project)
    [[ -d $PROJECT ]] || { echo "error: $PROJECT is not a directory" >&2; exit 2; }
    PROJECT=$(cd "$PROJECT" && pwd -P)
    echo "Copying the team into $PROJECT/.claude"
    run mkdir -p "$PROJECT/.claude/agents" "$PROJECT/.claude/skills"
    for f in "$REPO"/agents/*.md; do copy "$f" "$PROJECT/.claude/agents/${f##*/}"; done
    for d in "$REPO"/skills/*/; do d=${d%/}; copy "$d" "$PROJECT/.claude/skills/${d##*/}"; done
    ;;
  uninstall)
    echo "Removing links into $REPO from $CLAUDE_HOME"
    for f in "$CLAUDE_HOME"/agents/*.md; do unlink_ours "$f"; done
    for d in "$CLAUDE_HOME"/skills/*; do unlink_ours "$d"; done
    ;;
esac

echo
if [[ $DRY_RUN -eq 1 ]]; then
  echo "dry run, nothing changed: would install $installed, already present $present, conflicts $conflicts, would remove $removed"
  exit 0
fi
echo "installed $installed, already present $present, conflicts $conflicts, removed $removed"
if [[ $MODE == global && $installed -gt 0 ]]; then
  echo "Start a new Claude Code session to load the new agents and skills."
fi
if [[ $MODE == project && $installed -gt 0 ]]; then
  echo "Commit $PROJECT/.claude to share the team with the project. Project copies override global ones."
fi
if [[ $conflicts -gt 0 ]]; then exit 1; fi
