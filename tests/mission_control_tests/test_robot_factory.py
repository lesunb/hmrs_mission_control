from mission_control.robot import robot_factory

def test_create_robot():
    robot = robot_factory('r1', (1, 2))
    assert robot.id == 'r1'