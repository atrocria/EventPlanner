import json
from .tasksModel import TaskModel

class TaskServices():
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks: list[TaskModel] = []
        self.load()

    def add(self, text: str) -> TaskModel:
        task = TaskModel(text)
        self.tasks.append(task)
        self.save()
        return task

    def delete_by_id(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save()

    def delete_by_ids(self, task_ids: list[str]):
        ids = set(task_ids)
        self.tasks = [t for t in self.tasks if t.id not in ids]
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
            
    def all(self):
        return list(self.tasks)
    
    def save(self):
        with open(self.file_path, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.tasks = [TaskModel.from_dict(d) for d in data]
        except(FileNotFoundError, json.JSONDecodeError):
            self.tasks = []