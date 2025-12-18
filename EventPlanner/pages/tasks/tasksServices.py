import json
from .tasksModel import TaskModel

class TaskServices():
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks: list[TaskModel] = []
        self.load()

    def add(self, text: str, due_at=None) -> TaskModel:
        order = len(self.tasks)
        task = TaskModel(text=text, order=order, due_at=due_at)
        self.tasks.append(task)
        self.save()
        return task

    def delete_by_id(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.normalize_order()
        self.save()

    def delete_by_ids(self, task_ids: list[str]):
        ids = set(task_ids)
        self.tasks = [t for t in self.tasks if t.id not in ids]
        self.normalize_order()
        self.save()

    def toggle_by_id(self, task_id: str):
        for t in self.tasks:
            if t.id == task_id:
                t.toggle()
                break
        self.save()
            
    def update_text(self, task_id, new_text):
        for t in self.tasks:
            if t.id == task_id:
                t.text = new_text
                break
        self.save()
        
    def get_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def reorder(self, ordered_ids: list[str]):
        for index, task_id in enumerate(ordered_ids):
            task = self.get_by_id(task_id)
            if task:
                task.order = index
        self.normalize_order()
        self.save()
        
    def count_all(self) -> int:
        return len(self.tasks)

    def count_completed(self) -> int:
        return sum(1 for t in self.tasks if t.done)

    def count_pending(self) -> int:
        return sum(1 for t in self.tasks if not t.done)
            
    def all(self):
        return sorted(self.tasks, key=lambda t: t.order)
    
    def save(self):
        with open(self.file_path, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.tasks = [TaskModel.from_dict(d) for d in data]
                self.normalize_order()
        except(FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            
    def normalize_order(self):
        for index, task in enumerate(self.all()):
            task.order = index