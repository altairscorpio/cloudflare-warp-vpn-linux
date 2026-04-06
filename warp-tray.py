#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('XApp', '1.0')
from gi.repository import Gtk, XApp, GLib
import subprocess
import os
import json

# --- Translations ---
TRANSLATIONS = {
    "en": {
        "checking": "Checking status...",
        "connected": "✅ WARP CONNECTED",
        "disconnected": "❌ WARP DISCONNECTED",
        "connect": "Connect WARP",
        "disconnect": "Disconnect WARP",
        "tooltip_on": "WARP: Connected",
        "tooltip_off": "WARP: Disconnected",
        "language": "🌐 Language",
        "quit": "Quit",
    },
    "lt": {
        "checking": "Tikrinamas statusas...",
        "connected": "✅ WARP ĮJUNGTAS",
        "disconnected": "❌ WARP IŠJUNGTAS",
        "connect": "Įjungti WARP",
        "disconnect": "Išjungti WARP",
        "tooltip_on": "WARP: Įjungtas",
        "tooltip_off": "WARP: Išjungtas",
        "language": "🌐 Kalba",
        "quit": "Išeiti",
    }
}

CONFIG_FILE = os.path.expanduser("~/.config/warp-tray.json")

def load_lang():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f).get("lang", "en")
        except Exception:
            pass
    return "en"

def save_lang(lang):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"lang": lang}, f)

class WarpTray:
    def __init__(self):
        self.lang = load_lang()
        self.t = TRANSLATIONS[self.lang]

        self.icon = XApp.StatusIcon()
        self.icon.set_icon_name("nm-vpn-standalone-lock")
        self.icon.set_tooltip_text(self.t["tooltip_off"])

        self.menu = Gtk.Menu()

        # Status
        self.status_item = Gtk.MenuItem(label=self.t["checking"])
        self.status_item.set_sensitive(False)
        self.menu.append(self.status_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Connect / Disconnect
        self.toggle_item = Gtk.MenuItem(label=self.t["connect"])
        self.toggle_item.connect("activate", self.toggle_warp)
        self.menu.append(self.toggle_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Language submenu
        lang_item = Gtk.MenuItem(label=self.t["language"])
        lang_submenu = Gtk.Menu()

        en_item = Gtk.RadioMenuItem(label="English")
        lt_item = Gtk.RadioMenuItem.new_with_label_from_widget(en_item, "Lietuvių")

        if self.lang == "lt":
            lt_item.set_active(True)
        else:
            en_item.set_active(True)

        en_item.connect("activate", lambda w: self.set_language("en") if w.get_active() else None)
        lt_item.connect("activate", lambda w: self.set_language("lt") if w.get_active() else None)

        lang_submenu.append(en_item)
        lang_submenu.append(lt_item)
        lang_item.set_submenu(lang_submenu)
        self.menu.append(lang_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # Quit
        self.quit_item = Gtk.MenuItem(label=self.t["quit"])
        self.quit_item.connect("activate", lambda w: Gtk.main_quit())
        self.menu.append(self.quit_item)

        self.menu.show_all()
        self.icon.set_primary_menu(self.menu)
        self.icon.set_secondary_menu(self.menu)

        GLib.timeout_add_seconds(3, self.update_status)
        self.update_status()

    def set_language(self, lang):
        self.lang = lang
        self.t = TRANSLATIONS[lang]
        save_lang(lang)
        self.quit_item.set_label(self.t["quit"])
        self.update_status()

    def run(self, cmd):
        try:
            r = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            return r.stdout.strip() + r.stderr.strip()
        except Exception:
            return ""

    def update_status(self):
        output = self.run("warp-cli status 2>&1")
        if "Connected" in output:
            self.icon.set_icon_name("network-vpn")
            self.icon.set_tooltip_text(self.t["tooltip_on"])
            self.status_item.set_label(self.t["connected"])
            self.toggle_item.set_label(self.t["disconnect"])
        else:
            self.icon.set_icon_name("nm-vpn-standalone-lock")
            self.icon.set_tooltip_text(self.t["tooltip_off"])
            self.status_item.set_label(self.t["disconnected"])
            self.toggle_item.set_label(self.t["connect"])
        return True

    def toggle_warp(self, widget):
        output = self.run("warp-cli status 2>&1")
        if "Connected" in output:
            self.run("warp-cli disconnect")
        else:
            self.run("warp-cli connect")
        GLib.timeout_add(1500, self.update_status)

if __name__ == "__main__":
    WarpTray()
    Gtk.main()
