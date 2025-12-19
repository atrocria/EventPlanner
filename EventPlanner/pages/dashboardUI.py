from customtkinter          import CTkFrame, CTkLabel, CTkButton
from .dashboardController   import DashboardController

#display cards, communicate with each component's services for info
class DashboardUI(CTkFrame):
    def __init__(self, parent, controller: DashboardController, splash_key="dashboard"):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.splash_key = splash_key
        
        # 3 column, 3 rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        
        # big title
        CTkLabel(self, text="Dashboard", font=("Helvetica", 35, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=10)
        CTkButton(
            self, 
            text="ⓘ", 
            width=30,
            command=lambda: self.parent.show_page_splash(self.splash_key)
        ).grid(row=0, column=2, sticky="e", padx=10)
        
        # top one, big
        countdown_card = CTkFrame(self)
        countdown_card.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )
        self.countdown_info = self.controller.get_countdown_info()

        self.countdown_title = CTkLabel(
            countdown_card,
            font=("Helvetica", 24, "bold")
        )
        self.countdown_title.pack(pady=(20, 5))

        self.time_label = CTkLabel(
            countdown_card,
            font=("Helvetica", 20)
        )
        self.time_label.pack()

        self.update_countdown_display()
        self._countdown_running = False
        self._countdown_after_id = None

        info = self.controller.get_countdown_info()
        if info["has_countdown"]:
            self.start_countdown_refresh()

        # Budget card
        budget_card = CTkFrame(self)
        budget_card.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.budget_title = CTkLabel(
            budget_card,
            text="Budget",
            font=("Helvetica", 18, "bold")
        )
        self.budget_title.pack(pady=(15, 5))

        self.budget_info_label = CTkLabel(
            budget_card,
            font=("Helvetica", 14)
        )
        self.budget_info_label.pack()

        # Tasks card
        tasks_card = CTkFrame(self)
        tasks_card.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.tasks_title = CTkLabel(
            tasks_card,
            text="Tasks",
            font=("Helvetica", 18, "bold")
        )
        self.tasks_title.pack(pady=(15, 5))

        self.tasks_info_label = CTkLabel(
            tasks_card,
            font=("Helvetica", 14)
        )
        self.tasks_info_label.pack()


        # Guestlist card
        guestlist_card = CTkFrame(self)
        guestlist_card.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.guestlist_title = CTkLabel(
            guestlist_card,
            text="Guestlist",
            font=("Helvetica", 18, "bold")
        )
        self.guestlist_title.pack(pady=(15, 5))

        self.guestlist_info_label = CTkLabel(
            guestlist_card,
            font=("Helvetica", 14)
        )
        self.guestlist_info_label.pack()
        
    def format_seconds(self, seconds: int) -> str:
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
        
    def start_countdown_refresh(self):
        if self._countdown_running:
            return

        self._countdown_running = True
        self._tick_countdown()

    def _tick_countdown(self):
        info = self.controller.get_countdown_info()

        # countdown is gone → stop ticking
        if not info["has_countdown"]:
            print("stopping tick")
            self.stop_countdown_refresh()
            self.update_countdown_display()
            return

        self.update_countdown_display()
        self._countdown_after_id = self.after(1000, self._tick_countdown)

    def update_countdown_display(self):
        info = self.controller.get_countdown_info()

        if not info["has_countdown"]:
            self.countdown_title.configure(text="Countdown")
            self.time_label.configure(text="No countdown yet")
            return

        self.countdown_title.configure(text=info["event_name"])
        self.time_label.configure(
            text=self.format_seconds(info["remaining"])
        )
        
    def stop_countdown_refresh(self):
        if self._countdown_after_id is not None:
            self.after_cancel(self._countdown_after_id)
            self._countdown_after_id = None
            self._countdown_running = False
        
    def refresh(self):
        # countdown
        info = self.controller.get_countdown_info()
        if info["has_countdown"]:
            self.start_countdown_refresh()
        else:
            self.stop_countdown_refresh()
        self.update_countdown_display()

        # tasks
        self.update_tasks_display()

        # guestlist
        self.update_guestlist_display()

        # budget
        self.update_budget_display()

    def update_tasks_display(self):
        info = self.controller.get_tasks_info()

        if not info["has_tasks"]:
            self.tasks_info_label.configure(text="No tasks yet")
            return

        self.tasks_info_label.configure(
            text=f"{info['pending']} pending • {info['completed']} done"
        )

    def update_guestlist_display(self):
        info = self.controller.get_guestlist_info()

        if not info["has_guests"]:
            self.guestlist_info_label.configure(text="No guests yet")
            return

        self.guestlist_info_label.configure(
            text=f"{info['confirmed']} confirmed • {info['pending']} pending"
        )
        
    def update_budget_display(self):
        info = self.controller.get_budget_info()

        if not info["has_budget"]:
            self.budget_info_label.configure(text="No budget items yet")
            return

        total = info["total"]
        count = info["count"]

        self.budget_info_label.configure(
            text=f"{count} items • Total: ${total:,.2f}"
        )