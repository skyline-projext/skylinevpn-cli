<div align="center">

# SkylineVPN CLI

**SkylineVPN** 官方命令行客户端 — Linux · macOS · Windows

[English](README.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [Русский](README.ru.md) · [فارسی](README.fa.md)

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **防诈骗提醒：`getskyline.org` 为钓鱼网站。** 该网站并非由 SKYLINE NETWORKING TECH LLC 拥有、运营、授权或认可，与 SkylineVPN 无任何关联。请勿访问该网站，切勿在其中输入账号密码、支付信息或个人信息，也不要从中下载任何软件。因使用该网站造成的任何损失，我们概不负责。如您已在该网站提交信息，请立即修改密码，并通过官方网站联系客服。

> [!IMPORTANT]
> **唯一官方网站为 [www.skylinevpn.com](https://www.skylinevpn.com)。** 谨防仿冒网站。
>
> **CLI 客户端内无法购买订阅。** 请先在 [www.skylinevpn.com](https://www.skylinevpn.com) 购买订阅，再使用同一账号登录。

## 系统要求

| 平台 | 支持的系统 |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel 与 Apple 芯片 |
| Windows | Windows 10+ · x64 |

## 安装

### macOS

打开终端并运行：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

右键单击 **PowerShell** → **以管理员身份运行**，然后运行：

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

打开终端并运行：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

安装程序会检测系统架构、校验 SHA-256 校验和、安装后台服务，并询问显示语言。如需预先指定，请在命令末尾加上 `| sudo bash -s -- --lang en`（macOS / Linux）或 `-Lang en`（Windows）；中文请使用 `zh`。

## 使用

```bash
skyline login            # 使用 SkylineVPN 账号登录
skyline nodes            # 列出节点
skyline connect 3        # 连接 3 号节点（或：skyline connect --best）
skyline status           # 查看连接状态
skyline disconnect       # 断开连接
```

| 命令 | 说明 |
|---|---|
| `skyline mode smart` / `skyline mode global` | 智能分流 / 全局模式 |
| `skyline nodes --refresh` | 刷新节点列表 |
| `skyline me` | 账户信息 |
| `skyline lang english` / `skyline lang chinese` | 切换显示语言 |
| `skyline logout` | 退出登录（`--purge` 会同时删除已保存的登录数据） |
| `skyline version` | 版本信息 |
| `skyline --help` | 全部命令 |

> Windows 安装完成后，请打开一个**新的**终端窗口。Linux 请注销并重新登录一次，以便无需 `sudo` 即可使用 `skyline`。

## 更新

再次运行安装命令即可 — 它始终会获取最新版本。

## 卸载

| 平台 | 命令 |
|---|---|
| Linux | `sudo apt-get remove skyline-cli`（改用 `purge` 可同时删除数据和日志） |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh`（加上 `--purge` 可同时删除数据和日志） |
| Windows（管理员） | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"`（加上 `-Purge` 可同时删除数据和日志） |

## 离线安装与校验

所有安装包和安装程序均可在 [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) 页面获取，并附有 `SHA256SUMS.txt`。

- **Linux：** 下载 `skyline-linux-cli-universal-*.tar.gz`，解压后运行 `sudo bash <extracted-folder>/install.sh`。
- **macOS：** 将 `.pkg` 和 `skyline-macos-install.sh` 下载到同一文件夹，并在该文件夹中运行 `sudo bash skyline-macos-install.sh`。
- **Windows：** 下载 `skyline-windows-cli-amd64-*.zip`，解压后双击 `install.cmd`。

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` 可在不安装的情况下校验安装包。

## 故障排除

- **Linux VPS / 容器：** 需要 `/dev/net/tun`。请在 VPS 控制面板中启用 TUN/TAP，或使用 `--device /dev/net/tun --cap-add NET_ADMIN` 运行容器。
- **macOS：** 如果看到“已添加背景项目”，请在 *系统设置 → 通用 → 登录项与扩展* 中允许 `skyline`。
- **日志：** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## 支持

订阅、账单与支持：**[www.skylinevpn.com](https://www.skylinevpn.com)**（唯一官方网站）。

## Telegram 频道

关注官方 Telegram 频道，获取公告与服务通知。官方 Telegram 频道仅有以下两个：

- [![Telegram @skyline_vpn](https://img.shields.io/badge/Telegram-%40skyline__vpn-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn) 官方频道
- [![Telegram @skyline_vpn_1](https://img.shields.io/badge/Telegram-%40skyline__vpn__1-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn_1) 通知频道

---

© 2026 SKYLINE NETWORKING TECH LLC. 保留所有权利。详见 [LICENSE](LICENSE)。
