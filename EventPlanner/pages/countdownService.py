from pages.countdownModel import CountdownModel
from timerStateMachine import TimerState

class CountdownService:
    def __init__(self):
        self.model = CountdownModel()

    def start(self, days, hours, minutes, seconds):
        if self.can_start():
            self.model.set_countdown(days, hours, minutes, seconds)

    def pause(self):
        if self.can_pause():
            self.model.state = TimerState.PAUSED

    def reset(self):
        self.model = CountdownModel()

    def tick(self):
        self.model.update_remaining()
        return self.model.remaining

    def can_start(self):
        return self.model.state in (TimerState.IDLE, TimerState.PAUSED)

    def can_pause(self):
        return self.model.state == TimerState.RUNNING
