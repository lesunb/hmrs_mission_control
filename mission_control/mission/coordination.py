from typing import Callable, List
from .ihtn import AbstractTask, ElementaryTask, Task, TaskState, TaskStatus, transverse_ihtn


def update_mission(ihtn: Task, task_state: TaskState):
    transverse_ihtn(ihtn, task_state, update_success_and_in_progress)



def update_success_and_in_progress(task:Task, task_state: TaskState):
    if isinstance(task, ElementaryTask):
        task.state = task_state
    elif isinstance(task, AbstractTask):
        if task_state.status is TaskStatus.SUCCESS_END:
            all_succ = True
            # if all subtasks where a success, abstract task is a success
            for t in task.selected_method.subtasks:
                if t.state.is_status(TaskStatus.SUCCESS_END):
                    all_succ = False
                    break
            if all_succ:
                task.state = TaskState(status=TaskStatus.SUCCESS_END)
            # if a 
    else:
        raise Exception('not supported task')



