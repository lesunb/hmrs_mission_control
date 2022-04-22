from ..data_model import (AbstractTask, ElementaryTask, Task, TaskState,
                          TaskStatus, transverse_ihtn)


def update_estimates_with_progress(ihtn: Task, task_state: TaskState):
    transverse_ihtn(ihtn, task_state, update_elementary_task, update_abstrack_task)

def update_elementary_task(task:Task, task_state: TaskState):
    if isinstance(task, ElementaryTask):
        task.state = task_state
    else:
        raise Exception('not supported task')

def update_abstrack_task(task: AbstractTask, task_state: TaskState):
    if task_state.status is TaskStatus.FAILED:
        task.state.status = TaskStatus.FAILED
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
    check_failure, any_failure = check_any_with_status(TaskStatus.FAILED)
    check_success, all_success = check_all_with_status(TaskStatus.COMPLETED_WITH_SUC)
    for t in task.selected_method.subtasks:
        check_failure(t)
        check_success(t)
    if all_success():
        task.state.status = TaskStatus.COMPLETED_WITH_SUC
    elif any_failure():
        task.state.status = TaskStatus.FAILED
    else:
        task.state.status = TaskStatus.IN_PROGRESS


