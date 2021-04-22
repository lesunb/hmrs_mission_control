class Field(object):
    def __init__(self, default_value=None):
        self._value = default_value
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for callback in self._observers:
            print('announcing change')
            callback(self._value)

    def bind_to(self, callback):
        print('bound')
        self._observers.append(callback)