<div align="center">

# SkylineVPN CLI

**SkylineVPN** 公式コマンドラインクライアント — Linux · macOS · Windows

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **日本語** · [Русский](README.ru.md) · [فارسی](README.fa.md)

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **詐欺にご注意ください：`getskyline.org` はフィッシングサイトです。** 当該サイトは SKYLINE NETWORKING TECH LLC が所有、運営、許可または承認するものではなく、SkylineVPN とは一切関係ありません。アクセスしないでください。また、アカウント情報、お支払い情報、個人情報を入力したり、ソフトウェアをダウンロードしたりしないでください。当該サイトの利用により生じたいかなる損害についても、当社は責任を負いません。すでに情報を入力された場合は、直ちにパスワードを変更し、公式サイトからサポートにお問い合わせください。

> [!IMPORTANT]
> **公式サイトは [www.skylinevpn.com](https://www.skylinevpn.com) のみです。** 偽サイトにご注意ください。
>
> **CLI クライアントではサブスクリプションを購入できません。** 先に [www.skylinevpn.com](https://www.skylinevpn.com) でサブスクリプションを購入し、同じアカウントでログインしてください。

## 動作環境

| プラットフォーム | 対応システム |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel および Apple シリコン |
| Windows | Windows 10+ · x64；Windows 11 · ARM64 |

## インストール

### macOS

ターミナルを開いて、次のコマンドを実行します：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

**PowerShell** を右クリック → **管理者として実行** を選び、次のコマンドを実行します：

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

ターミナルを開いて、次のコマンドを実行します：

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

インストーラーはアーキテクチャを検出し、SHA-256 チェックサムを検証したうえでバックグラウンドサービスをインストールし、表示言語を尋ねます。あらかじめ指定するには、コマンドの末尾に `| sudo bash -s -- --lang en`（macOS / Linux）または `-Lang en`（Windows）を付けてください。中国語の場合は `zh` を使用します。

## 使い方

```bash
skyline login            # SkylineVPN アカウントでログイン
skyline nodes            # ノード一覧を表示
skyline connect 3        # 3 番のノードに接続（または：skyline connect --best）
skyline status           # 接続状態を表示
skyline disconnect       # 切断
```

| コマンド | 説明 |
|---|---|
| `skyline mode smart` / `skyline mode global` | スマートルーティング / グローバルモード |
| `skyline nodes --refresh` | ノード一覧を更新 |
| `skyline me` | アカウント情報 |
| `skyline lang english` / `skyline lang chinese` | 表示言語を切り替え |
| `skyline logout` | ログアウト（`--purge` で保存済みのログイン情報も削除） |
| `skyline version` | バージョン情報 |
| `skyline --help` | すべてのコマンド |

> Windows では、インストール後に**新しい**ターミナルウィンドウを開いてください。Linux では、`sudo` なしで `skyline` を使えるよう、一度ログアウトして再ログインしてください。

## アップデート

インストールコマンドをもう一度実行してください。常に最新リリースが取得されます。

## アンインストール

| プラットフォーム | コマンド |
|---|---|
| Linux | `sudo apt-get remove skyline-cli`（データとログも削除する場合は `purge` を使用） |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh`（データとログも削除する場合は `--purge` を追加） |
| Windows（管理者） | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"`（データとログも削除する場合は `-Purge` を追加） |

## オフラインインストールと検証

すべてのパッケージとインストーラーは、`SHA256SUMS.txt` とともに [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) ページで入手できます。

- **Linux：** `skyline-linux-cli-universal-*.tar.gz` をダウンロードして展開し、`sudo bash <extracted-folder>/install.sh` を実行します。
- **macOS：** `.pkg` と `skyline-macos-install.sh` を同じフォルダにダウンロードし、そのフォルダで `sudo bash skyline-macos-install.sh` を実行します。
- **Windows：** `skyline-windows-cli-amd64-*.zip`（ARM64 PC では `skyline-windows-cli-arm64-*.zip`）をダウンロードして展開し、`install.cmd` をダブルクリックします。

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` で、インストールせずにパッケージを検証できます。

## トラブルシューティング

- **Linux VPS / コンテナ：** `/dev/net/tun` が必要です。VPS のコントロールパネルで TUN/TAP を有効にするか、`--device /dev/net/tun --cap-add NET_ADMIN` を指定してコンテナを実行してください。
- **macOS：** 「バックグラウンド項目が追加されました」と表示された場合は、*システム設定 → 一般 → ログイン項目と機能拡張* で `skyline` を許可してください。
- **ログ：** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## サポート

サブスクリプション、お支払い、サポート：**[www.skylinevpn.com](https://www.skylinevpn.com)**（唯一の公式サイト）。

## Telegram チャンネル

お知らせやサービス通知は公式 Telegram チャンネルでご確認ください。公式 Telegram チャンネルは次の 2 つのみです：

- [![Telegram @skyline_vpn](https://img.shields.io/badge/Telegram-%40skyline__vpn-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn) 公式チャンネル
- [![Telegram @skyline_vpn_1](https://img.shields.io/badge/Telegram-%40skyline__vpn__1-26A5E4?logo=telegram&logoColor=white)](https://t.me/skyline_vpn_1) 通知チャンネル

---

© 2026 SKYLINE NETWORKING TECH LLC. 無断転載を禁じます。詳しくは [LICENSE](LICENSE) をご覧ください。
