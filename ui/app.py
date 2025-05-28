# ui/app.py
import customtkinter as ctk
from ui.device_card import DeviceCard
from ui.filter_panel import FilterPanel
from core.device_scanner import get_device_list
from utils.storage import load_metadata, save_metadata
import subprocess
import json
import os
from tkinter import filedialog

card_widgets = []

def launch_app():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("1100x800")
    app.title("Ultra Device Manager")

    metadata = load_metadata()
    devices = get_device_list()

    filter_frame = ctk.CTkFrame(app)
    filter_frame.pack(fill='x', padx=10, pady=5)

    content_frame = ctk.CTkScrollableFrame(app, width=1080, height=600)
    content_frame.pack(pady=5, padx=10, fill='both', expand=True)

    def apply_filters(filters):
        for card in card_widgets:
            match = True
            name = card.nickname.lower()
            status = card.device['status'].lower()
            tags = [t.lower() for t in card.device_meta.get("tags", [])]

            if filters['search'] and filters['search'] not in name:
                match = False
            if filters['tag'] and filters['tag'] not in tags:
                match = False
            if filters['status'] and filters['status'] not in status:
                match = False

            card.pack_forget() if not match else card.pack(pady=5, padx=5, fill='x')

    filter_panel = FilterPanel(filter_frame, on_filter=apply_filters)
    filter_panel.pack(fill='x')

    for device in devices:
        card = DeviceCard(content_frame, device, metadata, filter_callback=lambda: apply_filters({
            'search': filter_panel.search_var.get().strip().lower(),
            'tag': filter_panel.tag_var.get().strip().lower(),
            'status': filter_panel.status_var.get().strip().lower(),
        }))
        card.pack(pady=5, padx=5, fill='x')
        card_widgets.append(card)

    def show_history():
        history_window = ctk.CTkToplevel(app)
        history_window.title("Device History Viewer")
        history_window.geometry("600x500")

        for card in card_widgets:
            history = card.device_meta.get("history", [])
            if history:
                label = ctk.CTkLabel(history_window, text=f"📄 {card.nickname}", font=("Arial", 14, "bold"))
                label.pack(anchor='w', padx=10, pady=(10, 0))
                for entry in history:
                    entry_label = ctk.CTkLabel(history_window, text=f"  • {entry}", font=("Arial", 12))
                    entry_label.pack(anchor='w', padx=20)

    def open_properties():
        subprocess.run(["devmgmt.msc"], shell=True)

    def export_metadata():
        export_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if export_path:
            with open(export_path, 'w') as f:
                json.dump(metadata, f, indent=4)

    def import_metadata():
        import_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if import_path and os.path.isfile(import_path):
            with open(import_path, 'r') as f:
                imported_data = json.load(f)
                metadata.update(imported_data)
                save_metadata(metadata)
                app.destroy()
                launch_app()

    button_frame = ctk.CTkFrame(app)
    button_frame.pack(pady=10)

    ctk.CTkButton(button_frame, text="📁 View History Log", command=show_history).pack(side='left', padx=10)
    ctk.CTkButton(button_frame, text="🛠️ Open Device Properties", command=open_properties).pack(side='left', padx=10)
    ctk.CTkButton(button_frame, text="📤 Export Metadata", command=export_metadata).pack(side='left', padx=10)
    ctk.CTkButton(button_frame, text="📥 Import Metadata", command=import_metadata).pack(side='left', padx=10)

    app.mainloop()