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
from .countdownController import CountdownController
from .timerStateMachine import TimerState

UPDATE_INTERVAL = 200

class CountdownUI(CTkFrame):
    # Accept all parameters passed from app.py: parent/controller/back_target/splash_key
    def __init__(self, parent, controller: CountdownController = None, back_target=None, splash_key="countdown"):
        super().__init__(parent)
        self.controller = controller  # Use controller passed from parent (no self-creation)
        self.back_target = back_target  # Accept back button target function
        self.splash_key = splash_key    # Accept splash screen key identifier
        self.finished_alert_shown = False

        # Initialize variables (load saved event name from controller)
        self.event_name = StringVar(value=self.controller.get_event_name())
        self.years = StringVar(value="0")
        self.days = StringVar(value="0")
        self.hours = StringVar(value="0")
        self.minutes = StringVar(value="0")
        self.seconds = StringVar(value="0")

        # Auto-load running countdown on startup
        if self.controller.state == TimerState.RUNNING:
            # Show timer screen if countdown is active
            self.build_timer_screen()
        else:
            # Show input screen if no active countdown
            self.build_input_screen()

    def clear(self):
        """Clear all widgets from the current frame"""
        for widget in self.winfo_children():
            widget.destroy()

    # Input Validation Methods
    def validate_int(self, value, max_val):
        """Validate input is a positive integer within specified range"""
        if not value:
            return True
        try:
            num = int(value)
            return 0 <= num <= max_val
        except ValueError:
            return False

    def create_validator(self, max_val):
        """Create validation command for integer input fields"""
        return self.register(lambda P: self.validate_int(P, max_val))

    def _create_input_row(self, parent, label_text, var, row_num, max_val=999):
        """Create labeled input row with integer validation"""
        CTkLabel(parent, text=label_text).grid(row=row_num, column=0, padx=5, pady=5)
        entry = CTkEntry(parent, width=80, textvariable=var)
        entry.grid(row=row_num, column=1, padx=5)
        entry.configure(validate="key", validatecommand=(self.create_validator(max_val), "%P"))

    # Input Screen (Countdown Configuration)
    def build_input_screen(self):
        """Build screen for configuring countdown parameters"""
        self.clear()
        self.configure(fg_color="#2b2b2b")

        # Current date/weekday
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_day = datetime.now().strftime("%A")

        # Title section
        # Header frame (title + info button)
        header_frame = CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=10, fill="x", padx=20)

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        CTkLabel(
            header_frame,
            text="Event Countdown",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")

        CTkButton(
            header_frame,
            text="ⓘ",
            text_color="black",
            width=30,
            height=30,
            fg_color="#FFFFFF",
            hover_color="#A8A8A8",
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).grid(row=0, column=1, sticky="e", padx=(10, 0))

        CTkLabel(self, text=current_date, font=("Segoe UI", 16), text_color="lightgray").pack()
        CTkLabel(self, text=current_day, font=("Segoe UI", 14), text_color="lightgray").pack(pady=(0, 20))

        # Event name input
        CTkLabel(self, text="Event Name:", font=("Segoe UI", 16), text_color="white").pack()
        event_entry = CTkEntry(self, width=250, textvariable=self.event_name)
        event_entry.pack(pady=5, padx=20)

        # Time input frame (centered, no full-width stretch)
        time_frame = CTkFrame(self, fg_color="#3b3b3b")
        time_frame.pack(pady=20)  # Remove fill="x" and padx=20 for center alignment

        # Create time input rows (Years/Days/Hours/Minutes/Seconds)
        self._create_input_row(time_frame, "Years:", self.years, 0, 99)
        self._create_input_row(time_frame, "Days:", self.days, 1, 364)
        self._create_input_row(time_frame, "Hours:", self.hours, 2, 23)
        self._create_input_row(time_frame, "Minutes:", self.minutes, 3, 59)
        self._create_input_row(time_frame, "Seconds:", self.seconds, 4, 59)

        # Button frame (centered alignment)
        btn_frame = CTkFrame(self, fg_color="#2b2b2b")
        btn_frame.pack(pady=20)
        # Add column weight for center alignment (prevent left alignment)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # Start button (ONLY COLOR MODIFIED - light gray default, orange hover)
        start_btn = CTkButton(
            btn_frame,
            text="Start Countdown",
            command=self.start_countdown,
            fg_color="#d0d0d0",  # Light gray default (replaced original blue)
            hover_color="#ff9f43",  # Orange hover color (as requested)
            text_color="#333333",  # Dark gray text for better contrast
            width=150
        )
        start_btn.grid(row=0, column=0, padx=10)

        # Back button (if back target provided)
        if self.back_target:
            back_btn = CTkButton(
                btn_frame,
                text="← Back to Dashboard",
                command=self.go_back,
                width=180,
                height=38,
                fg_color="transparent",
                hover_color="#3a3a3a",
                text_color="#bbbbbb",
                border_width=1,
                border_color="#555555",
                corner_radius=10
            )
            back_btn.grid(row=1, column=0, padx=10, pady=10)

    def go_back(self):
        if not self.back_target:
            return

        # bring dashboard to front
        self.back_target.tkraise()

        # refresh dashboard data
        if hasattr(self.back_target, "refresh"):
            self.back_target.refresh()

        # sync sidebar highlight
        root = self.winfo_toplevel()
        if hasattr(root, "sidebar"):
            root.sidebar.select_by_target(self.back_target)

    # Timer Display Screen
    def build_timer_screen(self):
        """Build screen for displaying active countdown"""
        self.clear()
        self.configure(fg_color="black")
        
        # Header frame (event name + info button)
        header_frame = CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 0))

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        CTkLabel(
            header_frame,
            textvariable=self.event_name,
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")

        CTkButton(
            header_frame,
            text="ⓘ",
            text_color="black",
            width=30,
            height=30,
            fg_color="#FFFFFF",
            hover_color="#A8A8A8",
            command=lambda: self.winfo_toplevel().show_page_splash(self.splash_key)
        ).grid(row=0, column=1, sticky="e", padx=(10, 0))

        # Event name display
        CTkLabel(
            self,
            textvariable=self.event_name,
            font=("Segoe UI", 32, "bold"),
            text_color="white"
        ).pack(pady=30)

        # Countdown canvas
        self.timer_canvas = CTkCanvas(
            self,
            width=400,
            height=400,
            bg="black",
            highlightthickness=0
        )
        self.timer_canvas.pack(pady=20)

        # Outer circle (orange)
        self.timer_canvas.create_oval(
            20, 20, 380, 380,
            outline="#FF8C00",
            width=15
        )

        # Progress arc (white)
        self.progress_arc = self.timer_canvas.create_arc(
            20, 20, 380, 380,
            start=90,
            extent=0,
            style="arc",
            outline="white",
            width=15
        )

        # Load saved remaining time
        remaining = self.controller.service.model.remaining
        days = remaining // 86400
        hours = (remaining % 86400) // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        # Time display text
        self.time_display = self.timer_canvas.create_text(
            200, 180,
            text=f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}",
            fill="white",
            font=("Segoe UI", 36, "bold")
        )

        # Current date display
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_display = self.timer_canvas.create_text(
            200, 220,
            text=current_date,
            fill="gray",
            font=("Segoe UI", 14)
        )

        # Remaining days display
        self.days_left_display = self.timer_canvas.create_text(
            200, 250,
            text=f"{days} day(s) remaining",
            fill="gray",
            font=("Segoe UI", 14)
        )

        # Reset button
        reset_btn = CTkButton(
            self,
            text="Reset",
            command=self.reset_countdown,
            fg_color="#dc3545",
            hover_color="#c82333",
            width=120,
            height=40,
            font=("Segoe UI", 16, "bold")
        )
        reset_btn.pack(pady=30)
        
        if self.back_target:
            back_btn = CTkButton(
                self,
                text="← Back to Dashboard",
                command=self.go_back,
                width=180,
                height=38,
                fg_color="transparent",
                hover_color="#3a3a3a",
                text_color="#bbbbbb",
                border_width=1,
                border_color="#555555",
                corner_radius=10
            )
            back_btn.pack(pady=10)

        # Start real-time update loop
        self.start_update_loop()

    # Core Functionality Methods
    def start_countdown(self):
        """Start countdown after validating input parameters"""
        try:
            # Convert input values to integers
            years = int(self.years.get())
            days = int(self.days.get()) + (years * 365)
            hours = int(self.hours.get())
            minutes = int(self.minutes.get())
            seconds = int(self.seconds.get())

            # Save event name to controller
            self.controller.set_event_name(self.event_name.get())

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter only numeric values (0-99)")
            return

        # Validate total time is greater than 0
        total_seconds = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds
        if total_seconds <= 0:
            messagebox.showerror("Invalid Time", "Please enter a time greater than 0")
            return

        # Start countdown via controller
        self.controller.start(days, hours, minutes, seconds)
        self.finished_alert_shown = False
        self.build_timer_screen()

    def reset_countdown(self):
        """Reset countdown to initial state via controller"""
        self.controller.reset()
        self.build_input_screen()

    def start_update_loop(self):
        """Real-time countdown update loop (runs every UPDATE_INTERVAL ms)"""
        # Show completion alert when countdown finishes
        if self.controller.state == TimerState.FINISHED and not self.finished_alert_shown:
            messagebox.showinfo("Countdown Complete", f"{self.event_name.get()} has finished!")
            self.finished_alert_shown = True
            self.build_input_screen()
            return

        # Get updated remaining time
        remaining = self.controller.tick()
        total = self.controller.service.model.total_seconds

        # Calculate time components
        days = remaining // 86400
        hours = (remaining % 86400) // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        # Update time display
        self.timer_canvas.itemconfigure(
            self.time_display,
            text=f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        # Update progress arc
        if total > 0:
            progress_angle = 360 * (1 - (remaining / total))
            self.timer_canvas.itemconfigure(self.progress_arc, extent=progress_angle)

        # Update date and remaining days display
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.timer_canvas.itemconfigure(self.date_display, text=current_date)
        self.timer_canvas.itemconfigure(self.days_left_display, text=f"{days} day(s) remaining")

        # Repeat update loop
        self.after(UPDATE_INTERVAL, self.start_update_loop)