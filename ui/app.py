# ui/app.py
import customtkinter as ctk
from ui.device_card import DeviceCard
from ui.filter_panel import FilterPanel
from core.device_scanner import get_device_list
from utils.storage import load_metadata, save_metadata

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

    content_frame = ctk.CTkScrollableFrame(app, width=1080, height=660)
    content_frame.pack(pady=5, padx=10, fill='both', expand=True)

    def apply_filters(filters):
        any_filter = filters['search'] or filters['tag'] or filters['status']
        for card in card_widgets:
            name = card.nickname.lower()
            tag = card.device_meta.get("tag", "").lower()
            status = card.device['status'].lower()

            match = (
                (not filters['search'] or filters['search'] in name) and
                (not filters['tag'] or filters['tag'] in tag) and
                (not filters['status'] or filters['status'] in status)
            )

            if not any_filter or match:
                card.pack(pady=5, padx=5, fill='x')
            else:
                card.pack_forget()

    filter_panel = FilterPanel(filter_frame, on_filter=apply_filters)
    filter_panel.pack(fill='x')

    def update_tag_filter():
        tag_list = [card.device_meta.get("tag", "") for card in card_widgets if card.device_meta.get("tag", "")]
        if hasattr(filter_panel, "update_tags"):
            filter_panel.update_tags(tag_list)

    for device in devices:
        card = DeviceCard(
            content_frame,
            device,
            metadata,
            filter_callback=lambda: apply_filters({
                'search': filter_panel.search_var.get().strip().lower(),
                'tag': filter_panel.tag_var.get().strip().lower(),
                'status': filter_panel.status_var.get().strip().lower(),
            }),
            tag_update_callback=update_tag_filter
        )
        card.pack(pady=5, padx=5, fill='x')
        card_widgets.append(card)

    update_tag_filter()
    app.mainloop()
