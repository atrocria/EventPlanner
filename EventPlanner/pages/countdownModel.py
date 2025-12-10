from datetime import datetime, timedelta
from timerStateMachine import TimerState

class CountdownModel:
    def __init__(self):
        self.total_seconds = 0
        self.end_time = None
        self.remaining = 0
        self.state = TimerState.IDLE

    def set_countdown(self, days, hours, minutes, seconds):
        self.total_seconds = days*86400 + hours*3600 + minutes*60 + seconds
        self.end_time = datetime.now() + timedelta(seconds=self.total_seconds)
        self.remaining = self.total_seconds
        self.state = TimerState.RUNNING

    def update_remaining(self):
        if self.state == TimerState.RUNNING:
            now = datetime.now()
            self.remaining = max(0, int((self.end_time - now).total_seconds()))
            if self.remaining == 0:
                self.state = TimerState.FINISHED
