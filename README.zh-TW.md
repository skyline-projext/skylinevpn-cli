<div align="center">

# SkylineVPN CLI

**SkylineVPN** 官方命令列用戶端 — Linux · macOS · Windows

[English](README.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [日本語](README.ja.md) · [Русский](README.ru.md) · [فارسی](README.fa.md)

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **防詐騙提醒：`getskyline.org` 為釣魚網站。** 該網站並非由 SKYLINE NETWORKING TECH LLC 擁有、經營、授權或認可，與 SkylineVPN 無任何關聯。請勿造訪該網站，切勿於其中輸入帳號密碼、付款資訊或個人資料，亦請勿從中下載任何軟體。因使用該網站所生之任何損失，我們概不負責。若您已於該網站提交資料，請立即變更密碼，並透過官方網站聯絡客服。

> [!IMPORTANT]
> **唯一官方網站為 [www.skylinevpn.com](https://www.skylinevpn.com)。** 請慎防仿冒網站。
>
> **CLI 用戶端內無法購買訂閱。** 請先至 [www.skylinevpn.com](https://www.skylinevpn.com) 購買訂閱，再以同一帳號登入。

## 系統需求

| 平台 | 支援的系統 |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel 與 Apple 晶片 |
| Windows | Windows 10+ · x64；Windows 11 · ARM64 |

## 安裝

### macOS

開啟終端機並執行：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

在 **PowerShell** 上按右鍵 → **以系統管理員身分執行**，然後執行：

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

開啟終端機並執行：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

安裝程式會偵測系統架構、驗證 SHA-256 總和檢查碼、安裝背景服務，並詢問顯示語言。若要預先指定，請在指令結尾加上 `| sudo bash -s -- --lang en`（macOS / Linux）或 `-Lang en`（Windows）；中文請使用 `zh`。

## 使用方式

```bash
skyline login            # 以 SkylineVPN 帳號登入
skyline nodes            # 列出節點
skyline connect 3        # 連線至 3 號節點（或：skyline connect --best）
skyline status           # 顯示連線狀態
skyline disconnect       # 中斷連線
```

| 指令 | 說明 |
|---|---|
| `skyline mode smart` / `skyline mode global` | 智慧分流 / 全域模式 |
| `skyline nodes --refresh` | 重新整理節點清單 |
| `skyline me` | 帳號資訊 |
| `skyline lang english` / `skyline lang chinese` | 切換顯示語言 |
| `skyline logout` | 登出（`--purge` 會一併移除已儲存的登入資料） |
| `skyline version` | 版本資訊 |
| `skyline --help` | 所有指令 |

> Windows 安裝完成後，請開啟一個**新的**終端機視窗。Linux 請登出後重新登入一次，即可不需 `sudo` 直接使用 `skyline`。

## 更新

再次執行安裝指令即可 — 它一律會取得最新版本。

## 解除安裝

| 平台 | 指令 |
|---|---|
| Linux | `sudo apt-get remove skyline-cli`（改用 `purge` 可一併移除資料與記錄檔） |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh`（加上 `--purge` 可一併移除資料與記錄檔） |
| Windows（系統管理員） | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"`（加上 `-Purge` 可一併移除資料與記錄檔） |

## 離線安裝與驗證

所有套件與安裝程式皆可在 [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) 頁面取得，並附有 `SHA256SUMS.txt`。

- **Linux：** 下載 `skyline-linux-cli-universal-*.tar.gz`，解壓縮後執行 `sudo bash <extracted-folder>/install.sh`。
- **macOS：** 將 `.pkg` 與 `skyline-macos-install.sh` 下載至同一個資料夾，並在該資料夾中執行 `sudo bash skyline-macos-install.sh`。
- **Windows：** 下載 `skyline-windows-cli-amd64-*.zip`（ARM64 電腦請下載 `skyline-windows-cli-arm64-*.zip`），解壓縮後按兩下 `install.cmd`。

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` 可在不安裝的情況下驗證套件。

## 疑難排解

- **Linux VPS / 容器：** 需要 `/dev/net/tun`。請在 VPS 控制台中啟用 TUN/TAP，或以 `--device /dev/net/tun --cap-add NET_ADMIN` 執行容器。
- **macOS：** 若看到「已加入背景項目」，請在 *系統設定 → 一般 → 登入項目與延伸功能* 中允許 `skyline`。
- **記錄檔：** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## 支援

訂閱、帳務與支援：**[www.skylinevpn.com](https://www.skylinevpn.com)**（唯一官方網站）。

## Telegram 頻道

關注官方 Telegram 頻道，取得公告與服務通知。官方 Telegram 頻道僅有以下兩個：

- [![Telegram @skyline_vpn](https://img.shields.io/badge/Telegram-%40skyline__vpn-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn) 官方頻道
- [![Telegram @skyline_vpn_1](https://img.shields.io/badge/Telegram-%40skyline__vpn__1-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn_1) 通知頻道

---

© 2026 SKYLINE NETWORKING TECH LLC. 版權所有。詳見 [LICENSE](LICENSE)。
