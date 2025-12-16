import customtkinter
from customtkinter      import CTkFrame, CTkLabel, CTkEntry, CTkButton
from .budgetController  import BudgetController

class BudgetUI(CTkFrame):
    def __init__(self, parent, controller: BudgetController, back_target="untitled", splash_key="budget"):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target
        self.splash_key = splash_key
        
        CTkButton(
            self,
            text="ⓘ",
            width=30,
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).pack(side="right")

        # -----------------------
        # HEADER
        # -----------------------
        CTkLabel(self, text="Budget Tracker", font=("Arial", 20, "bold")).pack(pady=10)

        # Back button
        CTkButton(self, text="Back to Home", width=120,
                  command=lambda: back_target.tkraise()).pack(pady=5)

        # -----------------------
        # INPUT FORM
        # -----------------------
        form_frame = CTkFrame(self)
        form_frame.pack(pady=10)

        CTkLabel(form_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = CTkEntry(form_frame, width=180)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        CTkLabel(form_frame, text="Amount (RM):").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = CTkEntry(form_frame, width=180)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        CTkButton(form_frame, text="Add Expense", width=150,
                  command=self.add_item).grid(row=2, column=0, columnspan=2, pady=10)

        # -----------------------
        # LIST AREA
        # -----------------------
        self.items_frame = CTkFrame(self, corner_radius=8)
        self.items_frame.pack(pady=10, fill="both", expand=True)

        # -----------------------
        # TOTAL DISPLAY
        # -----------------------
        self.total_label = CTkLabel(self, text="Total: RM0", font=("Arial", 16, "bold"))
        self.total_label.pack(pady=10)

        self.refresh_list()

    # ----------------------------------------------------
    # ADD ITEM
    # ----------------------------------------------------
    def add_item(self):
        name = self.name_entry.get().strip()
        amount_text = self.amount_entry.get().strip()

        if name == "" or amount_text == "":
            return

        try:
            amount = float(amount_text)
        except ValueError:
            return

        self.controller.add_item(name, amount)

        self.name_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")

        self.refresh_list()

    # ----------------------------------------------------
    # DELETE ITEM
    # ----------------------------------------------------
    def delete_item(self, index):
        self.controller.delete_item(index)
        self.refresh_list()

    # ----------------------------------------------------
    # REFRESH LIST + TOTAL
    # ----------------------------------------------------
    def refresh_list(self):
        # Clear old rows
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        items = self.controller.get_items()

        for index, item in enumerate(items):
            row = CTkFrame(self.items_frame)
            row.pack(fill="x", pady=3, padx=5)

            CTkLabel(row, text=item.name, width=200, anchor="w").pack(side="left", padx=10)
            CTkLabel(row, text=f"RM {item.amount}", width=120).pack(side="left")

            del_btn = CTkButton(row, text="Delete", width=80,
                                command=lambda i=index: self.delete_item(i))
            del_btn.pack(side="right", padx=10)

        self.update_total()

    # ----------------------------------------------------
    # SHOW TOTAL
    # ----------------------------------------------------
    def update_total(self):
        total = self.controller.get_total()
        self.total_label.configure(text=f"Total: RM{total}")
