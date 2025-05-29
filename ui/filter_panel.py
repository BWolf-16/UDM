
import customtkinter as ctk

class FilterPanel(ctk.CTkFrame):
    def __init__(self, parent, apply_filters_callback=None, clear_callback=None):
        super().__init__(parent, corner_radius=12)
        self.apply_filters_callback = apply_filters_callback
        self.clear_callback = clear_callback

        self.search_var = ctk.StringVar(value="")
        self.tag_var = ctk.StringVar(value="")
        self.status_var = ctk.StringVar(value="All")
        self.show_hidden_var = ctk.BooleanVar(value=False)

        self.grid_columnconfigure((1, 3, 5), weight=1)

        # Search
        ctk.CTkLabel(self, text="🔍", font=("Segoe UI", 14)).grid(row=0, column=0, padx=(10, 5), sticky="e")
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Search device name...")
        self.search_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Tag Dropdown
        ctk.CTkLabel(self, text="🏷️", font=("Segoe UI", 14)).grid(row=0, column=2, padx=(10, 5), sticky="e")
        self.tag_menu = ctk.CTkOptionMenu(self, variable=self.tag_var, values=[""])
        self.tag_menu.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="ew")
        self.tag_menu.set("")

        # Status Dropdown
        ctk.CTkLabel(self, text="📊", font=("Segoe UI", 14)).grid(row=0, column=4, padx=(10, 5), sticky="e")
        self.status_menu = ctk.CTkOptionMenu(
            self,
            variable=self.status_var,
            values=[
                "All", "Enabled", "Working", "Warning", "Disabled",
                "Degraded", "Unknown", "Error", "Suspended", "Not Present"
            ]
        )
        self.status_menu.set("All")
        self.status_menu.grid(row=0, column=5, padx=(0, 10), pady=10, sticky="ew")

        # Buttons
        self.apply_btn = ctk.CTkButton(self, text="🎯 Apply Filters", command=self.apply_filters)
        self.apply_btn.grid(row=0, column=6, padx=(5, 2), pady=10)

        self.clear_btn = ctk.CTkButton(self, text="🧹 Clear Filters", command=self.clear_filters)
        self.clear_btn.grid(row=0, column=7, padx=(2, 10), pady=10)

        # Show Hidden Devices Checkbox
        self.show_hidden_checkbox = ctk.CTkCheckBox(
            self,
            text="👻 Show Hidden Devices",
            variable=self.show_hidden_var,
            command=self.apply_filters
        )
        self.show_hidden_checkbox.grid(row=1, column=0, columnspan=8, sticky="w", padx=15, pady=(0, 10))

    def apply_filters(self):
        if self.apply_filters_callback:
            self.apply_filters_callback()

    def clear_filters(self):
        self.search_var.set("")
        self.tag_var.set("")
        self.tag_menu.set("")
        self.status_var.set("All")
        self.status_menu.set("All")
        self.show_hidden_var.set(False)
        if self.clear_callback:
            self.clear_callback()

    def update_tags(self, tags):
        unique_tags = sorted(set(t for t in tags if t.strip()), key=lambda x: x.lower())
        self.tag_menu.configure(values=[""] + unique_tags)
        self.tag_menu.set("")
