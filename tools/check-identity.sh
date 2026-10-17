#!/usr/bin/env bash
# Publishing gate: every commit must be authored and committed by the locked publishing identity,
# carry no co-author / session trailers, git must never hold agent or memory files, and no
# forbidden term may appear in commit metadata or file contents anywhere in history.
# Run by tools/publish-release.sh and by the local git hooks (tools/install-hooks.sh).
#
# Usage: tools/check-identity.sh                   full check: identity, every commit on HEAD, all files ever committed
#        tools/check-identity.sh --commit-msg FILE  before a commit: identity, the new message, the staged files
#
# Forbidden terms: one literal per line in $SKYLINE_FORBIDDEN_TERMS
# (default ~/.config/skylinevpn-release/forbidden-terms), kept outside git so they are never published.
set -euo pipefail

NAME=skyline-projext
EMAIL=176280006+skyline-projext@users.noreply.github.com
IDENT="$NAME <$EMAIL>"
# Agent instructions, memories, transcripts and editor-agent folders
AGENT_FILES='(^|/)(CLAUDE(\.local)?\.md|AGENTS\.md|GEMINI\.md|MEMORY\.md|\.mcp\.json|\.cursorrules|copilot-instructions\.md)$|(^|/)(\.claude|\.cursor|\.codex|\.aider[^/]*|\.continue|memory)/|\.jsonl$'
# Trailers / text that attach anyone but the publishing identity
MSG_LEAKS='^(co-authored-by|signed-off-by|reviewed-by|claude-session|generated-by):|claude\.ai|anthropic|claude code|session_[0-9A-Za-z]{8,}'

root=$(cd "$(dirname "$0")/.." && pwd)
terms_file=${SKYLINE_FORBIDDEN_TERMS:-$HOME/.config/skylinevpn-release/forbidden-terms}
fail=0
bad() { echo "check-identity: $*" >&2; fail=1; }

terms=$(mktemp)
trap 'rm -f "$terms"' EXIT
if [ -r "$terms_file" ]; then
  grep -vE '^[[:space:]]*(#|$)' "$terms_file" > "$terms" || true
fi
[ -s "$terms" ] || { echo "check-identity: FAILED, no forbidden terms in $terms_file (see tools/RELEASING.md)" >&2; exit 1; }

for who in author committer; do
  ident=$(git -C "$root" var "GIT_$(echo "$who" | tr a-z A-Z)_IDENT" | sed -E 's/ [0-9]+ [+-][0-9]{4}$//')
  [ "$ident" = "$IDENT" ] || bad "git $who identity is '$ident', expected '$IDENT'"
done

if [ "${1:-}" = --commit-msg ]; then
  msg=${2:?usage: --commit-msg FILE}
  grep -vE '^#' "$msg" | grep -inE "$MSG_LEAKS" | sed 's/^/commit message: /' >&2 && fail=1
  grep -vE '^#' "$msg" | grep -inFf "$terms" | sed 's/^/commit message has a forbidden term: /' >&2 && fail=1
  git -C "$root" diff --cached --name-only --diff-filter=ACMR | grep -E "$AGENT_FILES" | sed 's/^/staged agent file: /' >&2 && fail=1
  git -C "$root" grep --cached -inIF -f "$terms" | cut -c1-200 | sed 's/^/staged forbidden term: /' >&2 && fail=1
else
  while IFS='|' read -r sha author committer; do
    [ "$author" = "$IDENT" ] || bad "$sha author is '$author'"
    [ "$committer" = "$IDENT" ] || bad "$sha committer is '$committer'"
    git -C "$root" log -1 --format=%B "$sha" | grep -inE "$MSG_LEAKS" | sed "s/^/$sha message: /" >&2 && fail=1
    git -C "$root" log -1 --format='%an %ae %cn %ce%n%B' "$sha" | grep -inFf "$terms" \
      | sed "s/^/$sha metadata has a forbidden term: /" >&2 && fail=1
  done < <(git -C "$root" log --format='%h|%an <%ae>|%cn <%ce>' HEAD)
  { git -C "$root" ls-files; git -C "$root" log --name-only --format= HEAD; } | sort -u | grep -E "$AGENT_FILES" \
    | sed 's/^/agent file in git: /' >&2 && fail=1
  # Contents of every committed version of every file, plus the index
  { git -C "$root" rev-list HEAD | xargs git -C "$root" grep -iIF -f "$terms" --; git -C "$root" grep --cached -iIF -f "$terms"; } \
    | cut -c1-200 | sed 's/^/forbidden term in git: /' >&2 && fail=1
fi

[ "$fail" = 0 ] || { echo "check-identity: FAILED, fix the above before committing / publishing" >&2; exit 1; }
echo "check-identity: ok ($IDENT)"
