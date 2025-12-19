import uuid
from datetime   import datetime

class TaskModel:
    def __init__(self, text, task_id=None, done=False, due_at=None, notified=False, order=0):
        self.id = task_id or uuid.uuid4().hex
        self.text = text 
        self.done = done
        self.order = order
        self.due_at = due_at
        self.notified = notified

    # task done? if so, task = !doness
    def toggle(self):
        self.done = not self.done
        
    # whats stored for json to read
    def to_dict(self):
        return {
            "id": self.id, 
            "text": self.text, 
            "done": self.done, 
            "order": self.order, 
            "due_at": self.due_at.isoformat() if self.due_at else None, 
            "notified": self.notified
        }
    
    # whats stored for UI to read
    @classmethod
    def from_dict(cls, data:dict):
        due_at = None
        raw = data.get("due_at")

        if isinstance(raw, str):
            due_at = datetime.fromisoformat(raw)
        
        return cls(
            text=data["text"],
            task_id=data["id"],
            done=data.get("done", False),
            order=data.get("order", 0),
            due_at=due_at,
            notified=data.get("notified", False)
        )