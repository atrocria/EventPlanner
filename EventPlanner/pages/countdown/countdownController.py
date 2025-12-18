from .countdownService import CountdownService
from .timerStateMachine import TimerState

class CountdownController:
    # Compatibility mode: service parameter is optional (use passed service or create new)
    def __init__(self, service: CountdownService = None):
        # Use passed service if provided, otherwise create a new CountdownService instance
        self.service = service if service is not None else CountdownService()

    @property
    def state(self):
        return self.service.model.state

    def start(self, days, hours, minutes, seconds):
        self.service.start(days, hours, minutes, seconds)

    def reset(self):
        self.service.reset()

    def tick(self):
        return self.service.tick()

    def get_event_name(self):
        return self.service.model.event_name

    def set_event_name(self, name):
        self.service.model.event_name = name