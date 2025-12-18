from .countdownModel import CountdownModel
from .timerStateMachine import TimerState
from datetime import datetime, timedelta
import json
import os

class CountdownService:
    def __init__(self):
        self.model = CountdownModel()
        # Force JSON storage in project root (same directory as app.py) - no path errors
        self.json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "countdown_data.json")
        
        # Auto-create JSON file if it doesn't exist
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({"total_seconds":0, "end_time":"", "state":0, "event_name":"My Countdown"}, f)
        
        # Load saved data and calculate remaining time
        self.load_json()
        self.calculate_remaining_time()

    # Load countdown data from JSON file
    def load_json(self):
        """Load persisted countdown data from JSON file"""
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.model.total_seconds = data["total_seconds"]
            self.model.event_name = data["event_name"]
            if data["end_time"]:
                self.model.end_time = datetime.fromisoformat(data["end_time"])
            self.model.state = TimerState(data["state"])
        except Exception:
            # Fail silently if JSON load fails (use default values)
            pass

    # Save countdown data to JSON file
    def save_json(self):
        """Persist current countdown state to JSON file"""
        try:
            end_time = self.model.end_time.isoformat() if self.model.end_time else ""
            data = {
                "total_seconds": self.model.total_seconds,
                "end_time": end_time,
                "state": self.model.state.value,
                "event_name": self.model.event_name
            }
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            # Fail silently if JSON save fails
            pass

    # Calculate remaining time after app restart (core functionality)
    def calculate_remaining_time(self):
        """Calculate remaining time when app restarts (for persistent countdown)"""
        if self.model.state != TimerState.RUNNING or not self.model.end_time:
            return
        now = datetime.now()
        self.model.remaining = max(0, int((self.model.end_time - now).total_seconds()))
        if self.model.remaining == 0:
            self.model.state = TimerState.FINISHED
            self.save_json()

    # Start the countdown
    def start(self, days, hours, minutes, seconds):
        """Initialize and start countdown with specified time parameters"""
        self.model.total_seconds = days*86400 + hours*3600 + minutes*60 + seconds
        self.model.end_time = datetime.now() + timedelta(seconds=self.model.total_seconds)
        self.model.state = TimerState.RUNNING
        self.model.remaining = self.model.total_seconds
        self.save_json()

    # Reset the countdown
    def reset(self):
        """Reset countdown to idle state (clear end time, reset remaining time)"""
        self.model.state = TimerState.IDLE
        self.model.end_time = None
        self.model.remaining = self.model.total_seconds
        self.save_json()

    # Update remaining time in real-time
    def tick(self):
        """Update and return current remaining seconds (call every update cycle)"""
        if self.model.state == TimerState.RUNNING and self.model.end_time:
            self.model.remaining = max(0, int((self.model.end_time - datetime.now()).total_seconds()))
            if self.model.remaining == 0:
                self.model.state = TimerState.FINISHED
                self.save_json()
        return self.model.remaining