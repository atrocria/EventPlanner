import uuid

class TaskModel:
    def __init__(self, text, task_id=None, done=False):
        self.id = task_id or uuid.uuid4().hex
        self.text = text 
        self.done = done

    # task done? if so, task = !doness
    def toggle(self):
        self.done = not self.done
        
    # whats stored for json to read
    def to_dict(self):
        return {"id": self.id, "text": self.text, "done": self.done}
    
    # whats stored for UI to read
    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            text=data["text"],
            task_id=data["id"],
            done=data.get("done", False),
        )