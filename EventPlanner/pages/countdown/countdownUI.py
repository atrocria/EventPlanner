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

# Shorten update interval to 200ms for smoother animation (5 updates per second)
UPDATE_INTERVAL = 200  


class CountdownUI(CTkFrame):
    def __init__(self, parent, controller: CountdownController, back_target, splash_key="countdown"):
        super().__init__(parent)
        self.controller = controller
        self.back_target = back_target
        
        # Variable for event name (shared across screens)
        self.event_name = StringVar(value="My Event")  
        # New variable for years input (0 by default)
        self.years = StringVar(value="0")

        # Initialize with input screen
        self.build_input_screen()

    # ---------- COMMON METHODS ----------
    def clear(self):
        """Remove all widgets from the current frame to reset UI"""
        for widget in self.winfo_children():
            widget.destroy()

    # ---------- INPUT VALIDATION (LIMIT NUMERIC INPUTS) ----------
    def validate_int(self, value, max_val):
        """
        Validate input is a positive integer within specified range
        :param value: Input string to validate
        :param max_val: Maximum allowed numeric value
        :return: Boolean (True = valid input)
        """
        if not value:  # Allow empty input (defaults to 0)
            return True
        try:
            num = int(value)
            return 0 <= num <= max_val
        except ValueError:
            return False

    def create_validator(self, max_val):
        """Create a registered validation command for entry widgets"""
        return self.register(lambda P: self.validate_int(P, max_val))

    # ---------- INPUT SCREEN (PAGE 1: SET COUNTDOWN PARAMETERS) ----------
    def build_input_screen(self):
        """Build the input screen for setting countdown time and event name"""
        self.clear()

        # Display current date and day (top section)
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_day = datetime.now().strftime("%A")

        CTkLabel(
            self,
            text=current_date,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(10, 0))

        CTkLabel(
            self,
            text=current_day,
            font=("Segoe UI", 14)
        ).pack(pady=(0, 10))

        # Main title
        CTkLabel(
            self,
            text="Set Countdown",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # Event Name Input Field
        CTkLabel(self, text="Event Name:").pack(pady=5)
        CTkEntry(
            self, 
            width=200, 
            textvariable=self.event_name
        ).pack(pady=5)

        # Time input variables (days/hours/minutes/seconds)
        self.days = StringVar(value="0")
        self.hours = StringVar(value="0")
        self.minutes = StringVar(value="0")
        self.seconds = StringVar(value="0")

        # Form container for time inputs
        input_form = CTkFrame(self)
        input_form.pack(pady=10)

        # Add time input rows with validation limits
        self._create_input_row(input_form, "Years", self.years, 0, 99)    # Max: 99 years
        self._create_input_row(input_form, "Days", self.days, 1, 364)     # Max: 364 days
        self._create_input_row(input_form, "Hours", self.hours, 2, 23)    # Max: 23 hours
        self._create_input_row(input_form, "Minutes", self.minutes, 3, 59)# Max: 59 minutes
        self._create_input_row(input_form, "Seconds", self.seconds, 4, 59)# Max: 59 seconds

        # Start countdown button
        CTkButton(
            self,
            text="Start Countdown",
            command=self.start_countdown
        ).pack(pady=15)

    def _create_input_row(self, parent, label_text, var, row_num, max_val=999):
        """
        Create a labeled input row with numeric validation
        :param parent: Parent frame for the row
        :param label_text: Text for the input label
        :param var: StringVar bound to the entry widget
        :param row_num: Grid row position for the row
        :param max_val: Maximum allowed value (default: 999)
        """
        # Input label
        CTkLabel(parent, text=label_text).grid(row=row_num, column=0, padx=5, pady=5)
        
        # Input field with validation
        input_field = CTkEntry(parent, width=80, textvariable=var)
        input_field.grid(row=row_num, column=1, padx=5)
        
        # Configure input validation (only allow 0~max_val integers)
        input_field.configure(
            validate="key",
            validatecommand=(self.create_validator(max_val), "%P")
        )

    # ---------- TIMER SCREEN (PAGE 2: COUNTDOWN DISPLAY) ----------
    def build_timer_screen(self):
        """Build the full-screen countdown timer with enlarged centered elements"""
        self.clear()
        self.configure(fg_color="black")

        # 1. Enlarged event name (centered with bigger font)
        CTkLabel(
            self,
            textvariable=self.event_name,
            font=("Segoe UI", 32, "bold"),  # Larger font size
            text_color="white"
        ).pack(pady=30)  # Add top padding for centering

        # 2. Enlarged canvas for countdown circle (250x250 → 400x400)
        self.timer_canvas = CTkCanvas(
            self,
            width=400,    # Increased width
            height=400,   # Increased height
            bg="black",
            highlightthickness=0  # Remove border
        )
        self.timer_canvas.pack(pady=20)  # Center canvas vertically

        # 3. Enlarged outer circle (thicker border)
        self.timer_canvas.create_oval(
            20, 20, 380, 380,  # Expanded circle bounds
            outline="#FF8C00",  # Original orange color
            width=15  # Thicker border (12 → 15)
        )

        # 4. Enlarged progress arc (matches outer circle size)
        self.progress_arc = self.timer_canvas.create_arc(
            20, 20, 380, 380,
            start=90,
            extent=0,
            style="arc",
            outline="white",
            width=15  # Thicker arc border
        )

        # 5. REDUCED time display (smaller font: 48 → 36)
        self.time_display = self.timer_canvas.create_text(
            200, 180,  # Center of 400x400 canvas
            text="00:00:00:00",
            fill="white",
            font=("Segoe UI", 36, "bold")  # Smaller font (48 → 36)
        )

        # 6. REDUCED date/day text (smaller font: 16 → 14)
        self.date_display = self.timer_canvas.create_text(
            200, 220,
            text="DATE",
            fill="gray",
            font=("Segoe UI", 14)  # Smaller font (16 → 14)
        )
        
        self.days_left_display = self.timer_canvas.create_text(
            200, 250,
            text="DAY",
            fill="gray",
            font=("Segoe UI", 14)  # Smaller font (16 → 14)
        )

        # 7. Enlarged reset button (bigger size + font)
        CTkButton(
            self,
            text="Reset",
            font=("Segoe UI", 16, "bold"),  # Larger font
            width=120,  # Wider button
            height=40,  # Taller button
            command=self.reset_countdown
        ).pack(pady=30)  # Add bottom padding for centering

        # Start smooth update loop
        self.start_update_loop()

    # ---------- ACTION METHODS ----------
    def start_countdown(self):
        """Validate inputs and start the countdown timer"""
        try:
            # Convert input values to integers (including years → days conversion)
            years = int(self.years.get())
            days = int(self.days.get()) + (years * 365)  # 1 year = 365 days
            hours = int(self.hours.get())
            minutes = int(self.minutes.get())
            seconds = int(self.seconds.get())

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid numbers only (0 to maximum limit).")
            return

        # Calculate total seconds to validate positive time
        total_seconds = (days * 86400) + (hours * 3600) + (minutes * 60) + seconds
        if total_seconds <= 0:
            messagebox.showerror("Invalid Input", "Total countdown time must be greater than zero.")
            return

        # Initialize countdown via controller
        self.controller.start(days, hours, minutes, seconds)
        self.finished_alert_shown = False
        self.build_timer_screen()

    def reset_countdown(self):
        """Reset countdown and return to input screen"""
        self.controller.reset()
        self.build_input_screen()

    # ---------- UPDATE LOOP (SMOOTH ANIMATION) ----------
    def start_update_loop(self):
        """Continuous update loop for smooth countdown animation (200ms interval)"""
        # Get remaining seconds from controller
        remaining_seconds = self.controller.tick()
        total_seconds = self.controller.service.model.total_seconds

        # Calculate time breakdown (DD:HH:MM:SS)
        days_remaining = remaining_seconds // 86400
        hours_remaining = (remaining_seconds % 86400) // 3600
        minutes_remaining = (remaining_seconds % 3600) // 60
        seconds_remaining = remaining_seconds % 60

        # Update time display text
        self.timer_canvas.itemconfigure(
            self.time_display,
            text=f"{days_remaining:02d}:{hours_remaining:02d}:{minutes_remaining:02d}:{seconds_remaining:02d}"
        )

        # Update current date display
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.timer_canvas.itemconfigure(self.date_display, text=current_date)
        self.timer_canvas.itemconfigure(self.days_left_display, text=f"{days_remaining} day(s)")

        # Update progress arc with smooth angle changes
        if total_seconds > 0:
            progress_angle = 360 * (1 - (remaining_seconds / total_seconds))
            self.timer_canvas.itemconfigure(self.progress_arc, extent=progress_angle)

        # Handle countdown completion
        if self.controller.state == TimerState.FINISHED:
            if not self.finished_alert_shown:
                self.finished_alert_shown = True
                messagebox.showinfo(
                    "Countdown Complete",
                    f"{self.event_name.get()} countdown has finished!"
                )
                self.build_input_screen()  # Return to input screen
            return

        # Schedule next update (200ms = smoother animation)
        self.after(UPDATE_INTERVAL, self.start_update_loop)