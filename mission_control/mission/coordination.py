from typing import Callable, List
from .ihtn import AbstractTask, ElementaryTask, Task, TaskState, TaskStatus, transverse_ihtn


def update_mission(ihtn: Task, task_state: TaskState):
    transverse_ihtn(ihtn, task_state, update_elementary_task, update_abstrack_task)



def update_elementary_task(task:Task, task_state: TaskState):
    if isinstance(task, ElementaryTask):
        task.state = task_state
    else:
        raise Exception('not supported task')


def update_abstrack_task(task:Task, task_state: TaskState):
    if task_state.status is TaskStatus.FAILURE:
        task.state.status = TaskStatus.FAILURE
        return

    def check_any_with_status(status):
        any = False
        def check(t):
            nonlocal any
            if t.state.is_status(status): 
                any = True
        def check_any():
            return any
        return check, check_any
    def check_all_with_status(status):
        all = True
        def check(t):
            nonlocal all
            if not t.state.is_status(status): 
                all = False
        def check_all():
            return all
        return check, check_all

    # new success
    check_failure, any_failure = check_any_with_status(TaskStatus.FAILURE)
    check_success, all_success = check_all_with_status(TaskStatus.SUCCESS_ENDED)
    for t in task.selected_method.subtasks:
        check_failure(t)
        check_success(t)
    if all_success():
        task.state.status = TaskStatus.SUCCESS_ENDED
    elif any_failure():
        task.state.status = TaskStatus.FAILURE
    else:
        task.state.status = TaskStatus.IN_PROGRESS


