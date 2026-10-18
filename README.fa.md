<div align="center">

# SkylineVPN CLI

کلاینت رسمی خط فرمان **SkylineVPN** — Linux · macOS · Windows

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [Русский](README.ru.md) · **فارسی**

[![Latest release](https://img.shields.io/github/v/release/skyline-projext/skylinevpn-cli?label=release)](https://github.com/skyline-projext/skylinevpn-cli/releases/latest)

</div>

> [!CAUTION]
> **هشدار کلاهبرداری: `getskyline.org` یک وب‌سایت فیشینگ است.** این وب‌سایت متعلق به SKYLINE NETWORKING TECH LLC نیست، توسط آن اداره نمی‌شود، مجوز یا تأیید آن را ندارد و هیچ ارتباطی با SkylineVPN ندارد. از آن بازدید نکنید، اطلاعات حساب کاربری، اطلاعات پرداخت یا اطلاعات شخصی خود را در آن وارد نکنید و هیچ نرم‌افزاری از آن دانلود نکنید. ما هیچ مسئولیتی در قبال خسارات ناشی از استفاده از این وب‌سایت نمی‌پذیریم. اگر قبلاً اطلاعاتی در آن وارد کرده‌اید، فوراً رمز عبور خود را تغییر دهید و از طریق وب‌سایت رسمی با پشتیبانی تماس بگیرید.

> [!IMPORTANT]
> **تنها وب‌سایت رسمی [www.skylinevpn.com](https://www.skylinevpn.com) است.** مراقب سایت‌های جعلی باشید.
>
> **خرید اشتراک در کلاینت CLI امکان‌پذیر نیست.** لطفاً ابتدا از [www.skylinevpn.com](https://www.skylinevpn.com) اشتراک تهیه کنید، سپس با همان حساب کاربری وارد شوید.

## پیش‌نیازها

| پلتفرم | سیستم‌های پشتیبانی‌شده |
|---|---|
| Linux | Ubuntu 22.04+ / Debian 12+ · amd64, arm64 |
| macOS | macOS 12+ · Intel و Apple Silicon |
| Windows | Windows 10+ · x64 |

## نصب

### macOS

ترمینال را باز کنید و دستور زیر را اجرا کنید:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-macos-install.sh | sudo bash
```

### Windows

روی **PowerShell** راست‌کلیک کنید ← **Run as administrator**، سپس دستور زیر را اجرا کنید:

```powershell
iwr -UseBasicParsing https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-windows-install.ps1 -OutFile $env:TEMP\skyline-install.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\skyline-install.ps1
```

### Linux

ترمینال را باز کنید و دستور زیر را اجرا کنید:

```bash
curl -fsSL https://github.com/skyline-projext/skylinevpn-cli/releases/latest/download/skyline-linux-install.sh | sudo bash
```

نصب‌کننده معماری سیستم را تشخیص می‌دهد، checksum از نوع SHA-256 را بررسی می‌کند، سرویس پس‌زمینه را نصب می‌کند و زبان نمایش را از شما می‌پرسد. برای تعیین زبان از ابتدا، `| sudo bash -s -- --lang en` (macOS / Linux) یا `-Lang en` (Windows) را به انتهای دستور اضافه کنید؛ برای زبان چینی از `zh` استفاده کنید.

## استفاده

```bash
skyline login            # ورود با حساب SkylineVPN
skyline nodes            # فهرست نودها
skyline connect 3        # اتصال به نود شماره 3 (یا: skyline connect --best)
skyline status           # نمایش وضعیت اتصال
skyline disconnect       # قطع اتصال
```

| دستور | توضیحات |
|---|---|
| `skyline mode smart` / `skyline mode global` | مسیریابی هوشمند / حالت سراسری |
| `skyline nodes --refresh` | به‌روزرسانی فهرست نودها |
| `skyline me` | اطلاعات حساب |
| `skyline lang english` / `skyline lang chinese` | تغییر زبان نمایش |
| `skyline logout` | خروج از حساب (`--purge` اطلاعات ورود ذخیره‌شده را نیز حذف می‌کند) |
| `skyline version` | اطلاعات نسخه |
| `skyline --help` | همهٔ دستورات |

> در Windows، پس از نصب یک پنجرهٔ ترمینال **جدید** باز کنید. در Linux، یک بار از سیستم خارج شوید و دوباره وارد شوید تا `skyline` بدون `sudo` کار کند.

## به‌روزرسانی

دستور نصب را دوباره اجرا کنید — این دستور همیشه آخرین نسخه را دریافت می‌کند.

## حذف نصب

| پلتفرم | دستور |
|---|---|
| Linux | `sudo apt-get remove skyline-cli` (برای حذف داده‌ها و لاگ‌ها نیز از `purge` استفاده کنید) |
| macOS | `sudo /usr/local/lib/skyline/uninstall.sh` (برای حذف داده‌ها و لاگ‌ها نیز `--purge` را اضافه کنید) |
| Windows (مدیر سیستم) | `powershell -ExecutionPolicy Bypass -File "$env:ProgramFiles\Skyline CLI\uninstall.ps1"` (برای حذف داده‌ها و لاگ‌ها نیز `-Purge` را اضافه کنید) |

## نصب آفلاین و اعتبارسنجی

همهٔ بسته‌ها و نصب‌کننده‌ها به همراه `SHA256SUMS.txt` در صفحهٔ [Releases](https://github.com/skyline-projext/skylinevpn-cli/releases/latest) در دسترس هستند.

- **Linux:** فایل `skyline-linux-cli-universal-*.tar.gz` را دانلود و از حالت فشرده خارج کنید، سپس `sudo bash <extracted-folder>/install.sh` را اجرا کنید.
- **macOS:** فایل `.pkg` و `skyline-macos-install.sh` را در یک پوشه دانلود کنید و `sudo bash skyline-macos-install.sh` را در همان پوشه اجرا کنید.
- **Windows:** فایل `skyline-windows-cli-amd64-*.zip` را دانلود و از حالت فشرده خارج کنید، سپس روی `install.cmd` دوبار کلیک کنید.

`bash skyline-linux-install.sh --check <file>` / `bash skyline-macos-install.sh --check <file>` یک بسته را بدون نصب، اعتبارسنجی می‌کند.

## عیب‌یابی

- **VPS / کانتینر Linux:** وجود `/dev/net/tun` الزامی است. TUN/TAP را در پنل VPS خود فعال کنید، یا کانتینر را با `--device /dev/net/tun --cap-add NET_ADMIN` اجرا کنید.
- **macOS:** اگر پیام «Background item added» را دیدید، در *System Settings → General → Login Items & Extensions* به `skyline` اجازه دهید.
- **لاگ‌ها:** Linux `/var/log/skyline/` · macOS `/Library/Logs/Skyline/` · Windows `%ProgramData%\Skyline CLI\logs`

## پشتیبانی

اشتراک، پرداخت و پشتیبانی: **[www.skylinevpn.com](https://www.skylinevpn.com)** (تنها وب‌سایت رسمی).

---

© 2026 SKYLINE NETWORKING TECH LLC. تمامی حقوق محفوظ است. برای جزئیات، [LICENSE](LICENSE) را ببینید.
