from typing import Callable, List

from .ihtn import AbstractTask, ElementaryTask, SyncTask, Task, TaskState


def flat_plan(ihtn) -> List[ElementaryTask]:
    if isinstance(ihtn, (ElementaryTask, SyncTask)):
        return [ihtn]
    elif isinstance(ihtn, AbstractTask):
        plan = []
        for subtask in ihtn.selected_method.subtasks:
            plan.extend(flat_plan(subtask))
        return plan

def count_elementary_tasks(ihtn):
    if isinstance(ihtn, ElementaryTask):
        return 1
    elif isinstance(ihtn, AbstractTask):
        count = 0
        for subtask in ihtn.selected_method.subtasks:
            count += count_elementary_tasks(subtask)
        return count
    else: return 0

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

def transverse_ihtn(ihtn: Task, task_state: TaskState, handle_leaf_match:Callable, handle_branch_match):
    """
    deep-first search for task_status.update, and apply handle_subtree 
     into the each intermediate task
    """
    if isinstance(ihtn, ElementaryTask):
        if ihtn == task_state.task:
            handle_leaf_match(ihtn, task_state)
            return True
        else:
            return False
    
    if isinstance(ihtn, AbstractTask):
        for subtask in ihtn.selected_method.subtasks:
            was_found = transverse_ihtn(subtask, task_state, handle_leaf_match, handle_branch_match)
            if was_found:
                handle_branch_match(ihtn, task_state)
                return True
        return False

def transverse_ihtn_apply_for_task(ihtn: Task, task_list: List[Task], apply: Callable):
    """
    deep-first search the ihtn for tasks in task_list, for each match call apply for a pair ihtn task, task in task_list
     into the each intermediate task
    """
    if isinstance(ihtn, ElementaryTask):
        if ihtn in task_list:
            index = task_list.index(ihtn)
            apply(ihtn, task_list[index])
    
    if isinstance(ihtn, AbstractTask):
        for subtask in ihtn.selected_method.subtasks:
            transverse_ihtn_apply_for_task(subtask, task_list, apply)


def ihtn_aggregate(ihtn: Task, agg_func: Callable):
    """
    aggregate results from subtasks into higher level abstract tasks
    """
    if isinstance(ihtn, ElementaryTask):
        return ihtn
    
    if isinstance(ihtn, AbstractTask):
        subtask_agg = map(lambda task: ihtn_aggregate(task, agg_func), ihtn.selected_method.subtasks)
        return agg_func(ihtn, list(subtask_agg))
        