from pages.tasksServices import TaskServices

class TaskController:
    def __init__(self, service: TaskServices):
        self.service = service

    def add_task(self, text):
        return self.service.add(text)

    def delete_task(self, task_id):
        self.service.delete_by_id(task_id)

    def toggle_task(self, task_id):
        self.service.toggle_by_id(task_id)

    def get_task(self):
        return self.service.all()