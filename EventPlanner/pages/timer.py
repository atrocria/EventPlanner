import tkinter as tk
from tkinter import messagebox
import time
import math
from datetime import datetime, timedelta

# ======= CONFIG =======
RADIUS = 100
CENTER_X = 150
CENTER_Y = 150
ORANGE = "#FFA500"
WHITE = "#FFFFFF"
BACKGROUND = "#000000"
UPDATE_INTERVAL = 50  # milliseconds for smooth animation

# ======= MAIN APP =======
class CountdownApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Circular Countdown Timer")
        self.root.configure(bg=BACKGROUND)
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.create_input_screen()

    # -------- INPUT SCREEN --------
    def create_input_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Set Countdown", bg=BACKGROUND, fg=WHITE, font=("Helvetica", 16, "bold")).pack(pady=10)
        
        self.days_var = tk.StringVar(value="0")
        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")
        
        frame = tk.Frame(self.root, bg=BACKGROUND)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Days:", bg=BACKGROUND, fg=WHITE).grid(row=0, column=0)
        tk.Entry(frame, width=5, textvariable=self.days_var).grid(row=0, column=1)
        tk.Label(frame, text="Hours:", bg=BACKGROUND, fg=WHITE).grid(row=0, column=2)
        tk.Entry(frame, width=5, textvariable=self.hours_var).grid(row=0, column=3)
        tk.Label(frame, text="Minutes:", bg=BACKGROUND, fg=WHITE).grid(row=1, column=0)
        tk.Entry(frame, width=5, textvariable=self.minutes_var).grid(row=1, column=1)
        tk.Label(frame, text="Seconds:", bg=BACKGROUND, fg=WHITE).grid(row=1, column=2)
        tk.Entry(frame, width=5, textvariable=self.seconds_var).grid(row=1, column=3)

        tk.Button(self.root, text="Start Countdown", command=self.start_countdown).pack(pady=20)

    # -------- START COUNTDOWN --------
    def start_countdown(self):
        try:
            d = int(self.days_var.get())
            h = int(self.hours_var.get())
            m = int(self.minutes_var.get())
            s = int(self.seconds_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers!")
            return
        
        total_seconds = d*86400 + h*3600 + m*60 + s
        if total_seconds <= 0:
            messagebox.showerror("Invalid input", "Countdown must be greater than 0 seconds!")
            return
        
        self.end_time = datetime.now() + timedelta(seconds=total_seconds)
        self.create_countdown_screen(total_seconds)

    # -------- COUNTDOWN SCREEN --------
    def create_countdown_screen(self, total_seconds):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.total_seconds = total_seconds
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.time_text = self.canvas.create_text(CENTER_X, CENTER_Y+20, text="", fill=WHITE, font=("Helvetica", 16, "bold"))
        self.date_text = self.canvas.create_text(CENTER_X, CENTER_Y-40, text="", fill=WHITE, font=("Helvetica", 12))
        self.day_text = self.canvas.create_text(CENTER_X, CENTER_Y-20, text="", fill=WHITE, font=("Helvetica", 12))
        
        self.canvas.create_oval(CENTER_X-RADIUS, CENTER_Y-RADIUS, CENTER_X+RADIUS, CENTER_Y+RADIUS, outline=ORANGE, width=8)
        
        self.update_timer()

    # -------- TIMER UPDATE --------
    def update_timer(self):
        now = datetime.now()
        remaining = max(0, int((self.end_time - now).total_seconds()))
        
        # Update countdown text
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60
        self.canvas.itemconfig(self.time_text, text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Update date/day text (end date)
        end_date_str = self.end_time.strftime("%Y-%d-%m")
        end_day_str = self.end_time.strftime("%A")
        self.canvas.itemconfig(self.date_text, text=end_date_str)
        self.canvas.itemconfig(self.day_text, text=end_day_str)
        
        # Smooth progress effect
        fraction = remaining / self.total_seconds if self.total_seconds > 0 else 0
        self.canvas.delete("progress")
        angle = 360 * fraction
        # draw progress arc
        self.canvas.create_arc(CENTER_X-RADIUS, CENTER_Y-RADIUS, CENTER_X+RADIUS, CENTER_Y+RADIUS,
                               start=90, extent=-angle, style="arc", outline=ORANGE, width=8, tags="progress")
        
        if remaining > 0:
            self.root.after(UPDATE_INTERVAL, self.update_timer)
        else:
            # Countdown finished
            self.canvas.delete("progress")
            self.canvas.create_oval(CENTER_X-RADIUS, CENTER_Y-RADIUS, CENTER_X+RADIUS, CENTER_Y+RADIUS,
                                    outline=WHITE, width=8)
            self.canvas.itemconfig(self.time_text, fill=WHITE)
            self.canvas.itemconfig(self.date_text, fill=WHITE)
            self.canvas.itemconfig(self.day_text, fill=WHITE)
            messagebox.showinfo("Time's up!", "Countdown finished!")
            self.create_input_screen()


# ======= RUN APP =======
root = tk.Tk()
app = CountdownApp(root)
root.mainloop()