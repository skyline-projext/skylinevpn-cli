#!/usr/bin/env python3
"""Stage a GitHub release of the SkylineVPN CLI from the three upstream CI bundles.

Usage:
    python3 tools/build_release.py <tag> [--src DIR] [--out DIR]

    <tag>       release tag, e.g. v3.0.0
    --src DIR   folder holding Linux-CLI*.zip, macOS-CLI*.zip, Windows-CLI*.zip (default: repo root)
    --out DIR   output folder (default: dist/<tag>)

What it does:
    - unpacks the upstream bundles into a temp folder;
    - checks every package against the sha256 baked into its installer;
    - points the installers' download URLs at this repo's GitHub release <tag>
      (so an installer always matches its own packages); upstream already gives them
      stable names, which makes .../releases/latest/download/<name> work;
    - fails if an installer still contains internal build notes / hosts or downloads
      from another release, or if the three platforms disagree on the app version;
    - unpacks every asset down to its last file (zip, tar, deb, pkg, gzip / xz / zstd / pbzx)
      and fails if any forbidden term from ~/.config/skylinevpn-release/forbidden-terms
      (override: $SKYLINE_FORBIDDEN_TERMS) appears anywhere in it; --accept-upstream-terms
      turns hits in upstream assets into listed warnings (never in the generated notes / checksums);
    - writes the release assets, SHA256SUMS.txt and RELEASE_NOTES.md into the output folder.

Internal test scripts and *.version files from the upstream bundles are never published.
"""
import argparse
import bz2
import glob
import gzip
import hashlib
import io
import lzma
import os
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib

REPO = "skyline-projext/skylinevpn-cli"
SITE = "https://www.skylinevpn.com"
RELEASES = f"https://github.com/{REPO}/releases"
LATEST = f"{RELEASES}/latest/download"

LINUX_INSTALLER = "skyline-linux-install.sh"
MACOS_INSTALLER = "skyline-macos-install.sh"
WINDOWS_INSTALLER = "skyline-windows-install.ps1"

# Nothing matching these may end up in a published installer.
LEAK_PATTERNS = [
    r"(?i)cloudfront", r"(?i)amazonaws", r"(?i)\bs3\b", r"(?i)telegram", r"开发群", r"\.github/workflows",
    r"github\.com/(?!skyline-projext/skylinevpn-cli)", r"\bPLAN\b", r"\bD-\d+", r"用户[：定]",
    r"App 会话", r"(?<!\$env:)\bCI\b", r"Artifact",
    # personal / agent identities and e-mail addresses
    r"(?i)claude|anthropic|session_[0-9A-Za-z]{8,}|noreply", r"[\w.%+-]+@[\w-]+\.[\w.-]+",
]

# Literal terms that must not appear in any asset; kept outside git so the list is never published.
TERMS_FILE = os.environ.get("SKYLINE_FORBIDDEN_TERMS",
                            os.path.expanduser("~/.config/skylinevpn-release/forbidden-terms"))


def die(msg):
    sys.exit(f"build_release: {msg}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def one(pattern, where):
    hits = glob.glob(os.path.join(where, pattern))
    if len(hits) != 1:
        die(f"expected exactly one {pattern} in {where}, found {len(hits)}")
    return hits[0]


def sub(text, pattern, repl, flags=re.M, count_min=1, count_max=1):
    """re.subn that insists on the expected number of hits, so upstream format changes fail loudly."""
    new, n = re.subn(pattern, repl, text, flags=flags)
    if not (count_min <= n <= count_max):
        die(f"pattern {pattern!r} matched {n} times (expected {count_min}..{count_max})")
    return new


def var(text, name, quote='"'):
    m = re.search(rf"^\$?{name}\s*=\s*{quote}([^{quote}]*){quote}", text, re.M)
    if not m:
        die(f"{name} not found in installer")
    return m.group(1)


def scrub_common(text, eol="\n"):
    """Customer-facing wording shared by the bash and PowerShell installers."""
    text = sub(text, r"请从 Telegram / Release 里给出的地址重新下载 \*-install\.sh",
               f"请从 {RELEASES} 重新下载安装脚本", count_min=0, count_max=99)
    text = sub(text, r"Download \*-install\.sh again from the link you were given",
               f"Download the installer again from {RELEASES}", count_min=0, count_max=99)
    text = sub(text, r"占位符没有被 CI 填入", "占位符没有被填入", count_min=0, count_max=99)
    text = sub(text, r" not filled in by CI\)", " not filled in)", count_min=0, count_max=99)
    text = sub(text, r"把上面的输出发给开发群",f"把上面的输出发给客服（{SITE}）", count_min=0, count_max=99)
    text = sub(text, r"[sS]end the output above to support(?! \()",
               lambda m: f"{m.group(0)} ({SITE})", count_min=0, count_max=99)
    return text


def retag(text, tag):
    """Point every release download URL at <tag>, so an installer always matches its own packages."""
    return sub(text, r"(/releases/download/)[^/\s\"']+/", rf"\g<1>{tag}/", count_max=99)


def check_leaks(path, tag):
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    for i, line in enumerate(text.splitlines(), 1):
        for p in LEAK_PATTERNS:
            if re.search(p, line):
                die(f"{os.path.basename(path)}:{i} still contains internal info ({p}): {line.strip()}")
        for t in re.findall(r"/releases/download/([^/\s\"']+)/", line):
            if t != tag:
                die(f"{os.path.basename(path)}:{i} downloads from release {t}, expected {tag}")


def forbidden_terms():
    """One regex over all forbidden terms, case-insensitive, as UTF-8 and as UTF-16LE (Windows resources)."""
    try:
        with open(TERMS_FILE, encoding="utf-8") as f:
            terms = [l.strip() for l in f if l.strip() and not l.lstrip().startswith("#")]
    except OSError:
        terms = []
    if not terms:
        die(f"no forbidden terms in {TERMS_FILE} (see tools/RELEASING.md)")
    alts = []
    for t in terms:
        b = t.encode()
        alts += [re.escape(b), b"\x00".join(re.escape(bytes([c])) for c in b)]
    return re.compile(b"|".join(alts), re.I)


def zstd_decompress(data):
    try:
        import zstandard
        return zstandard.ZstdDecompressor().stream_reader(io.BytesIO(data)).read()
    except ImportError:
        try:
            return subprocess.run(["zstd", "-dc"], input=data, stdout=subprocess.PIPE, check=True).stdout
        except FileNotFoundError:
            die("need the zstandard Python module or the zstd command to scan .deb packages")


def unwrap(data):
    """Undo stream compression: gzip, xz, zstd, Apple pbzx."""
    while True:
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        elif data[:6] == b"\xfd7zXZ\x00":
            data = lzma.decompress(data)
        elif data[:4] == b"\x28\xb5\x2f\xfd":
            data = zstd_decompress(data)
        elif data[:4] == b"pbzx":
            chunks, pos = [], 12
            while pos < len(data):
                size = struct.unpack_from(">Q", data, pos + 8)[0]
                chunk = data[pos + 16:pos + 16 + size]
                chunks.append(lzma.decompress(chunk) if chunk[:6] == b"\xfd7zXZ\x00" else chunk)
                pos += 16 + size
            data = b"".join(chunks)
        else:
            return data


def members(data):
    """(name, bytes) of each file in a zip / tar / ar (.deb) / xar (.pkg) archive; None if data is no archive."""
    if data[:4] == b"PK\x03\x04":
        z = zipfile.ZipFile(io.BytesIO(data))
        return [(i.filename, z.read(i)) for i in z.infolist() if not i.is_dir()] + [("(zip comment)", z.comment)]
    if data[257:262] == b"ustar":
        t = tarfile.open(fileobj=io.BytesIO(data))
        return [(m.name, t.extractfile(m).read() if m.isfile() else b"") for m in t.getmembers()] \
            + [(f"{m.name} (owner)", f"{m.uname} {m.gname} {m.linkname}".encode()) for m in t.getmembers()]
    if data[:8] == b"!<arch>\n":
        out, pos = [], 8
        while pos + 60 <= len(data):
            name, size = data[pos:pos + 16].decode().strip().rstrip("/"), int(data[pos + 48:pos + 58])
            out.append((name, data[pos + 60:pos + 60 + size]))
            pos += 60 + size + (size & 1)
        return out
    if data[:4] == b"xar!":
        hsize, _, clen = struct.unpack_from(">HHQ", data, 4)
        toc = zlib.decompress(data[hsize:hsize + clen])
        out = [("(xar toc)", toc)]
        for f in ET.fromstring(toc).iter("file"):
            d = f.find("data")
            if d is None or d.find("offset") is None:
                continue
            off, length = int(d.find("offset").text), int(d.find("length").text)
            raw = data[hsize + clen + off:hsize + clen + off + length]
            style = d.find("encoding").get("style", "")
            raw = zlib.decompress(raw) if "gzip" in style else bz2.decompress(raw) if "bzip2" in style else raw
            out.append((f.find("name").text, raw))
        return out
    return None


def scan_terms(name, data, rx, hits):
    """Record every forbidden term in an asset, recursing into the archives packed inside it."""
    data = unwrap(data)
    inner = members(data)
    if inner is None:
        for m in rx.finditer(data):
            term = m.group().replace(b"\x00", b"").decode("latin1")
            hits.add(f"{name}: {term}")
        return
    for sub_name, sub_data in inner:
        if rx.search(sub_name.encode()):
            hits.add(f"{name}/{sub_name}: (file name)")
        scan_terms(f"{name}/{sub_name}", sub_data, rx, hits)


def write_text(path, text, bom=False, mode=0o644):
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, mode)


# ---------------------------------------------------------------- Linux
def build_linux(zip_path, work, out, tag):
    src = os.path.join(work, "linux")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(src)
    script_path = one(LINUX_INSTALLER, src)
    bundle_path = one("skyline-linux-cli-universal-*.tar.gz", src)
    upstream = open(script_path, encoding="utf-8").read()

    deb_names = {a: var(upstream, f"DEB_NAME_{a.upper()}") for a in ("amd64", "arm64")}
    deb_shas = {a: var(upstream, f"DEB_SHA256_{a.upper()}") for a in ("amd64", "arm64")}
    version, build = var(upstream, "APP_VERSION"), var(upstream, "BUILD_TS")
    if var(upstream, "SELF_NAME") != LINUX_INSTALLER:
        die(f"SELF_NAME in {LINUX_INSTALLER} is not {LINUX_INSTALLER}")
    text = scrub_common(retag(upstream, tag))

    # Packages: verify against the sha256 baked into the installer.
    bundle_dir = os.path.join(work, "linux-bundle")
    with tarfile.open(bundle_path) as t:
        t.extractall(bundle_dir)
    (top,) = os.listdir(bundle_dir)
    for arch in ("amd64", "arm64"):
        deb = os.path.join(bundle_dir, top, arch, deb_names[arch])
        if sha256(deb) != deb_shas[arch]:
            die(f"{deb_names[arch]}: sha256 does not match the installer")
        shutil.copy2(deb, os.path.join(out, deb_names[arch]))
    bundled = os.path.join(bundle_dir, top, "install.sh")
    if open(bundled, encoding="utf-8").read() != upstream:
        die(f"install.sh in {os.path.basename(bundle_path)} differs from {LINUX_INSTALLER}")

    write_text(os.path.join(out, LINUX_INSTALLER), text, mode=0o755)
    if text == upstream:
        # Nothing to patch: publish the offline bundle exactly as built.
        shutil.copy2(bundle_path, os.path.join(out, os.path.basename(bundle_path)))
    else:
        # Offline bundle: same layout, patched install.sh.
        write_text(bundled, text, mode=0o755)

        def reset(ti):
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = "root"
            return ti

        with tarfile.open(os.path.join(out, os.path.basename(bundle_path)), "w:gz") as t:
            t.add(os.path.join(bundle_dir, top), arcname=top, filter=reset)
    return {"version": version, "build": build, "bundle": os.path.basename(bundle_path), "debs": deb_names}


# ---------------------------------------------------------------- macOS
def build_macos(zip_path, work, out, tag):
    src = os.path.join(work, "macos")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(src)
    script_path = one(MACOS_INSTALLER, src)
    text = open(script_path, encoding="utf-8").read()

    pkg_name, pkg_sha = var(text, "PKG_NAME"), var(text, "PKG_SHA256")
    version, build = var(text, "APP_VERSION"), var(text, "BUILD_TS")
    pkg = os.path.join(src, pkg_name)
    if not os.path.isfile(pkg):
        die(f"{pkg_name} missing from {os.path.basename(zip_path)}")
    if sha256(pkg) != pkg_sha:
        die(f"{pkg_name}: sha256 does not match the installer")
    if not var(text, "SELF_URL").endswith(f"/{MACOS_INSTALLER}"):
        die(f"SELF_URL in {MACOS_INSTALLER} does not end in {MACOS_INSTALLER}")
    text = scrub_common(retag(text, tag))

    # Only the .pkg is published; the bundle's .tar.gz and the PKG_ALT_NAME copy are not.
    write_text(os.path.join(out, MACOS_INSTALLER), text, mode=0o755)
    shutil.copy2(pkg, os.path.join(out, pkg_name))
    return {"version": version, "build": build, "pkg": pkg_name}


# ---------------------------------------------------------------- Windows
def build_windows(zip_path, work, out, tag):
    src = os.path.join(work, "windows")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(src)
    script_path = one(WINDOWS_INSTALLER, src)
    raw = open(script_path, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    eol = "\r\n" if "\r\n" in text else "\n"

    zip_name, zip_sha = var(text, "ZipName", "'"), var(text, "ZipSha256", "'")
    version, build = var(text, "AppVersion", "'"), var(text, "BuildTs", "'")
    pkg = os.path.join(src, zip_name)
    if not os.path.isfile(pkg):
        die(f"{zip_name} missing from {os.path.basename(zip_path)}")
    if sha256(pkg) != zip_sha:
        die(f"{zip_name}: sha256 does not match the installer")
    if not var(text, "ZipUrl", "'").endswith(f"/{zip_name}"):
        die(f"$ZipUrl in {WINDOWS_INSTALLER} does not end in {zip_name}")
    text = scrub_common(retag(text, tag), eol)

    write_text(os.path.join(out, WINDOWS_INSTALLER), text, bom=bom)
    shutil.copy2(pkg, os.path.join(out, zip_name))
    return {"version": version, "build": build, "zip": zip_name}


# ---------------------------------------------------------------- notes
def notes(tag, lin, mac, win):
    return f"""## SkylineVPN CLI {tag}

> [!IMPORTANT]
> **The only official website is [www.skylinevpn.com]({SITE}).** Memberships cannot be purchased in the CLI client — please buy a plan on the website first.
> **唯一官网 [www.skylinevpn.com]({SITE})。** CLI 客户端无法购买会员，请先前往官网购买。

### One-line install

**macOS**
```bash
curl -fsSL {LATEST}/{MACOS_INSTALLER} | sudo bash
```
**Windows** (PowerShell, *Run as administrator*)
```powershell
iwr -UseBasicParsing {LATEST}/{WINDOWS_INSTALLER} -OutFile $env:TEMP\\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\\skyline-install.ps1
```
**Linux**
```bash
curl -fsSL {LATEST}/{LINUX_INSTALLER} | sudo bash
```

Then: `skyline login` → `skyline nodes` → `skyline connect <number>` → `skyline status`. Full guide: [README](https://github.com/{REPO}#readme).

### Assets

| Platform | File |
|---|---|
| macOS installer | `{MACOS_INSTALLER}` |
| macOS 12+ (universal) | `{mac['pkg']}` |
| Windows installer | `{WINDOWS_INSTALLER}` |
| Windows 10+ x64 | `{win['zip']}` |
| Linux installer | `{LINUX_INSTALLER}` |
| Linux amd64 | `{lin['debs']['amd64']}` |
| Linux arm64 | `{lin['debs']['arm64']}` |
| Linux offline bundle (amd64 + arm64) | `{lin['bundle']}` |

Builds: macOS {mac['version']} ({mac['build']}) · Windows {win['version']} ({win['build']}) · Linux {lin['version']} ({lin['build']}). Checksums: `SHA256SUMS.txt`.
"""


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag")
    ap.add_argument("--src", default=root)
    ap.add_argument("--out")
    ap.add_argument("--accept-upstream-terms", action="store_true",
                    help="stage even if upstream packages / installers contain forbidden terms (listed as warnings); "
                         "the generated RELEASE_NOTES.md and SHA256SUMS.txt are always checked")
    a = ap.parse_args()
    if not re.fullmatch(r"v\d+\.\d+\.\d+([-.][0-9A-Za-z.-]+)?", a.tag):
        die(f"tag must look like v3.0.0, got {a.tag!r}")
    out = a.out or os.path.join(root, "dist", a.tag)
    terms = forbidden_terms()
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)

    with tempfile.TemporaryDirectory(prefix="skyline-release-") as work:
        lin = build_linux(one("Linux-CLI*.zip", a.src), work, out, a.tag)
        mac = build_macos(one("macOS-CLI*.zip", a.src), work, out, a.tag)
        win = build_windows(one("Windows-CLI*.zip", a.src), work, out, a.tag)

    versions = {lin["version"], mac["version"], win["version"]}
    if len(versions) != 1:
        die(f"platforms disagree on the app version: Linux {lin['version']}, macOS {mac['version']}, Windows {win['version']}")
    if a.tag.lstrip("v").split("-")[0] != lin["version"]:
        print(f"build_release: note: tag {a.tag} differs from app version {lin['version']}", file=sys.stderr)

    for name in (LINUX_INSTALLER, MACOS_INSTALLER, WINDOWS_INSTALLER):
        check_leaks(os.path.join(out, name), a.tag)

    assets = sorted(os.listdir(out))
    with open(os.path.join(out, "SHA256SUMS.txt"), "w") as f:
        for name in assets:
            f.write(f"{sha256(os.path.join(out, name))}  {name}\n")
    write_text(os.path.join(out, "RELEASE_NOTES.md"), notes(a.tag, lin, mac, win))
    check_leaks(os.path.join(out, "RELEASE_NOTES.md"), a.tag)

    hits, ours = set(), set()
    for name in sorted(os.listdir(out)):
        with open(os.path.join(out, name), "rb") as f:
            scan_terms(name, f.read(), terms, ours if name in ("RELEASE_NOTES.md", "SHA256SUMS.txt") else hits)
    if ours or (hits and not a.accept_upstream_terms):
        shutil.rmtree(out)  # never leave a publishable folder behind
        die(f"forbidden terms in {len(hits | ours)} places, nothing staged:\n  " + "\n  ".join(sorted(hits | ours)))
    if hits:
        print(f"build_release: WARNING: accepted {len(hits)} forbidden-term hits in upstream assets:\n  "
              + "\n  ".join(sorted(hits)), file=sys.stderr)

    print(f"Release {a.tag} staged in {out}:")
    for name in sorted(os.listdir(out)):
        print(f"  {os.path.getsize(os.path.join(out, name)):>10}  {name}")


if __name__ == "__main__":
    main()
