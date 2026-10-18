#!/usr/bin/env bash
# Publish a release staged by tools/build_release.py to GitHub and mark it as latest.
#
# Usage: tools/publish-release.sh <tag> [--confirm-account skyline-projext]   e.g. tools/publish-release.sh v3.0.0
#        Without --confirm-account it asks on the terminal.
#
# Needs: gh, a local main equal to origin/main, and a token for skyline-projext in $GH_TOKEN
# (falls back to the export_ghp_skylinevpn_token line in ~/.zshrc). The token is never written to disk.
# Refuses to publish unless tools/check-identity.sh passes and the publishing identity is typed back.
set -euo pipefail

REPO=skyline-projext/skylinevpn-cli
root=$(cd "$(dirname "$0")/.." && pwd)
tag=${1:?usage: tools/publish-release.sh <tag> [--confirm-account skyline-projext]}
confirmed=
[ "${2:-}" = --confirm-account ] && confirmed=${3:-}
dist="$root/dist/$tag"

if [ -z "${GH_TOKEN:-}" ]; then
  GH_TOKEN=$(sed -nE 's/^export_ghp_skylinevpn_token="([^"]+)".*/\1/p' ~/.zshrc 2>/dev/null || true)
fi
[ -n "${GH_TOKEN:-}" ] || { echo "GH_TOKEN is not set" >&2; exit 2; }
export GH_TOKEN

[ -f "$dist/RELEASE_NOTES.md" ] || { echo "$dist not staged: run python3 tools/build_release.py $tag" >&2; exit 2; }
(cd "$dist" && sha256sum -c --quiet SHA256SUMS.txt) || { echo "checksums in $dist do not match" >&2; exit 2; }

login=$(gh api user --jq .login)
[ "$login" = skyline-projext ] || { echo "token belongs to $login, expected skyline-projext" >&2; exit 2; }

"$root/tools/check-identity.sh" || exit 2

head=$(git -C "$root" rev-parse HEAD)
remote=$(git -C "$root" ls-remote origin refs/heads/main | cut -f1)
[ "$head" = "$remote" ] || { echo "local HEAD is not origin/main: merge the pull request, then git checkout main && git pull" >&2; exit 2; }

# Publishing identity is locked: show it and have it typed back before anything is published.
cat >&2 <<EOF_
About to publish $REPO $tag (commit ${head:0:12}) as:
  GitHub account : $login
  git author     : $(git -C "$root" log -1 --format='%an <%ae>' "$head")
  git committer  : $(git -C "$root" log -1 --format='%cn <%ce>' "$head")
EOF_
if [ -z "$confirmed" ]; then
  [ -t 0 ] || { echo "publish-release: no terminal: pass --confirm-account skyline-projext" >&2; exit 2; }
  read -r -p "Check the identity above, then type the publishing account (skyline-projext) to continue: " confirmed
fi
[ "$confirmed" = skyline-projext ] || { echo "publish-release: not confirmed, nothing published" >&2; exit 2; }

assets=()
while IFS= read -r f; do assets+=("$dist/$f"); done < <(ls "$dist" | grep -v '^RELEASE_NOTES\.md$')

gh release create "$tag" "${assets[@]}" \
  --repo "$REPO" \
  --target "$head" \
  --title "SkylineVPN CLI $tag" \
  --notes-file "$dist/RELEASE_NOTES.md" \
  --latest

echo "Published: https://github.com/$REPO/releases/tag/$tag"
