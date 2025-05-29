# ui/app.py
import customtkinter as ctk
import ctypes
from ui.device_card import DeviceCard
from ui.filter_panel import FilterPanel
from utils.device_scanner import get_devices
from utils.storage import load_metadata, save_metadata

def launch_app():
    app = ctk.CTk()
    app.title("Ultra Device Manager")
    app.geometry("1000x800")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(2, weight=1)

    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    label = ctk.CTkLabel(app, text="🛡️ Admin Mode: ON" if is_admin else "⚠️ Admin Mode: OFF",
                         text_color="#00FF99" if is_admin else "#FFCC00",
                         font=("Segoe UI", 12, "bold"))
    label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

    metadata = load_metadata()
    devices = get_devices(include_hidden=True)

    card_frame = ctk.CTkScrollableFrame(app)
    card_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 15))

    device_cards = []

    def apply_filters():
        filters = {
            "search": filter_panel.search_var.get().strip().lower(),
            "tag": filter_panel.tag_var.get().strip().lower(),
            "status": filter_panel.status_var.get().strip().lower(),
            "show_hidden": filter_panel.show_hidden_var.get()
        }

        for widget in card_frame.winfo_children():
            widget.destroy()

        filtered_devices = []
        for device in devices:
            name = device["name"].lower()
            status = device["status"].lower()
            device_id = device["device_id"]
            tag = metadata.get(device_id, {}).get("tag", "").lower()
            hidden = device.get("hidden", False)

            if filters["search"] and filters["search"] not in name:
                continue
            if filters["tag"] and filters["tag"] != tag:
                continue
            if filters["status"] != "all" and filters["status"] not in status:
                continue
            if not filters["show_hidden"] and hidden:
                continue

            filtered_devices.append(device)

        tags = []
        for device in filtered_devices:
            t = metadata.get(device["device_id"], {}).get("tag", "")
            if t:
                tags.append(t)

        filter_panel.update_tags(tags)

        for device in filtered_devices:
            card = DeviceCard(card_frame, device, metadata, filter_callback=apply_filters,
                              tag_update_callback=lambda: filter_panel.update_tags([metadata.get(d["device_id"], {}).get("tag", "") for d in devices]))
            card.pack(padx=10, pady=5, fill="x")

    filter_panel = FilterPanel(app, apply_filters_callback=apply_filters, clear_callback=apply_filters)
    filter_panel.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))

    apply_filters()
    app.mainloop()
