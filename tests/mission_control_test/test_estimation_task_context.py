from mission_control.estimate.core import TaskContext
from mission_control.core import Worker, POI
from mission_control.mission.ihtn import ElementaryTask

def test_task_context_start():
    unit = Worker(position = (3, 4))
    tsk_ctx = TaskContext(unit)
    tsk_ctx.start()
    assert tsk_ctx.origin == (3, 4)

def test_task_context_get_properties():
    sr_poi = POI('storage_room')
    room3_poi = POI('room3')

    unit = Worker(position = sr_poi)
    tsk_ctx = TaskContext(unit)
    tsk_ctx.start()
    task = ElementaryTask(type='navigate', destination=room3_poi)
    tsk_ctx = tsk_ctx.unwind(task)
    assert tsk_ctx.get('origin') == sr_poi
    assert tsk_ctx.get('destination') == room3_poi


def test_task_context_position_unwinding():
    sr_poi = POI('storage_room')
    room1_poi = POI('room1')
    room3_poi = POI('room3')
    task1 = ElementaryTask(type='navigate', destination=room3_poi)
    task2 = ElementaryTask(type='navigate', destination=room1_poi)
    task3 = ElementaryTask(type='simple_action')
    task4 = ElementaryTask(type='navigate', destination=room3_poi)

    unit = Worker(position = sr_poi)
    tsk_ctx = TaskContext(unit)
    tsk_ctx.start()
    tsk_ctxs = []
    for task in [task1, task2, task3, task4]:
        tsk_ctx = tsk_ctx.unwind(task)
        tsk_ctxs.append(tsk_ctx)

    assert tsk_ctxs[0].get('origin') == sr_poi
    assert tsk_ctxs[1].get('origin') == room3_poi
    assert tsk_ctxs[2].get('origin') == room1_poi
    assert tsk_ctxs[3].get('origin') == room1_poi # stay still, action has no destination
    assert tsk_ctxs[3].get('destination') == room3_poi


