#!/bin/bash
# Cloudflare WARP + Tray Icon installer for Linux Mint 22 (Cinnamon)
# https://github.com/altairscorpio/cloudflare-warp-vpn-linux

set -e

echo "================================================"
echo " Cloudflare WARP installer for Linux Mint 22"
echo "================================================"
echo ""

# 1. Add Cloudflare GPG key
echo "[1/6] Adding Cloudflare GPG key..."
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg

# 2. Add repository (force Ubuntu Noble codename — Mint uses its own codename which is not supported)
echo "[2/6] Adding Cloudflare APT repository..."
echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ noble main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list

# 3. Install cloudflare-warp and tray dependencies
echo "[3/6] Installing Cloudflare WARP and dependencies..."
sudo apt-get update -qq
sudo apt-get install -y cloudflare-warp python3-gi gir1.2-xapp-1.0 gir1.2-gtk-3.0

# 4. Enable and start warp-svc
echo "[4/6] Enabling and starting warp-svc..."
sudo systemctl enable warp-svc
sudo systemctl start warp-svc

# 5. Install tray app
echo "[5/6] Installing WARP tray icon..."
mkdir -p ~/.local/bin
cp warp-tray.py ~/.local/bin/warp-tray
chmod +x ~/.local/bin/warp-tray

# 6. Add to autostart
echo "[6/6] Adding to autostart..."
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/warp-tray.desktop << EOF
[Desktop Entry]
Name=Cloudflare WARP Tray
Comment=Cloudflare WARP tray icon
Exec=/home/$USER/.local/bin/warp-tray
Icon=network-vpn
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=5
EOF

echo ""
echo "================================================"
echo " Installation complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Register WARP:   warp-cli registration new"
echo "  2. Connect:         warp-cli connect"
echo "  3. Start tray icon: warp-tray &"
echo ""
echo "The tray icon will start automatically on next login."
