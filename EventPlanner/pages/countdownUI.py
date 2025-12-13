from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, StringVar
from tkinter import messagebox
from timerStateMachine import TimerState

UPDATE_INTERVAL = 1000  # 1 second


class CountdownUI(CTkFrame):
    def __init__(self, parent, controller, back_target):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target

        self.build_input_screen()

    # ---------- UI BUILDERS ----------

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def build_input_screen(self):
        self.clear()

        CTkLabel(self, text="Set Countdown", font=("Segoe UI", 20, "bold")).pack(pady=10)

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

        CTkButton(self, text="Start Countdown", command=self.start).pack(pady=15)

    def _row(self, parent, label, var, row):
        CTkLabel(parent, text=label).grid(row=row, column=0, padx=5, pady=5)
        CTkEntry(parent, width=80, textvariable=var).grid(row=row, column=1, padx=5)

    def build_timer_screen(self):
        self.clear()

        self.time_label = CTkLabel(self, text="00:00:00", font=("Segoe UI", 32, "bold"))
        self.time_label.pack(pady=30)

        CTkButton(self, text="Reset", command=self.reset).pack(pady=10)

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

        if d*86400 + h*3600 + m*60 + s <= 0:
            messagebox.showerror("Invalid Input", "Time must be greater than zero.")
            return

        self.controller.start(d, h, m, s)
        self.build_timer_screen()

    def reset(self):
        self.controller.reset()
        self.build_input_screen()

    def update_loop(self):
        remaining = self.controller.tick()

        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60

        self.time_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

        if self.controller.state == TimerState.RUNNING:
            self.after(UPDATE_INTERVAL, self.update_loop)
        else:
            messagebox.showinfo("Done", "Countdown finished.")
            self.build_input_screen()
