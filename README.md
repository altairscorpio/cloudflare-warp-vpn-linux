# Cloudflare WARP for Linux Mint 22 (Cinnamon)

A simple system tray icon for controlling Cloudflare WARP VPN on Linux Mint 22 (Cinnamon desktop).

> ⚠️ **Note:** Linux Mint uses its own release codenames (e.g. `zena`) which are **not supported** by Cloudflare's APT repository. This installer always uses the Ubuntu base codename (`noble`) which works correctly.

## Features

- 🔒 Tray icon showing WARP connected / disconnected status
- 🖱️ Click to open menu — connect, disconnect, or quit
- 🌐 English and Lithuanian language support (saved between sessions)
- 🔄 Status auto-refreshes every 3 seconds
- 🚀 Starts automatically on login

## Requirements

- Linux Mint 22.x (Ubuntu 24.04 Noble base)
- Cinnamon desktop
- Internet connection

## Installation

```bash
git clone https://github.com/altairscorpio/cloudflare-warp-vpn-linux.git
cd cloudflare-warp-vpn-linux
chmod +x install.sh
./install.sh
```

After installation, register and connect:

```bash
warp-cli registration new   # opens browser to register
warp-cli connect
warp-tray &                 # start tray icon (auto-starts on next login)
```

## Usage

| Action | Result |
|--------|--------|
| Click tray icon | Opens menu |
| Menu → Connect WARP | Connects to WARP |
| Menu → Disconnect WARP | Disconnects from WARP |
| Menu → 🌐 Language | Switch between English / Lietuvių |
| Menu → Quit | Closes the tray app |

## Useful Commands

```bash
warp-cli status                  # check current status
warp-cli connect                 # connect
warp-cli disconnect              # disconnect
warp-cli registration show       # show registration info
sudo systemctl status warp-svc  # check WARP service
```

## Troubleshooting

**Tray icon not appearing?**
```bash
sudo systemctl start warp-svc
warp-tray &
```

**`warp-cli` errors after fresh install?**
```bash
sudo systemctl enable warp-svc
sudo systemctl start warp-svc
warp-cli registration new
```

**Wrong Ubuntu codename error (404)?**
Make sure `/etc/apt/sources.list.d/cloudflare-client.list` contains `noble`, not your Mint codename.

## How It Works

- Uses **XApp.StatusIcon** — the only reliably working tray API for Cinnamon desktop
- AppIndicator3 / AyatanaAppIndicator3 are **not used** as they do not work reliably on Cinnamon
- Language preference saved to `~/.config/warp-tray.json`
- Autostart configured via `~/.config/autostart/warp-tray.desktop`

## Tested On

- Linux Mint 22.3 "Zena" — Cinnamon desktop
