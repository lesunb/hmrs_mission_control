
from mission_control.mission.ihtn import Task, ElementaryTask, AbstractTask, SyncTask, MethodOrdering


def is_assigned(task: Task, role):
    return True if role in task.assign_to else False

def create_send_message(next_task, role):
    SEND_MESSAGE = SyncTask.SyncType.SEND_MESSAGE
    smt = SyncTask(type=SEND_MESSAGE, to_=next_task.assign_to, assign_to=role)
    return smt

def create_wait_message(next_task, role):
    WAIT_MESSAGE = SyncTask.SyncType.WAIT_MESSAGE
    wmt = SyncTask(type=WAIT_MESSAGE, from_=next_task.assign_to, assign_to=role)
    return wmt

def distribute(task: Task, role):
    if isinstance(task, ElementaryTask):
        if role in task.assign_to:
            return task.clone()
        else:
            return #noup
    elif isinstance(task, AbstractTask):
        ta: AbstractTask = task
        n_methods = []
        for method in ta.methods:
            nsubtasks = []
            if method.order == MethodOrdering.NON_ORDERED:
                for tk in method.subtasks:
                    if not is_assigned(tk, role):
                        continue
                    else:
                        nplan = distribute(task, role)
                        nsubtasks.append(nplan)
            else:
                # SEQUENTIAL
                for k, ktask in  enumerate(method.subtasks):
                    # last
                    plan = distribute(ktask, role)
                    if plan is not None:
                        nsubtasks.append(plan)
                    if k + 1 == len(method.subtasks):
                        pass
                    else:
                        if is_assigned(ktask, role):
                            next_task = method.subtasks[k+1]
                            if not is_assigned(next_task, role):
                                # assigned to this, and  not the next
                                # = notify the next
                                smt = create_send_message(next_task, role)
                                nsubtasks.append(smt)
                        elif is_assigned(method.subtasks[k+1], role):
                            # not assign to this, but to the next
                            wmt = create_wait_message(next_task, role)
                            nsubtasks.append(wmt)
                        else:
                            pass
                            # noop
            n_method = method.clone()
            n_method.subtasks = nsubtasks
            n_methods.append(n_method)
        n_ta = ta.clone()
        n_ta.methods = n_methods
        n_ta.selected_method = n_methods[0]
        return n_ta

    

def count_elementary_tasks(ihtn):
    if isinstance(ihtn, ElementaryTask):
        return 1
    elif isinstance(ihtn, AbstractTask):
        count = 0
        for subtask in ihtn.selected_method.subtasks:
            count += count_elementary_tasks(subtask)
        return count
    else: return 0

def flat_plan(ihtn):
    if isinstance(ihtn, ElementaryTask) or isinstance(ihtn, SyncTask) :
        return [ihtn]
    elif isinstance(ihtn, AbstractTask):
        plan = []
        for subtask in ihtn.selected_method.subtasks:
            plan.extend(flat_plan(subtask))
        return plan

def check_tasks_names(tasks, expected):
    obtained_task_names = []
    for task in tasks:
        obtained_task_names.append(task.name)
    
    diff =  set(obtained_task_names) ^ set(expected)
    return not diff