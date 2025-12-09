# ui.py
import customtkinter as ctk

class BudgetUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("Event Planner - Budget Tracker")
        self.root.geometry("450x600")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
        self.budget_menu = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)

        for frame in (self.main_menu, self.budget_menu):
            frame.grid(row=0, column=0, sticky="nsew")

        self.build_main_menu()
        self.build_budget_menu()

        self.show_frame(self.main_menu)

    def show_frame(self, frame):
        frame.tkraise()

    def build_main_menu(self):
        ctk.CTkLabel(self.main_menu, text="EVENT PLANNER", font=("Arial", 26, "bold")).pack(pady=40)
        ctk.CTkButton(self.main_menu,
                      text="Budget Manager",
                      width=200,
                      height=50,
                      command=lambda: self.show_frame(self.budget_menu)).pack(pady=20)

    def build_budget_menu(self):
        container = ctk.CTkFrame(self.budget_menu, fg_color="transparent", corner_radius=0)
        container.place(relx=0.5, rely=0.5, anchor="center")

        header = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
        header.pack(pady=(0, 15))

        ctk.CTkLabel(header, text="EVENT BUDGET MANAGER", font=("Arial", 20, "bold")).pack()
        self.summary_label = ctk.CTkLabel(header,
                                          text="Income: 0.00 | Expense: 0.00 | Balance: 0.00",
                                          font=("Arial", 14))
        self.summary_label.pack(pady=5)

        form = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
        form.pack(pady=15)

        ctk.CTkLabel(form, text="Category:", font=("Arial", 14)).pack(anchor="w")
        self.category_entry = ctk.CTkEntry(form, width=260, corner_radius=8)
        self.category_entry.pack(pady=5)

        ctk.CTkLabel(form, text="Amount:", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
        self.amount_entry = ctk.CTkEntry(form, width=260, corner_radius=8)
        self.amount_entry.pack(pady=5)

        ctk.CTkLabel(form, text="Type:", font=("Arial", 14)).pack(anchor="w", pady=(10, 0))
        self.type_var = ctk.StringVar(value="Expense")
        type_dropdown = ctk.CTkComboBox(form, values=["Income", "Expense"], variable=self.type_var,
                                        width=260, corner_radius=8)
        type_dropdown.pack(pady=5)

        btn_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Add Item", width=180,
                      fg_color="#3A6EA5", hover_color="#ff8800",
                      command=self.controller.add_item).grid(row=0, column=0, padx=5, pady=5)

        ctk.CTkButton(btn_frame, text="View Budget", width=180,
                      fg_color="#3A6EA5", hover_color="#ff8800",
                      command=self.controller.view_budget).grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton(btn_frame, text="Remove Item", width=180,
                      fg_color="#3A6EA5", hover_color="#ff8800",
                      command=self.controller.remove_item).grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkButton(btn_frame, text="Clear Form", width=180,
                      fg_color="#3A6EA5", hover_color="#ff8800",
                      command=self.clear_form).grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(container, text="← Back to Main Menu", width=200,
                      fg_color="#1f6aa5", hover_color="#ff8800",
                      command=lambda: self.show_frame(self.main_menu)).pack(pady=15)

    def clear_form(self):
        self.category_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.type_var.set("Expense")
        self.update_summary()

    def update_summary(self):
        total_income, total_expense, balance = self.controller.service.get_summary()
        self.summary_label.configure(
            text=f"Income: {total_income:.2f} | Expense: {total_expense:.2f} | Balance: {balance:.2f}"
        )