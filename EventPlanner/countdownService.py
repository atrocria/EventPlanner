from EventPlanner.countdownModel import CountdownModel

class CountdownService:
    def __init__(self, model: CountdownModel):
        self.model = model

    def start(self, days, hours, minutes, seconds):
        self.model.set_countdown(days, hours, minutes, seconds)

    def tick(self):
        self.model.update_remaining()

