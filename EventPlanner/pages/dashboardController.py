from pages.countdown.countdownService   import CountdownService
from pages.budget.budgetServices        import BudgetService
from pages.tasks.tasksServices          import TaskServices
from pages.guestlist.guestlistService   import GuestListService
from pages.countdown.timerStateMachine  import TimerState

#display cards, communicate with each component's services for info
class DashboardController():
    def __init__(self, countdown_service: CountdownService, budget_service: BudgetService, tasks_service: TaskServices, guestlist_service: GuestListService):
        self.countdown_service = countdown_service
        self.budget_service = budget_service
        self.tasks_service = tasks_service
        self.guestlist_service = guestlist_service
        print("sup")

    def get_countdown_info(self):
        model = self.countdown_service.model
        remaining = self.countdown_service.tick()

        has_countdown = (
            model.end_time is not None and
            model.state != TimerState.IDLE
        )

        return {
            "has_countdown": has_countdown,
            "event_name": model.event_name,
            "remaining": remaining,
            "state": model.state.name
        }
        
    def get_budget_info(self):
        if not self.budget_service.has_items():
            return {
                "has_budget": False
            }

        return {
            "has_budget": True,
            "count": self.budget_service.count_items(),
            "total": self.budget_service.get_total()
        }

    def get_guestlist_info(self):
        total = self.guestlist_service.count_all()

        if total == 0:
            return {
                "has_guests": False
            }

        confirmed = self.guestlist_service.count_confirmed()
        pending = self.guestlist_service.count_pending()

        return {
            "has_guests": True,
            "total": total,
            "confirmed": confirmed,
            "pending": pending
        }

    def get_tasks_info(self):
        total = self.tasks_service.count_all()

        if total == 0:
            return {
                "has_tasks": False
            }

        completed = self.tasks_service.count_completed()
        pending = total - completed

        return {
            "has_tasks": True,
            "total": total,
            "completed": completed,
            "pending": pending
        }
