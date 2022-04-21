from mission_control.coordinator.estimating.core import TaskContext, create_context_gen
from mission_control.data_model.restrictions import Worker, POI
from mission_control.data_model.ihtn import ElementaryTask

def test_task_context_start():
    sr_poi = POI('storage_room')
    worker = Worker(location = sr_poi)
    tsk_ctx = TaskContext(worker)
    tsk_ctx.start()
    assert tsk_ctx.origin == sr_poi

def test_task_context_get_properties():
    sr_poi = POI('storage_room')
    room3_poi = POI('room3')

    worker = Worker(location = sr_poi)
    tsk_ctx = TaskContext(worker)
    tsk_ctx.start()
    task = ElementaryTask(type='navigate', destination=room3_poi)
    tsk_ctx = tsk_ctx.unwind(task)
    assert tsk_ctx.get('origin') == sr_poi
    assert tsk_ctx.get('destination') == room3_poi



sr_poi = POI('storage_room')
room1_poi = POI('room1')
room3_poi = POI('room3')
task1 = ElementaryTask(type='navigate', destination=room3_poi)
task2 = ElementaryTask(type='navigate', destination=room1_poi)
task3 = ElementaryTask(type='simple_action')
task4 = ElementaryTask(type='navigate', destination=room3_poi)

worker = Worker(location = sr_poi)
task_list = [task1, task2, task3, task4]

def test_task_context_position_unwinding():
    tsk_ctx = TaskContext(worker)
    tsk_ctx.start()
    tsk_ctxs = []
    for task in task_list:
        tsk_ctx = tsk_ctx.unwind(task)
        tsk_ctxs.append(tsk_ctx)

    assert tsk_ctxs[0].get('origin') == sr_poi
    assert tsk_ctxs[1].get('origin') == room3_poi
    assert tsk_ctxs[2].get('origin') == room1_poi
    assert tsk_ctxs[3].get('origin') == room1_poi # stay still, action has no destination
    assert tsk_ctxs[3].get('destination') == room3_poi



def test_create_task_context():
    task_context_gen = create_context_gen(worker, task_list)
    estimates = []
    task_ctxs = list(task_context_gen)
    last_ctx = task_ctxs[3]
    assert last_ctx.get('origin') == room1_poi