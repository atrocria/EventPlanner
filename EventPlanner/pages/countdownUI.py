import customtkinter as ctk
from tkinter import messagebox  # can keep this for popups
from EventPlanner.countdownModel import CountdownModel
from EventPlanner.countdownService import CountdownService
from EventPlanner.timerStateMachine import TimerState

# ===== CONFIG =====
RADIUS = 100
CENTER_X = 150
CENTER_Y = 150
ORANGE = "#FFA500"
WHITE = "#FFFFFF"
BACKGROUND = "#000000"
UPDATE_INTERVAL = 50

class CountdownUI:
    def __init__(self, root, service: CountdownService, model: CountdownModel):
        self.root = root
        self.service = service
        self.model = model
        self.root.title("Circular Countdown Timer")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(fg_color=BACKGROUND)  # CTk background
        self.create_input_screen()

    # --- Input screen ---
    def create_input_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.root, text="Set Countdown", text_color=WHITE,
                     font=("Helvetica", 16, "bold")).pack(pady=10)

        self.days_var = ctk.StringVar(value="0")
        self.hours_var = ctk.StringVar(value="0")
        self.minutes_var = ctk.StringVar(value="0")
        self.seconds_var = ctk.StringVar(value="0")

        frame = ctk.CTkFrame(self.root, fg_color=BACKGROUND, border_width=0)
        frame.pack(pady=10)

        ctk.CTkLabel(frame, text="Days:", text_color=WHITE).grid(row=0, column=0)
        ctk.CTkEntry(frame, width=50, textvariable=self.days_var).grid(row=0, column=1)

        ctk.CTkLabel(frame, text="Hours:", text_color=WHITE).grid(row=0, column=2)
        ctk.CTkEntry(frame, width=50, textvariable=self.hours_var).grid(row=0, column=3)

        ctk.CTkLabel(frame, text="Minutes:", text_color=WHITE).grid(row=1, column=0)
        ctk.CTkEntry(frame, width=50, textvariable=self.minutes_var).grid(row=1, column=1)

        ctk.CTkLabel(frame, text="Seconds:", text_color=WHITE).grid(row=1, column=2)
        ctk.CTkEntry(frame, width=50, textvariable=self.seconds_var).grid(row=1, column=3)

        ctk.CTkButton(self.root, text="Start Countdown", command=self.start_countdown).pack(pady=20)

    # --- Start countdown ---
    def start_countdown(self):
        try:
            d = int(self.days_var.get())
            h = int(self.hours_var.get())
            m = int(self.minutes_var.get())
            s = int(self.seconds_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers!")
            return

        if d*86400 + h*3600 + m*60 + s <= 0:
            messagebox.showerror("Invalid input", "Countdown must be greater than 0 seconds!")
            return

        self.service.start(d, h, m, s)
        self.create_countdown_screen()

    # --- Countdown screen ---
    def create_countdown_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Canvas stays tk.Canvas since CTk does not have native Canvas
        self.canvas = ctk.CTkCanvas(self.root, width=300, height=300, bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack(pady=20)

        self.time_text = self.canvas.create_text(CENTER_X, CENTER_Y+20, text="", fill=WHITE,
                                                 font=("Helvetica", 16, "bold"))
        self.date_text = self.canvas.create_text(CENTER_X, CENTER_Y-40, text="", fill=WHITE,
                                                 font=("Helvetica", 12))
        self.day_text = self.canvas.create_text(CENTER_X, CENTER_Y-20, text="", fill=WHITE,
                                                font=("Helvetica", 12))

        # Base white ring
        self.canvas.create_oval(CENTER_X - RADIUS, CENTER_Y - RADIUS,
                                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                                outline=WHITE, width=8)

        self.update_timer()

    # --- Timer update ---
    def update_timer(self):
        self.service.tick()
        remaining = self.model.remaining
        total = self.model.total_seconds

        # Update text
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60
        self.canvas.itemconfig(self.time_text, text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        if self.model.end_time:
            self.canvas.itemconfig(self.date_text, text=self.model.end_time.strftime("%Y-%d-%m"))
            self.canvas.itemconfig(self.day_text, text=self.model.end_time.strftime("%A"))

        # Progress arcs
        self.canvas.delete("progress")

        fraction = remaining / total if total > 0 else 0
        angle_orange = 360 * fraction
        angle_white = 360 - angle_orange

        # White arc
        if angle_white > 0:
            self.canvas.create_arc(
                CENTER_X - RADIUS, CENTER_Y - RADIUS,
                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                start=90, extent=angle_white,
                style="arc", outline=WHITE, width=8, tags="progress"
            )

        # Orange arc
        if remaining > 0:
            self.canvas.create_arc(
                CENTER_X - RADIUS, CENTER_Y - RADIUS,
                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                start=90 - angle_orange, extent=angle_orange,
                style="arc", outline=ORANGE, width=8, tags="progress"
            )

        # Continue or finish
        if self.model.state == TimerState.RUNNING:
            self.root.after(UPDATE_INTERVAL, self.update_timer)
        else:
            # Fully white
            self.canvas.delete("progress")
            self.canvas.create_oval(
                CENTER_X - RADIUS, CENTER_Y - RADIUS,
                CENTER_X + RADIUS, CENTER_Y + RADIUS,
                outline=WHITE, width=8
            )
            messagebox.showinfo("Time's up!", "Countdown finished!")
            self.create_input_screen()
