# pages/budgetUI.py

import customtkinter
from customtkinter import (
    CTkFrame, CTkLabel, CTkButton, CTkEntry,
    CTkScrollableFrame
)
from tkinter import messagebox


class BudgetUI(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

        # ---------------------------
        # TITLE
        # ---------------------------
        CTkLabel(self, text="Budget Tracker",
                 font=("Arial", 24, "bold")).grid(
            row=0, column=0, pady=20
        )

        # ---------------------------
        # SCROLL AREA FOR BUDGET ITEMS
        # ---------------------------
        self.items_frame = CTkScrollableFrame(self, fg_color="#1e1e1e", corner_radius=10)
        self.items_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.items_frame.grid_columnconfigure(0, weight=1)

        # ---------------------------
        # ENTRY FIELDS
        # ---------------------------
        self.entry_item = CTkEntry(self, placeholder_text="Item name")
        self.entry_item.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 5))

        self.entry_amount = CTkEntry(self, placeholder_text="Amount (RM)")
        self.entry_amount.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

        # ---------------------------
        # BUTTONS
        # ---------------------------
        CTkButton(self, text="Add Expense", command=self.add_item).grid(
            row=4, column=0, padx=20, pady=5, sticky="ew"
        )

        CTkButton(self, text="Refresh List", command=self.refresh).grid(
            row=5, column=0, padx=20, pady=5, sticky="ew"
        )

        # TOTAL LABEL
        self.total_label = CTkLabel(self, text="Total: RM 0", font=("Arial", 18, "bold"))
        self.total_label.grid(row=6, column=0, pady=10)

        # Load existing data
        self.refresh()

    # ------------------------------------------------
    # ADD ITEM
    # ------------------------------------------------

    def add_item(self):
        item = self.entry_item.get().strip()
        amount = self.entry_amount.get().strip()

        if not item or not amount:
            messagebox.showerror("Error", "Item and amount cannot be empty.")
            return

        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        self.controller.add(item, amount)

        self.entry_item.delete(0, "end")
        self.entry_amount.delete(0, "end")

        self.refresh()

    # ------------------------------------------------
    # REMOVE ITEM
    # ------------------------------------------------

    def remove_item(self, item_name):
        self.controller.remove(item_name)
        self.refresh()

    # ------------------------------------------------
    # REFRESH DISPLAY
    # ------------------------------------------------

    def refresh(self):
        # clear frame
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        items = self.controller.get_items()

        for index, obj in enumerate(items):
            row_frame = CTkFrame(self.items_frame, fg_color="#2a2a2a", corner_radius=10)
            row_frame.grid(row=index, column=0, sticky="ew", padx=5, pady=5)
            row_frame.grid_columnconfigure(0, weight=1)

            CTkLabel(row_frame, text=f"{obj.item} - RM {obj.amount}",
                     anchor="w", font=("Arial", 15)).grid(
                row=0, column=0, sticky="w", padx=10, pady=10
            )

            CTkButton(row_frame, text="Delete", width=70,
                      command=lambda name=obj.item: self.remove_item(name)).grid(
                row=0, column=1, padx=10
            )

        # update total
        total = self.controller.total()
        self.total_label.configure(text=f"Total: RM {total:.2f}")
