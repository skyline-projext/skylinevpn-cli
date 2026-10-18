<div align="center">

# SkylineVPN CLI

Official command-line client for **SkylineVPN** — Linux · macOS · Windows

**English** · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [Русский](README.ru.md) · [فارسی](README.fa.md)

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **Fraud warning: `getskyline.org` is a phishing website.** It is not owned, operated, authorized or endorsed by SKYLINE NETWORKING TECH LLC and has no affiliation with SkylineVPN. Do not visit it, enter account credentials, payment details or personal information on it, or download any software from it. We accept no responsibility for any loss arising from the use of that website. If you have already entered information there, change your password immediately and contact support through the official website.

> [!IMPORTANT]
> **The only official website is [www.skylinevpn.com](https://www.skylinevpn.com).** Beware of imitation sites.
>
> **Subscriptions cannot be purchased in the CLI client.** Please purchase a subscription at [www.skylinevpn.com](https://www.skylinevpn.com) first, then log in with the same account.

## Requirements

| Platform | Supported systems |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel and Apple silicon |
| Windows | Windows 10+ · x64 |

## Install

### macOS

Open a terminal and run:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

Right-click **PowerShell** → **Run as administrator**, then run:

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

Open a terminal and run:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

The installer detects your architecture, verifies the SHA-256 checksum, installs the background service and asks for the display language. To choose it up front, end the command with `| sudo bash -s -- --lang en` (macOS / Linux) or `-Lang en` (Windows); use `zh` for Chinese.

## Usage

```bash
skyline login            # log in with your SkylineVPN account
skyline nodes            # list nodes
skyline connect 3        # connect to node #3 (or: skyline connect --best)
skyline status           # show connection status
skyline disconnect       # disconnect
```

| Command | Description |
|---|---|
| `skyline mode smart` / `skyline mode global` | Smart routing / global mode |
| `skyline nodes --refresh` | Refresh the node list |
| `skyline me` | Account info |
| `skyline lang english` / `skyline lang chinese` | Switch display language |
| `skyline logout` | Log out (`--purge` also removes saved login data) |
| `skyline version` | Version info |
| `skyline --help` | All commands |

> On Windows, open a **new** terminal window after installing. On Linux, log out and back in once so `skyline` works without `sudo`.

## Update

Run the install command again — it always fetches the latest release.

## Uninstall

| Platform | Command |
|---|---|
| Linux | `sudo apt-get remove skyline-cli` (use `purge` to also remove data and logs) |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh` (add `--purge` to also remove data and logs) |
| Windows (admin) | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"` (add `-Purge` to also remove data and logs) |

## Offline install & verification

All packages and installers are on the [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) page together with `SHA256SUMS.txt`.

- **Linux:** download `skyline-linux-cli-universal-*.tar.gz`, extract it, run `sudo bash <extracted-folder>/install.sh`.
- **macOS:** download the `.pkg` and `skyline-macos-install.sh` into the same folder, run `sudo bash skyline-macos-install.sh` there.
- **Windows:** download `skyline-windows-cli-amd64-*.zip`, extract it, double-click `install.cmd`.

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` verifies a package without installing.

## Troubleshooting

- **Linux VPS / container:** `/dev/net/tun` is required. Enable TUN/TAP in your VPS panel, or run the container with `--device /dev/net/tun --cap-add NET_ADMIN`.
- **macOS:** if you see "Background item added", allow `skyline` in *System Settings → General → Login Items & Extensions*.
- **Logs:** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## Support

Subscriptions, billing and support: **[www.skylinevpn.com](https://www.skylinevpn.com)** (the only official website).

## Telegram

Follow our official Telegram channels for announcements and service notifications. These are our only official Telegram channels:

- [![Telegram @skyline_vpn](https://img.shields.io/badge/Telegram-%40skyline__vpn-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn) Official channel
- [![Telegram @skyline_vpn_1](https://img.shields.io/badge/Telegram-%40skyline__vpn__1-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn_1) Notifications

---

© 2026 SKYLINE NETWORKING TECH LLC. All rights reserved. See [LICENSE](LICENSE).
