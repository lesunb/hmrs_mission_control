from mission_control.mission.ihtn import ElementaryTask
from mission_control.processes.sequencing import ActiveSkillController, SequencingProcess, TaskStatus, LocalMissionController

from ..world_collector import *

def test_mission_no_mission():
    seq_proc = SequencingProcess(None)
    task_status = TaskStatus()
    local_mission  = LocalMissionController(None)
    seq_proc.run(local_mission, None, task_status=task_status)
    
    # just check nothing breaks when running a non completly started process
    assert True

def test_mission_start(ihtn_collect):
    seq_proc = SequencingProcess(skill_library = collector_skill_library)
    task_status = TaskStatus()
    local_mission_ctrl  = LocalMissionController(ihtn_collect)
    active_skill_crl= ActiveSkillController()
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    
    assert isinstance(local_mission_ctrl._curr_task, ElementaryTask)


def test_task_finished_and_has_next():
    global_mission = collection_ihtn.collect.value.clone()
    seq_proc = SequencingProcess(skill_library = collector_skill_library)
    task_status = TaskStatus()
    local_mission_ctrl  = LocalMissionController(global_mission)
    active_skill_crl= ActiveSkillController()
    
    # Two ticks to complete the first task
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    assert local_mission_ctrl._curr_task == collection_ihtn.navto_room3.value
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    assert local_mission_ctrl._curr_task is None

    # Next tick loads the next task
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    assert isinstance(local_mission_ctrl._curr_task, ElementaryTask)
    assert local_mission_ctrl._curr_task == collection_ihtn.pick_up_object.value


def test_mission_just_finished():
    global_mission = collection_ihtn.collect.value.clone()
    seq_proc = SequencingProcess(skill_library = collector_skill_library)
    task_status = TaskStatus()
    local_mission_ctrl  = LocalMissionController(global_mission)
    active_skill_crl= ActiveSkillController()
    
    # Two ticks to complete the first task
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)

    # Next tick loads the next task
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    assert local_mission_ctrl._curr_task == collection_ihtn.pick_up_object.value
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
     # mission concluded
    assert local_mission_ctrl._curr_task == None
    assert local_mission_ctrl.status == LocalMissionController.Status.CONCLUDED_WIH_SUCCESS

    # nothing more is done
    assert active_skill_crl.is_idle()
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    seq_proc.run(local_mission_ctrl, active_skill_crl, task_status=task_status)
    assert active_skill_crl.is_idle()
    
