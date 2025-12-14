from pages.countdownService import CountdownService

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
        return self.service.tick()
