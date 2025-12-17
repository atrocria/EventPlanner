from .countdownModel    import CountdownModel
from .timerStateMachine import TimerState
from datetime           import datetime, timedelta


class CountdownService:
    def __init__(self):
        self.model = CountdownModel()


    def start(self, days, hours, minutes, seconds):
        self.model.set_countdown(days, hours, minutes, seconds)
        print("SERVICE total_seconds =", self.model.total_seconds)
        
        if self.model.total_seconds > 0:
            self.model.end_time = datetime.now() + timedelta(seconds=self.model.total_seconds)
            self.model.state = TimerState.RUNNING

    def reset(self):
        self.model.state = TimerState.IDLE
        self.model.remaining = self.model.total_seconds

    def tick(self):
        if self.model.state == TimerState.RUNNING:
            now = datetime.now()
            self.model.remaining = max(0, int((self.model.end_time - now).total_seconds()))
            if self.model.remaining == 0:
                self.model.state = TimerState.FINISHED
        return self.model.remaining

