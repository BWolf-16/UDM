import customtkinter as ctk

class FilterPanel(ctk.CTkFrame):
    def __init__(self, parent, on_filter):
        super().__init__(parent, corner_radius=12)
        self.on_filter = on_filter

        self.search_var = ctk.StringVar()
        self.tag_var = ctk.StringVar()
        self.status_var = ctk.StringVar()

        self.grid_columnconfigure((1, 3, 5), weight=1)

        # Search
        ctk.CTkLabel(self, text="🔍", font=("Segoe UI", 14)).grid(row=0, column=0, padx=(10, 5), sticky="e")
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Search name...")
        self.search_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Tag
        ctk.CTkLabel(self, text="🏷️", font=("Segoe UI", 14)).grid(row=0, column=2, padx=(10, 5), sticky="e")
        self.tag_entry = ctk.CTkEntry(self, textvariable=self.tag_var, placeholder_text="Filter tag only...")
        self.tag_entry.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="ew")

        # Status
        ctk.CTkLabel(self, text="📊", font=("Segoe UI", 14)).grid(row=0, column=4, padx=(10, 5), sticky="e")
        self.status_menu = ctk.CTkOptionMenu(
            self,
            variable=self.status_var,
            values=["", "OK", "Warning", "Disabled", "Degraded", "Unknown"]
        )
        self.status_menu.grid(row=0, column=5, padx=(0, 10), pady=10, sticky="ew")

        # Apply Button
        self.apply_btn = ctk.CTkButton(self, text="🎯 Apply Filters", command=self.apply_filters)
        self.apply_btn.grid(row=0, column=6, padx=(5, 10), pady=10)

    def apply_filters(self):
        filters = {
            "search": self.search_var.get().strip().lower(),
            "tag": self.tag_var.get().strip().lower(),
            "status": self.status_var.get().strip().lower(),
        }
        self.on_filter(filters)
