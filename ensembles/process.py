
class KBAccess():
    def __init__(self, bound_to: Component):
        self.bound_to = bound_to
    
    def get(self, key):
        return self.bound_to[key]


class InjectedOutjectedFunc():
    def __init__(self, eval, inp = [], inoutp =[], outp = []):
        self.in_params = []
        self.out_params = []
    
    def bind(self, context):
        pass

    def call(self):
        params  = self.inject()
        result = self.eval(params)
        self.outject(result)

    def inject(self):
        pass

    def outject(self, out):
        pass



class InOutjectable(KBAccess):
    def __init__(self, inject: [string] = [], outject: [string] = []):
        super.__init__(kb)
        self.inject = inject
        self.outject = ouject

    def get_injections(self):
        parameters = []
        for field_id in self.inject:
            field = self.get(field_id)
            parameters.append((field_id, field))
        return parameters

    def set_outject(self, fields, values):
        key = 0
        # TODO check fields.lenght != values.lenght and raise error if not
        for out_field in self.outject:
            field = self.get(out_field)
            value = values[key]
            field.set_value(value)
            key += 1


class Mapping(InOutjectable):
    def __init__(self):
        pass


class Process(InOutjectable):
    def __init__(self, inject = [], outject = []):    
        self.inject_keys = inject
        self.outject_keys = outject
        self.kb = None
    
    def bind(self, component):
        self.kb = component.kb

    def call(self, fnc):
        parameters = self.get_injections()
        results = fnc(parameters)
        self.set_outject(parameters, results)


class Trigger:
    pass

class Periodic(Trigger):
    def __init__(self, period = 0):
        self.period = period

class Changed(Trigger):
    def __init__(self, field_id):
        self.field = field_id
