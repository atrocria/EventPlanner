from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkButton,
    StringVar,
    CTkCanvas
)
from tkinter import messagebox
from datetime import datetime
from .timerStateMachine import TimerState
from .countdownController import CountdownController

UPDATE_INTERVAL = 1000  # 1 second


class CountdownUI(CTkFrame):
    def __init__(self, parent, controller: CountdownController, back_target):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target
        self.finished_shown = False

        self.build_input_screen()

    # ---------- COMMON ----------

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ---------- INPUT SCREEN (PAGE 1) ----------

    def build_input_screen(self):
        self.clear()

        # date & day (top)
        today_date = datetime.now().strftime("%Y-%m-%d")
        today_day = datetime.now().strftime("%A")

        CTkLabel(
            self,
            text=today_date,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(10, 0))

        CTkLabel(
            self,
            text=today_day,
            font=("Segoe UI", 14)
        ).pack(pady=(0, 10))

        CTkLabel(
            self,
            text="Set Countdown",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        self.days = StringVar(value="0")
        self.hours = StringVar(value="0")
        self.minutes = StringVar(value="0")
        self.seconds = StringVar(value="0")

        form = CTkFrame(self)
        form.pack(pady=10)

        self._row(form, "Days", self.days, 0)
        self._row(form, "Hours", self.hours, 1)
        self._row(form, "Minutes", self.minutes, 2)
        self._row(form, "Seconds", self.seconds, 3)

        CTkButton(
            self,
            text="Start Countdown",
            command=self.start
        ).pack(pady=15)

    def _row(self, parent, label, var, row):
        CTkLabel(parent, text=label).grid(row=row, column=0, padx=5, pady=5)
        CTkEntry(parent, width=80, textvariable=var).grid(
            row=row, column=1, padx=5
        )

    # ---------- TIMER SCREEN (PAGE 2) ----------

    def build_timer_screen(self):
        self.clear()
        self.configure(fg_color="black")

        self.canvas = CTkCanvas(
            self,
            width=250,
            height=250,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.canvas.create_oval(
            10, 10, 240, 240,
            outline="white",
            width=12
        )

        self.arc = self.canvas.create_arc(
            10, 10, 240, 240,
            start=90,
            extent=0,
            style="arc",
            outline="#FF8C00",
            width=12
        )

        self.time_text = self.canvas.create_text(
            125, 115,
            text="00:00:00",
            fill="white",
            font=("Segoe UI", 28, "bold")
        )

        self.date_text = self.canvas.create_text(
            125, 145,
            text="DATE",
            fill="gray",
            font=("Segoe UI", 12)
        )

        self.day_text = self.canvas.create_text(
            125, 170,
            text="DAY",
            fill="gray",
            font=("Segoe UI", 12)
        )

        CTkButton(
            self,
            text="Reset",
            command=self.reset
        ).pack(pady=10)

        self.update_loop()

    # ---------- ACTIONS ----------

    def start(self):
        try:
            d = int(self.days.get())
            h = int(self.hours.get())
            m = int(self.minutes.get())
            s = int(self.seconds.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid numbers.")
            return

        if d * 86400 + h * 3600 + m * 60 + s <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Time must be greater than zero."
            )
            return

        self.controller.start(d, h, m, s)
        self.finished_shown = False
        self.build_timer_screen()

    def reset(self):
        self.controller.reset()
        self.build_input_screen()

    # ---------- UPDATE LOOP ----------

    def update_loop(self):
        remaining = self.controller.tick()
        total = self.controller.service.model.total_seconds

        # time
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60

        self.canvas.itemconfigure(
            self.time_text,
            text=f"{h:02d}:{m:02d}:{s:02d}"
        )

        # date
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.canvas.itemconfigure(
            self.date_text,
            text=today_date
        )

        # days left
        days_left = remaining // 86400
        self.canvas.itemconfigure(
            self.day_text,
            text=f"{days_left} day(s)"
        )

        # progress arc
        if total > 0:
            angle = 360 * (1 - remaining / total)
            self.canvas.itemconfigure(self.arc, extent=angle)

        # finished
        if self.controller.state == TimerState.FINISHED:
            if not self.finished_shown:
                self.finished_shown = True
                messagebox.showinfo(
                    "Done",
                    "Countdown finished"
                )
                self.build_input_screen()
            return

        self.after(UPDATE_INTERVAL, self.update_loop)


