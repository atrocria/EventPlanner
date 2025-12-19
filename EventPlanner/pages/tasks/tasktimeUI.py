import tkinter              as tk 
from customtkinter          import CTkToplevel, CTkFrame, CTkButton, CTkLabel, CTkComboBox
from .tasktime_statemachine import TimeDial
from .taskController        import TaskController
import datetime
import time
import math

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
    def __init__(self, parent, task, on_save, anchor_seconds, max_seconds=100000000):
        super().__init__(parent)

        self.title("Set Time")
        self.geometry("600x600")
        self.resizable(False, False)
        
        self.last_tick = time.perf_counter()
        self.raw_distance = 0
        self.task = task
        self.on_save = on_save
        self.max_seconds = max_seconds
        self.anchor_seconds = anchor_seconds
        self.dial = TimeDial(
            max_seconds=self.max_seconds,
            anchor_seconds=  anchor_seconds,
            inner_scale_seconds=180 * 24 * 3600 # half a year
        )
        self.last_time = datetime.datetime.now()
        
        now = datetime.datetime.now()
        if task.due_at:
            delta = task.due_at - now
            self.selected_seconds = max(0, int(delta.total_seconds()))
        else:
            self.selected_seconds = 0
        self.dial.true_seconds = self.selected_seconds
        
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

        self.seconds = 0    # readonly result
        self.base_seconds = 0   # what position means
        self.overflow_seconds = 0   # momentum
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

        self.start_loop()
        CTkButton(btns, text="Save", command=self.save).pack(side="left", padx = 8)
        CTkButton(btns, text="Cancel", command=self.destroy).pack(side="left", padx = 8)
        
    def sync_date_from_seconds(self, seconds: int):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(seconds=seconds)
        
        self.day_var.set(str(future.day))
        self.month_var.set(str(future.month))
        self.year_var.set(str(future.year))
        
    def start_loop(self):
        self.last_tick = time.perf_counter()
        self.tick()

    def tick(self):
        now = time.perf_counter()
        dt = now - self.last_tick
        self.last_tick = now
        
        # advance dial even when mouse is still
        seconds = self.dial.update(
            raw_distance=self.raw_distance,
            max_radius=self.max_radius,
            dt=dt
        )
        
        if self.previewing:
            self.seconds = seconds
            self.update_tooltip()

        # reflect time over
        self.seconds = seconds
        self.update_tooltip()
        self.after(16, self.tick) # ~60fps
    
    def on_drag(self, event):
        # if holding again, stop snapback animation
        if self.snap_animating:
            self.snap_animating = False 
            
            if self.snap_after_id:                      # stop animating snapback
                self.after_cancel(self.snap_after_id)
                self.snap_after_id = None
        self.previewing = True                          # dragging mode = true
    
        # non linear scaling, gestimer inspired
        # mag x and mag y + hypotenuse line mmm
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        raw_distance = math.hypot(dx, dy) # triangle mmm
        
        self.raw_distance = raw_distance
        
        # lock ball position inside circle
        clamped_distance = min(raw_distance, self.max_radius)
        scale = clamped_distance / raw_distance if raw_distance > 0 else 0

        self.handle_x = self.center_x + dx * scale
        self.handle_y = self.center_y + dy * scale

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
        
        self.overflow_active = False
        self.overflow_after_id = None
        self.previewing = False         # dragging or nah
        self.selected_seconds = int(self.dial.true_seconds)
        self.selected_seconds = int(self.dial.true_seconds)
        self.sync_date_from_seconds(self.selected_seconds)
        
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

        self.update_handle()
        self.update_tooltip()

        # repeat
        self.snap_after_id = self.after(16, self.snap_step)
        
    def compute_seconds(self):
        return min(
            self.base_seconds + int(self.overflow_seconds),
            self.max_seconds
        )
        
    def save(self):
        now = datetime.datetime.now()
        due_at = now + datetime.timedelta(seconds=self.selected_seconds)

        self.on_save(due_at)
        self.destroy()