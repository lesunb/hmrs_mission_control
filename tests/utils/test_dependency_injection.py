from lagom import Container

class A:
    def __init__(self):
        self.foo_str = 'foo'
    
    def foo(self):
        return self.foo_str

class B:
    def __init__(self, a: A):
        self.a = a

def test_inject():
    container = Container()
    b = container[B]
    assert b.a.foo() == 'foo'
