class TaskController:
    def __init__(self, service):
        self.service = service
        self.view = None

    def bind_view(self, view):
        self.view = view
        
    def on_add(self, text):
        task = self.service.add(text)
        self.view.add_task_to_ui(task)

    def on_toggle(self, task):
        self.service.toggle(task)

    def on_delete(self, task):
        self.service.delete(task)
        self.view.remove_task_from_ui(task)