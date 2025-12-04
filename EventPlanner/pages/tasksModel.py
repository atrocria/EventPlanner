class Task:
    def __init__(self, text, done=False):
        self.text = text 
        self.done = done

    def toggle(self):
        self.done = not self.done