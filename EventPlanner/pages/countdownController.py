from pages.countdownService import CountdownService
from timerStateMachine      import TimerState

class CountdownController:
    def __init__(self, service: CountdownService):
        self.service = service

    @property
    def state(self):
        return self.service.model.state

    def start(self, d, h, m, s):
        if self.service.can_start():
            self.service.start(d, h, m, s)

    def reset(self):
        self.service.reset()

    def tick(self):
        if self.service.model.state == TimerState.RUNNING:
            self.service.model.update_remaining()
        return self.service.model.remaining