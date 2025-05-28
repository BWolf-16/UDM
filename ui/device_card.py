# ui/device_card.py
import customtkinter as ctk
from core.status_controller import enable_device, disable_device, restart_device
from utils.storage import save_metadata
from datetime import datetime
import subprocess
import os
import wmi

class DeviceCard(ctk.CTkFrame):
    def __init__(self, parent, device, metadata, filter_callback=None, tag_update_callback=None):
        super().__init__(parent, corner_radius=12)
        self.device = device
        self.metadata = metadata
        self.device_meta = self.metadata.get(device['device_id'], {})
        self.filter_callback = filter_callback
        self.tag_update_callback = tag_update_callback

        self.nickname = self.device_meta.get("nickname", device['name'])
        self.text_color = self.device_meta.get("text_color", "#ffffff")
        self.tag = self.device_meta.get("tag", "")

        self.configure(border_color="#AAAAAA", border_width=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text=self.nickname, font=("Segoe UI", 14, "bold"), text_color=self.text_color)
        self.label.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 5))
        self.label.bind("<Button-1>", lambda e: self.toggle_color_section())

        self.status_label = ctk.CTkButton(self, text=self.get_status_label(), width=130,
                                          fg_color=self.status_color(self.device['status']), command=self.show_status_actions)
        self.status_label.grid(row=0, column=1, sticky='e', padx=10)

        self.tag_button = ctk.CTkButton(self, text=f"🏷 {self.tag or 'Set Tag'}", width=100,
                                        fg_color=self.text_color if self.text_color != "#ffffff" else "#1E88E5",
                                        text_color="#ffffff", command=self.edit_tag)
        self.tag_button.grid(row=0, column=2, sticky='e', padx=10)

        self.advanced_toggle = ctk.CTkButton(self, text="⚙️ Advanced ▼", width=100, command=self.toggle_advanced)
        self.advanced_toggle.grid(row=0, column=3, sticky='e', padx=10)

        self.color_section = ctk.CTkFrame(self)
        self.color_section.grid(row=1, column=0, columnspan=4, sticky='w', padx=15, pady=(0, 5))
        self.color_section.grid_remove()
        self.add_color_buttons()

        self.advanced_section = ctk.CTkFrame(self)
        self.advanced_section.grid(row=1, column=0, columnspan=4, sticky='ew', padx=15, pady=0)
        self.advanced_section.grid_remove()
        self.add_advanced_buttons()

    def get_status_label(self):
        s = self.device['status'].lower()
        if "disable" in s:
            return "❌ Disabled"
        elif "ok" in s or "enable" in s or "working" in s:
            return "✔ Enabled"
        return "⚠ Unknown"

    def status_color(self, status):
        s = status.lower()
        if "ok" in s or "working" in s or "enable" in s:
            return "#4CAF50"
        elif "disable" in s:
            return "#F44336"
        return "#9E9E9E"

    def show_status_actions(self):
        if hasattr(self, "status_menu") and self.status_menu.winfo_exists():
            self.status_menu.destroy()
            return

        self.status_menu = ctk.CTkFrame(self)
        self.status_menu.grid(row=2, column=1, sticky='e', padx=10, pady=5)

        def act(label, func):
            try:
                func(self.device['device_id'])
                self.device['status'] = label
                self.status_label.configure(text=self.get_status_label(), fg_color=self.status_color(label))
                self.add_history(f"Device {label.lower()}")
            except Exception as e:
                self.status_label.configure(text="⚠ Failed")
                self.add_history(f"Failed: {e}")
            self.status_menu.destroy()
            if self.filter_callback:
                self.filter_callback()

        current = self.device['status'].lower()
        if "disable" in current:
            ctk.CTkButton(self.status_menu, text="🟢 Enable Device", command=lambda: act("Enabled", enable_device)).pack(padx=5, pady=2)
        else:
            ctk.CTkButton(self.status_menu, text="🔴 Disable Device", command=lambda: act("Disabled", disable_device)).pack(padx=5, pady=2)
        ctk.CTkButton(self.status_menu, text="🔁 Restart Device", command=lambda: act("Restarted", restart_device)).pack(padx=5, pady=2)

    def toggle_color_section(self):
        if self.color_section.winfo_ismapped():
            self.color_section.grid_remove()
        else:
            self.color_section.grid()

    def toggle_advanced(self):
        if self.advanced_section.winfo_ismapped():
            self.advanced_section.grid_remove()
        else:
            self.advanced_section.grid()

    def add_color_buttons(self):
        colors = ["#ffffff", "#1E88E5", "#C2185B", "#43A047", "#FDD835", "#F4511E","#AC05FF"]
        for c in colors:
            ctk.CTkButton(self.color_section, text=c, text_color=c, fg_color="transparent",
                          command=lambda col=c: self.set_text_color(col)).pack(side="left", padx=5, pady=5)

    def set_text_color(self, color):
        self.text_color = color
        self.device_meta["text_color"] = color
        self.metadata[self.device['device_id']] = self.device_meta
        save_metadata(self.metadata)
        self.label.configure(text_color=color)
        self.tag_button.configure(fg_color=color)
        self.add_history(f"Set label color to {color}")

    def add_advanced_buttons(self):
        actions = [
            ("📂", self.open_driver_folder),
            ("🧬", self.open_registry_location),
            ("⚙️", self.open_device_properties),
            ("🔄", self.refresh_device),
            ("🔍", self.search_driver_update),
        ]
        for icon, cmd in actions:
            ctk.CTkButton(self.advanced_section, text=icon, width=40, height=32, command=cmd).pack(side="right", padx=4, pady=2)

    def edit_tag(self):
        if hasattr(self, "tag_edit") and self.tag_edit.winfo_exists():
            self.tag_edit.destroy()
            return

        self.tag_edit = ctk.CTkFrame(self)
        self.tag_edit.grid(row=2, column=2, columnspan=2, sticky='e', padx=10, pady=5)

        entry = ctk.CTkEntry(self.tag_edit, width=150)
        entry.insert(0, self.tag)
        entry.pack(side='left', padx=5)

        def save():
            new_tag = entry.get().strip()
            self.tag = new_tag
            self.device_meta["tag"] = new_tag
            self.metadata[self.device['device_id']] = self.device_meta
            save_metadata(self.metadata)
            self.tag_button.configure(text=f"🏷 {new_tag or 'Set Tag'}")
            self.add_history(f"Updated tag to '{new_tag}'")
            self.tag_edit.destroy()
            if self.tag_update_callback:
                self.tag_update_callback()

        ctk.CTkButton(self.tag_edit, text="Save", command=save).pack(side='left')

    def open_driver_folder(self):
        try:
            w = wmi.WMI()
            for d in w.Win32_PnPSignedDriver():
                if d.DeviceID == self.device['device_id']:
                    path = os.path.join(os.environ['windir'], 'INF', d.InfName)
                    if os.path.exists(path):
                        subprocess.Popen(['explorer', '/select,', path])
                        return
            raise Exception("Driver not found")
        except Exception as e:
            print("Driver folder error:", e)

    def open_registry_location(self):
        try:
            device_id = self.device['device_id']
            key = f"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\{device_id}"
            subprocess.Popen(["regedit"])
        except Exception as e:
            print("Registry error:", e)

    def open_device_properties(self):
        subprocess.run(["devmgmt.msc"], shell=True)

    def refresh_device(self):
        subprocess.run("pnputil /scan-devices", shell=True)
        self.add_history("Refreshed device list")

    def search_driver_update(self):
        subprocess.run("ms-settings:windowsupdate", shell=True)
        self.add_history("Opened driver update UI")

    def add_history(self, event):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history = self.device_meta.get("history", [])
        history.append(f"[{now}] {event}")
        self.device_meta["history"] = history
        self.metadata[self.device['device_id']] = self.device_meta
        save_metadata(self.metadata)
