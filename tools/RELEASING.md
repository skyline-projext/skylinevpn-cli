# Releasing (maintainers)

Publishing identity is locked to **skyline-projext <176280006+skyline-projext@users.noreply.github.com>**:
every commit (author and committer) and the GitHub account that publishes. Commit messages carry no
co-author, sign-off or session lines. After cloning, run `tools/install-hooks.sh` once; it locks
the clone's git identity and installs hooks that run `tools/check-identity.sh` on every commit
and push. `publish-release.sh` runs the same check and asks you to confirm the account.

Terms that must never be published (names of other entities, personal accounts) are listed one per
line in `~/.config/skylinevpn-release/forbidden-terms`, outside the repo so the list itself stays
private. `check-identity.sh` scans all of git history for them and `build_release.py` scans every
release asset, including the files inside the packages; both refuse to run without that file.
Hits inside upstream packages that have been reviewed and accepted can be let through with
`build_release.py <tag> --accept-upstream-terms`, which lists every one of them as a warning.

1. Put the three CI bundles in the repo root (they are git-ignored):
   `Linux-CLI-*.zip`, `macOS-CLI*.zip`, `Windows-CLI*.zip`
2. Stage the release:
   ```bash
   python3 tools/build_release.py v3.0.1
   ```
   This verifies every package against its installer's sha256, points the installers
   (`skyline-{linux,macos}-install.sh`, `skyline-windows-install.ps1`, named by upstream) at
   `releases/download/<tag>/`, fails if internal build notes remain or the platforms disagree
   on the app version, and writes everything to `dist/<tag>/`. When the installers already
   point at `<tag>`, the assets are published byte-for-byte as upstream built them.
3. Update `CHANGELOG.md`, commit, `git push origin main`.
4. Publish and mark as latest:
   ```bash
   tools/publish-release.sh v3.0.1
   ```

The README's one-line commands use `releases/latest/download/…`, so they always serve the newest
release; each installer then downloads the packages of its own tag.

Never commit binaries, `*.version` files, internal test scripts, tokens, or agent instruction / memory
files (`CLAUDE.md`, `AGENTS.md`, `.claude/`, `MEMORY.md`, …) — `.gitignore` and `check-identity.sh` cover them.
