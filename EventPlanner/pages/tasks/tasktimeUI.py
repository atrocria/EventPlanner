from customtkinter import CTkToplevel, CTkFrame, CTkButton, CTkLabel, CTkComboBox
import tkinter as tk 
import math
import datetime

# converter pure logic
def format_duration(seconds: int) -> str:
    units = [
        ("y",  365 * 24 * 3600),
        ("mo", 30  * 24 * 3600),
        ("d",  24  * 3600),
        ("h",  3600),
        ("m",  60),
        ("s",  1)
    ]
    
    parts = []
    for label, unit_seconds in units:
        if seconds >= unit_seconds:
            value, seconds = divmod(seconds, unit_seconds)
            parts.append(f"{value}{label}")

    return " ".join(parts) if parts else "0s"

class TaskTimeUI(CTkToplevel):
    def __init__(self, parent, task, on_save, max_seconds=1200000000):
        super().__init__(parent)

        self.task = task
        self.on_save = on_save
        self.max_seconds = max_seconds
        
        self.title("Set Time")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # the task
        self.task_label = CTkLabel(
            self,
            text=(f"task:  {task.text}"),
            font=("Helvetica", 25, "bold"),
            wraplength=500,
            justify="left"
        )
        self.task_label.pack(pady=(10, 6))


        self.canvas_height = 300
        self.canvas_width = 380
        
        # create center point and radius
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        
        self.edge_padding = 20
        self.max_radius = min(self.center_x, self.center_y) - self.edge_padding
        
        # snapback anim
        self.snap_animating = False
        self.snap_after_id = None

        self.seconds = 0 # minute is distance
        self.selected_seconds = 0
        self.previewing = False
        
        self.attributes("-topmost", True)
        self.after(100, lambda: self.focus_force())
        self.grab_set()

        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg = "#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        self.origin_radius = 4
        self.origin = self.canvas.create_oval(
            self.center_x - self.origin_radius,
            self.center_y - self.origin_radius,
            self.center_x + self.origin_radius,
            self.center_y + self.origin_radius,
            fill="#666666",   # neutral gray
            outline=""
        )
        
        # the ball, the center pin
        self.handle_radius = 7
        self.handle_x = self.center_x
        self.handle_y = self.center_y
        self.vector_line = self.canvas.create_line( # the line
            self.center_x,
            self.center_y,
            self.handle_x,
            self.handle_y,
            width=5,
            fill="#ff6c6c"
        )
        self.handle = self.canvas.create_oval( # the ball
            self.handle_x - self.handle_radius,
            self.handle_y - self.handle_radius,
            self.handle_x + self.handle_radius,
            self.handle_y + self.handle_radius,
            fill="#000000",
            outline=""
        )
        
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release) # begin snapback animation
        
        # date picker frame
        self.date_row = CTkFrame(self, fg_color="transparent")
        self.date_row.pack(pady=(8, 12))
        
        # days
        self.day_var = tk.StringVar(value=str(datetime.datetime.now().day))
        self.day_box = CTkComboBox(
            self.date_row,
            values=[str(i) for i in range(1, 32)],
            variable=self.day_var,
            width=80
        )
        self.day_box.pack(side="left", padx=4)
        
        # months
        self.month_var = tk.StringVar(value=str(datetime.datetime.now().month))
        self.month_box = CTkComboBox(
            self.date_row,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            width=80
        )
        self.month_box.pack(side="left", padx=4)

        # year
        current_year = datetime.datetime.now().year
        self.year_var = tk.StringVar(value=str(current_year))

        self.year_box = CTkComboBox(
            self.date_row,
            values=[str(y) for y in range(current_year, current_year + 6)],
            variable=self.year_var,
            width=100
        )
        self.year_box.pack(side="left", padx=4)


        btns = CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        self.bigBlackBox = CTkLabel(
            self,
            text="0s",
            text_color="white",
            font=("Helvetica", 12, "bold"),
            fg_color="#000000",
            corner_radius=30,
            padx=12,
            pady=6
        )

        CTkButton(btns, text="Save", command=self.save).pack(side="left", padx = 8)
        CTkButton(btns, text="Cancel", command=self.destroy).pack(side="left", padx = 8)
        
    def on_drag(self, event):
        # if holding again
        if self.snap_animating:
            self.snap_animating = False
            if self.snap_after_id:
                self.after_cancel(self.snap_after_id)
                self.snap_after_id = None
        self.previewing = True
    
        # non linear scaling, gestimer inspired
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        distance = math.sqrt(dx*dx + dy*dy) # triangle mmm

        # clamp
        if distance > self.max_radius:
            scale = self.max_radius / distance
            dx *= scale
            dy *= scale
            distance = self.max_radius
        
        # update ball position
        self.handle_x = self.center_x + dx
        self.handle_y = self.center_y + dy
        
        # clamped unit 1
        normalized = distance / self.max_radius

        if normalized < 0.25:
            # 0–10 min
            local = normalized / 0.25
            seconds = local * 10 * 60

        elif normalized < 0.45:
            # 10–60 min
            local = (normalized - 0.25) / 0.20
            seconds = 10*60 + local * 50*60

        elif normalized < 0.60:
            # 1–6 h
            local = (normalized - 0.45) / 0.15
            seconds = 60*60 + local * 5*3600

        elif normalized < 0.72:
            # 6–24 h
            local = (normalized - 0.60) / 0.12
            seconds = 6*3600 + local * 18*3600

        elif normalized < 0.82:
            # 1–7 days
            local = (normalized - 0.72) / 0.10
            seconds = 24*3600 + local * 6*24*3600

        elif normalized < 0.92:
            # 1–4 weeks
            local = (normalized - 0.82) / 0.10
            seconds = 7*24*3600 + local * 3*7*24*3600

        else:
            # months → years
            local = (normalized - 0.92) / 0.08
            seconds = 28*24*3600 + local * (self.max_seconds - 28*24*3600)

        self.seconds = int(max(0, min(seconds, self.max_seconds)))

        
        self.update_handle()
        self.update_tooltip()
        
    def update_handle(self):
        r = self.handle_radius
        
        # connecting line position
        self.canvas.coords(
            self.vector_line,
            self.center_x,
            self.center_y,
            self.handle_x,
            self.handle_y
        )
        
        # handle position
        self.canvas.coords(
            self.handle,
            self.handle_x - r,
            self.handle_y - r,
            self.handle_x + r,
            self.handle_y + r
        )
        
    def update_tooltip(self):
        cx = self.canvas.winfo_rootx()
        cy = self.canvas.winfo_rooty()

        # move pill under pin
        self.bigBlackBox.place(
            x=self.handle_x + cx - self.winfo_rootx(),
            y=self.handle_y + cy - self.winfo_rooty() + self.handle_radius + 12,
            anchor="n"
        )
        seconds = self.seconds if self.previewing else self.selected_seconds
        duration = format_duration(seconds)
        now = datetime.datetime.now()
        future = now + datetime.timedelta(seconds=seconds)

        text = f"in {duration}"
        text_date = f"in {seconds} min\n{future.strftime('%H:%M')}" # set later on auto slider
        self.bigBlackBox.configure(text=text)
        self.bigBlackBox.tkraise()
        self.bigBlackBox.lift()
        
    def on_release(self, event):
        if self.snap_animating:
            return
        
        self.previewing = False         # dragging or nah
        self.selected_seconds = self.seconds
        
        self.snap_animating = True
        self.snap_step()

    # animation logic
    def snap_step(self):
        dx = self.center_x - self.handle_x
        dy = self.center_y - self.handle_y
        
        distance = math.sqrt(dx*dx + dy*dy)

        # snap to center threshold
        if distance < 1:
            self.handle_x = self.center_x
            self.handle_y = self.center_y
            
            self.update_handle()
            self.update_tooltip()

            # stop the animation
            self.snap_animating = False
            return
        
        easing = 0.25
        self.handle_x += dx * easing
        self.handle_y += dy * easing
        
        normalized = distance / self.max_radius
        self.seconds = int(self.max_seconds * (normalized ** 1.5))

        self.update_handle()
        self.update_tooltip()

        # repeat
        self.snap_after_id = self.after(16, self.snap_step)
        
    def save(self):
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        day = int(self.day_var.get())

        base_date = datetime.datetime(year, month, day)

        final_time = base_date + datetime.timedelta(
            seconds=self.selected_seconds
        )

        self.on_save(final_time)
        self.destroy()