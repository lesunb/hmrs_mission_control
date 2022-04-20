from ..ihtn import ElementaryTask, Task, AbstractTask

def eliminate_left_task(task: ElementaryTask, plan: Task):
    if plan is task:
        return None

    method = plan.selected_method
    if isinstance(method.subtasks[0], ElementaryTask):
        if method.subtasks[0] == task:
            if len(method.subtasks) == 1:
                # only task in method
                return None
            else:
                method.subtasks = method.subtasks[1:]
                return plan
        else:
            raise Exception(f'leftmost task is not {task}')
    else:
        res_plan = eliminate_left_task(task, method.subtasks[0])
        if res_plan is None:
            if len(method.subtasks) == 1:
                # only task in method
                return None
            else:
                method.subtasks = method.subtasks[1:]
                return plan
        else:
            method.subtasks[0] = res_plan
            return plan

def get_first_task(plan) -> ElementaryTask:
    if plan is None:
        return None
    if isinstance(plan, ElementaryTask):
        return plan
    
    if isinstance(plan, AbstractTask):
        if isinstance(plan.selected_method.subtasks[0], ElementaryTask):
            return plan.selected_method.subtasks[0]
        else:
            return get_first_task(plan.selected_method.subtasks[0])
