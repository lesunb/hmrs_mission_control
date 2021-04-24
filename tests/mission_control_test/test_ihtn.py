
from .lab_samples_exemplar import Roles
from .lab_samples_exemplar import ihtn_pickup_sample

def test_abstract_task_assign_to(ihtn_pickup_sample):
    obtained = ihtn_pickup_sample.assign_to
    expected = [Roles.r1, Roles.lab_arm, Roles.nurse]
    diff =  set(obtained) ^ set(expected)
    assert not diff

