<div align="center">

# SkylineVPN CLI

Официальный клиент командной строки **SkylineVPN** — Linux · macOS · Windows

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **Русский** · [فارسی](README.fa.md)

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **Предупреждение о мошенничестве: `getskyline.org` — фишинговый сайт.** Он не принадлежит SKYLINE NETWORKING TECH LLC, не управляется, не авторизован и не одобрен ею и никак не связан со SkylineVPN. Не посещайте его, не вводите на нём данные учётной записи, платёжные или личные данные и не скачивайте с него программы. Мы не несём ответственности за любой ущерб, возникший в результате использования этого сайта. Если вы уже ввели там свои данные, немедленно смените пароль и обратитесь в поддержку через официальный сайт.

> [!IMPORTANT]
> **Единственный официальный сайт — [www.skylinevpn.com](https://www.skylinevpn.com).** Остерегайтесь поддельных сайтов.
>
> **Подписку нельзя купить в CLI-клиенте.** Сначала оформите подписку на [www.skylinevpn.com](https://www.skylinevpn.com), затем войдите под той же учётной записью.

## Системные требования

| Платформа | Поддерживаемые системы |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel и Apple Silicon |
| Windows | Windows 10+ · x64 |

## Установка

### macOS

Откройте терминал и выполните:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

Щёлкните правой кнопкой мыши по **PowerShell** → **Запуск от имени администратора**, затем выполните:

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

Откройте терминал и выполните:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

Установщик определит архитектуру, проверит контрольную сумму SHA-256, установит фоновую службу и предложит выбрать язык интерфейса. Чтобы указать язык заранее, добавьте в конец команды `| sudo bash -s -- --lang en` (macOS / Linux) или `-Lang en` (Windows); для китайского используйте `zh`.

## Использование

```bash
skyline login            # войти с учётной записью SkylineVPN
skyline nodes            # список узлов
skyline connect 3        # подключиться к узлу №3 (или: skyline connect --best)
skyline status           # показать состояние подключения
skyline disconnect       # отключиться
```

| Команда | Описание |
|---|---|
| `skyline mode smart` / `skyline mode global` | Умная маршрутизация / глобальный режим |
| `skyline nodes --refresh` | Обновить список узлов |
| `skyline me` | Информация об учётной записи |
| `skyline lang english` / `skyline lang chinese` | Сменить язык интерфейса |
| `skyline logout` | Выйти (`--purge` также удаляет сохранённые данные входа) |
| `skyline version` | Информация о версии |
| `skyline --help` | Все команды |

> В Windows после установки откройте **новое** окно терминала. В Linux один раз выйдите из системы и войдите снова, чтобы `skyline` работал без `sudo`.

## Обновление

Снова выполните команду установки — она всегда загружает последний выпуск.

## Удаление

| Платформа | Команда |
|---|---|
| Linux | `sudo apt-get remove skyline-cli` (используйте `purge`, чтобы также удалить данные и журналы) |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh` (добавьте `--purge`, чтобы также удалить данные и журналы) |
| Windows (администратор) | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"` (добавьте `-Purge`, чтобы также удалить данные и журналы) |

## Офлайн-установка и проверка

Все пакеты и установщики доступны на странице [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) вместе с `SHA256SUMS.txt`.

- **Linux:** скачайте `skyline-linux-cli-universal-*.tar.gz`, распакуйте и выполните `sudo bash <extracted-folder>/install.sh`.
- **macOS:** скачайте `.pkg` и `skyline-macos-install.sh` в одну папку и выполните в ней `sudo bash skyline-macos-install.sh`.
- **Windows:** скачайте `skyline-windows-cli-amd64-*.zip`, распакуйте и дважды щёлкните `install.cmd`.

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` проверяет пакет без установки.

## Устранение неполадок

- **Linux VPS / контейнер:** требуется `/dev/net/tun`. Включите TUN/TAP в панели управления VPS или запустите контейнер с параметрами `--device /dev/net/tun --cap-add NET_ADMIN`.
- **macOS:** если появилось уведомление «Background item added», разрешите `skyline` в разделе *Системные настройки → Основные → Объекты входа и расширения*.
- **Журналы:** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## Поддержка

Подписка, оплата и поддержка: **[www.skylinevpn.com](https://www.skylinevpn.com)** (единственный официальный сайт).

---

© 2026 SKYLINE NETWORKING TECH LLC. Все права защищены. Подробнее см. [LICENSE](LICENSE).
