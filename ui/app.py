import customtkinter as ctk
import ctypes
from ui.device_card import DeviceCard
from ui.filter_panel import FilterPanel
from utils.device_scanner import get_devices
from utils.storage import load_metadata, save_metadata


def launch_app():
    app = ctk.CTk()
    app.title("Ultra Device Manager")
    app.geometry("1000x750")

    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    label = ctk.CTkLabel(app, text="🛡️ Admin Mode: ON" if is_admin else "⚠️ Admin Mode: OFF",
                         text_color="#00FF99" if is_admin else "#FFCC00",
                         font=("Segoe UI", 12, "bold"))
    label.pack(pady=(10, 0))

    metadata = load_metadata()
    all_devices = get_devices()

    # Frame to hold filters + cards
    content_frame = ctk.CTkFrame(app)
    content_frame.pack(expand=True, fill="both", padx=15, pady=10)

    # Device card container
    card_container = ctk.CTkScrollableFrame(content_frame)
    card_container.pack(fill="both", expand=True, padx=10, pady=10)

    device_cards = []

    def render_devices(filtered=None):
        for widget in card_container.winfo_children():
            widget.destroy()

        shown = filtered if filtered is not None else all_devices
        sorted_devices = sorted(shown, key=lambda d: d['name'].lower())

        for dev in sorted_devices:
            card = DeviceCard(card_container, dev, metadata,
                              filter_callback=apply_filters,
                              tag_update_callback=refresh_tags)
            card.pack(padx=10, pady=6, fill="x")
            device_cards.append(card)

    def refresh_tags():
        tags = list({metadata[dev['device_id']].get("tag", "") for dev in all_devices if metadata.get(dev['device_id'], {}).get("tag", "")})
        filter_panel.update_tags(tags)

    def apply_filters():
        search_term = filter_panel.search_entry.get().strip().lower()
        selected_status = filter_panel.status_var.get()
        selected_tag = filter_panel.tag_var.get()

        def match(dev):
            name = dev['name'].lower()
            tag = metadata.get(dev['device_id'], {}).get("tag", "").lower()
            status = dev['status'].lower()

            return (search_term in name or search_term in tag) and \
                   (selected_tag == "All" or selected_tag.lower() in tag) and \
                   (selected_status == "All" or selected_status.lower() in status)

        filtered = [dev for dev in all_devices if match(dev)]
        render_devices(filtered)

    filter_panel = FilterPanel(app, apply_filters_callback=apply_filters, clear_callback=lambda: render_devices())
    filter_panel.pack(fill="x", padx=15, pady=(0, 10))
    refresh_tags()
    render_devices()

    app.mainloop()
