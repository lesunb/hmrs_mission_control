from mission_control.common_descriptors.routes_ed import Route
from mission_control.mission.planning import flat_plan



def mc_task_to_exeuctor(elementary_task):
    """ Convert to format understood by the executor """
    command = elementary_task.type
    parameters = []
    label = elementary_task.name
    if getattr(elementary_task, 'action', None) is not None:
        parameters.append(elementary_task.action)
    if getattr(elementary_task, 'destination', None) is not None:
        parameters.append(elementary_task.destination.label)
    if getattr(elementary_task, 'target', None) is not None:
        parameters.append(elementary_task.target.label)
    if getattr(elementary_task, 'to_', None):
        parameters.append(elementary_task.to_.pop().label)
    if getattr(elementary_task, 'from_', None):
        parameters.append(elementary_task.from_.pop().label)
    if getattr(elementary_task, 'assignment', None) is not None and \
        getattr(elementary_task.assignment, 'plan', None) is not None:
        if isinstance(elementary_task.assignment.plan['route'], Route):
            route = elementary_task.assignment.plan['route']
            waypoints = route.get_all_waypoints()
            parameters.append(waypoints)
    return (command, parameters, label)

def prep_plan(robot):
    knowledge = robot.knowledge
    plan  = flat_plan(knowledge.local_mission.plan) \
                if (knowledge.local_mission) else None
    if plan is None: return
    else: return list(map(mc_task_to_exeuctor, plan))
