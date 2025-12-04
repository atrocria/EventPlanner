import pages.tasksModel as TaskModel

class taskServices():
    def __init__(self):
        self.tasks = []

    def add(self, text):
        task = TaskModel(text)
        self.tasks.append(task)
        return task

    def delete(self, task):
        self.tasks.remove(task)

    def toggle(self, task):
        task.toggle()