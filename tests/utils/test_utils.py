from tests.world_collector import *
from mission_control.utils import obj_to_string


def test_simple_obj():
    class ClsA:
        def __init__(self): 
            self.a= 11
            self.x= 3
    class ClsB(ClsA):
        def __init__(self):
            super().__init__()
            self.b= [22, 33]
    
    obj = ClsB()
    string = obj_to_string(obj)
    assert string


def test_circular_self_reference():
    class Cls:
        def __init__(self, name): 
            self.name= name
            self.ref, self.ref1 = None, None
    cla, clb = Cls('a'), Cls('b')
    cla.ref=clb
    clb.ref=cla
    cla.ref1=cla
    string = obj_to_string(cla)
    assert string


def test_circular_reference():
    class Cls:
        def __init__(self, name): 
            self.name= name
            self.ref, self.ref1, self.ref2, self.ref3, self.ref4 = None, None, None, None, None
    cla, clb, clc, cld = Cls('a'), Cls('b'), Cls('c'), Cls('d')
    cla.ref=clb
    clb.ref=clc
    clc.ref=cld
    cld.ref=cla
    cld.ref2=clb
    cld.ref3=clc
    cld.ref4=cld
    string = obj_to_string(cla)
    assert string


def test_to_string(ihtn_collect):
    string = obj_to_string(ihtn_collect)
    assert string

def test_dict_to_string():
    dictionary = {'key_a': 1, 'key_b': 2, 'key_c': [3, 4, 5]}
    string = obj_to_string(dictionary)
    assert string    