from datetime           import datetime
from .timerStateMachine import TimerState


class CountdownModel:
    def __init__(self):
        self.total_seconds = 0   
        self.remaining = 0       
        self.end_time = None     
        self.state = TimerState.IDLE

    def set_countdown(self, days, hours, minutes, seconds):
        self.total_seconds = days*86400 + hours*3600 + minutes*60 + seconds
        self.remaining = self.total_seconds
        self.end_time = None
        self.state = TimerState.IDLE


    def update_remaining(self, now=None):
        if self.state == TimerState.RUNNING:
            now = now or datetime.now()
            self.remaining = max(0, int((self.end_time - now).total_seconds()))
            if self.remaining == 0:
                self.state = TimerState.FINISHED
