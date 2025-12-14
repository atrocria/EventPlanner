from customtkinter          import CTkFrame, CTkLabel
from .dashboardController   import DashboardController

#display cards, communicate with each component's services for info
class DashboardUI(CTkFrame):
    def __init__(self, parent, controller: DashboardController):
        super().__init__(parent)
        self.controller = controller
        
        # 3 column, 3 rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        
        # big title
        CTkLabel(self, text="Dashboard", font=("Helvetica", 35, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)

        # top one, big
        countdown_card = CTkFrame(self)
        countdown_card.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )
        CTkLabel(countdown_card, text="Countdown").pack(expand=True)

        # Budget card
        budget_card = CTkFrame(self)
        budget_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        CTkLabel(budget_card, text="Budget").pack(expand=True)

        # Tasks card
        tasks_card = CTkFrame(self)
        tasks_card.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        CTkLabel(tasks_card, text="Tasks").pack(expand=True)

        # Guestlist card
        guestlist_card = CTkFrame(self)
        guestlist_card.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        CTkLabel(guestlist_card, text="Guestlist").pack(expand=True)