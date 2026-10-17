#!/usr/bin/env bash
# Install the local git hooks that run tools/check-identity.sh on every commit and push,
# and lock this clone's git identity. Hooks live in .git/hooks and are never pushed: run this after cloning.
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)

git -C "$root" config user.name skyline-projext
git -C "$root" config user.email 176280006+skyline-projext@users.noreply.github.com

hooks=$(git -C "$root" rev-parse --git-path hooks)
case "$hooks" in /*) ;; *) hooks="$root/$hooks" ;; esac
mkdir -p "$hooks"
printf '#!/bin/sh\nexec "$(git rev-parse --show-toplevel)/tools/check-identity.sh" --commit-msg "$1"\n' > "$hooks/commit-msg"
printf '#!/bin/sh\nexec "$(git rev-parse --show-toplevel)/tools/check-identity.sh"\n' > "$hooks/pre-push"
chmod +x "$hooks/commit-msg" "$hooks/pre-push"
echo "hooks installed in $hooks; identity: $(git -C "$root" config user.name) <$(git -C "$root" config user.email)>"
