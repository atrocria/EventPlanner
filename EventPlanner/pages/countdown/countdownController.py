from .countdownService  import CountdownService
from .timerStateMachine  import TimerState

class CountdownController:
    def __init__(self, service: CountdownService):
        self.service = service

    @property
    def state(self):
        return self.service.model.state

    def start(self, days, hours, minutes, seconds):
        self.service.start(days, hours, minutes, seconds)

    def reset(self):
        self.service.reset()

    def tick(self):
        return self.service.tick()
