from pages.tasksModel import TaskModel

class TaskServices():
    def __init__(self):
        self.tasks: list[TaskModel] = []

    def add(self, text: str) -> TaskModel:
        task = TaskModel(text)
        self.tasks.append(task)
        return task

    def delete_by_id(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def toggle_by_id(self, task_id: str):
        for t in self.tasks:
            if t.id == task_id:
                t.toggle()
                break
            
    def update_text(self, task_id, new_text):
        pass
            
    def all(self):
        return list(self.tasks)