# pages/budgetUI.py

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton

class BudgetUI(CTkFrame):
    def __init__(self, parent, controller, back_target=None):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target

        self.columnconfigure(0, weight=1)

        # Title
        CTkLabel(self, text="Budget Tracker", font=("Arial", 22, "bold")).grid(
            row=0, column=0, pady=20
        )

        # Scrollable List
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="#202020")
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.list_frame.columnconfigure(0, weight=1)

        # Input Fields
        self.entry_name = CTkEntry(self, placeholder_text="Item name")
        self.entry_amount = CTkEntry(self, placeholder_text="Amount (RM)")

        self.entry_name.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        self.entry_amount.grid(row=3, column=0, pady=5, padx=20, sticky="ew")

        # Add Button
        self.btn_add = CTkButton(self, text="Add Item", command=self.add_item)
        self.btn_add.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

        # Back Button
        if self.back_target:
            CTkButton(
                self, text="Back to Home", fg_color="#444444",
                command=lambda: self.back_target.tkraise()
            ).grid(row=5, column=0, pady=15, padx=20, sticky="ew")

        self.refresh_items()

    # ------------------------------------
    # Add New Item
    # ------------------------------------
    def add_item(self):
        name = self.entry_name.get().strip()
        amount = self.entry_amount.get().strip()

        if name == "" or amount == "":
            return  # ignore empty input

        self.controller.add_budget_item(name, float(amount))
        self.entry_name.delete(0, "end")
        self.entry_amount.delete(0, "end")

        self.refresh_items()

    # ------------------------------------
    # Delete Item
    # ------------------------------------
    def delete_item(self, item_name):
        self.controller.remove_budget_item(item_name)
        self.refresh_items()

    # ------------------------------------
    # Refresh UI
    # ------------------------------------
    def refresh_items(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = self.controller.get_budget_items()

        for i, item in enumerate(items):
            row = CTkFrame(self.list_frame, fg_color="#2A2A2A", corner_radius=8)
            row.grid(row=i, column=0, sticky="ew", padx=10, pady=5)

            CTkLabel(row, text=f"{item.name}", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            CTkLabel(row, text=f"RM {item.amount:.2f}", anchor="e").grid(row=0, column=1, padx=10, pady=5, sticky="e")

            # Delete Button
            CTkButton(
                row, text="Delete", width=70,
                fg_color="#803434",
                command=lambda name=item.name: self.delete_item(name)
            ).grid(row=0, column=2, padx=10, pady=5)
