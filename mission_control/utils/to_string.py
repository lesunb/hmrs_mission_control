
class RefPath:
    def __init__(self, ids =[]):
        self.ids = ids
    def ref_path(self, obj): 
        index = self.ids.index(id(obj))
        if index == 0:
            return "'.'"
        else:
            return "'" + '/'.join(['..' for i in range(0, index)]) + "'"
    def __add__(self, obj):
        return RefPath(ids = [id(obj)] + self.ids)
    def __contains__(self, obj):
        return id(obj) in self.ids

def dict_to_string(obj: dict, start_ident='', parents=RefPath()):
    start, end = '{ ', ' }'
    ident, line_break = start_ident+'  ', '\n'

    field_pars = [f'{ident}{k}:{obj_to_string(v, ident, parents=parents)}' for k,v in obj.items()]
    return start + line_break.join(field_pars) + end

def set_to_string(obj: set, start_ident='', already_referenced=set()):
    ident, line_break = start_ident + '  ', '\n'
    return str(list(map( 
        lambda value: f'{obj_to_string(value, ident, already_referenced)}' + line_break
        , obj)))

def obj_to_string(obj, base_ident='', ident='  ', parents=RefPath()):
    primitive = (int, str, bool, enumerate, float)
    internal_ident = base_ident + ident
    if obj is None:
        return 'None'
    if isinstance(obj, primitive):
        return str(obj)
    if isinstance(obj, (set, list, tuple)):
        from_obj = enumeration_to_string_base(base_ident=internal_ident)
        return from_obj(obj, parents=parents)
    if isinstance(obj, type):
        return f'{obj.__module__}.{obj.__name__}'
    if isinstance(obj, dict):
        return key_value_to_string_base(get_keys=lambda o:o.keys(), get_values=lambda o,k:o[k])(obj, parents)
        #return dict_to_string(obj, internal_ident, parents=parents)
    if hasattr(obj, 'to_str'):
        return obj.to_str()
    if not hasattr(obj, '__dict__'):
        raise(f'non primitive not listed:{obj.__class__}')
    # object
    if obj in parents:
        return parents.ref_path(obj)
    def obj_get_keys(obj):
        keys = ['__class__']
        keys.extend(list(filter(lambda a: not a.startswith('__') and not callable(getattr(obj, a)), dir(obj))))
        return keys
    def obj_get_value(obj, key):
        return getattr(obj, key)

    from_obj = key_value_to_string_base(get_keys=obj_get_keys, get_values=obj_get_value, base_ident=internal_ident)
    return from_obj(obj, parents=parents+obj)

            
    # attrs = list(filter(lambda a: not a.startswith('__') and not callable(getattr(obj, a)), dir(obj)))
    # start, end = '{ ', ' }'
    # ident, line_break = start_ident +'  ', ',\n'
    # # fields_mapping =  map( 
    # #     lambda key: f'{ident}{key}:{obj_to_string(getattr(obj, key))}'
    # #     , attrs)
    # # content = line_break.join(str(x) for x in fields_mapping)
    # #return start + content + end
    # field_pars = [f'{ident}{k}:{obj_to_string(getattr(obj, k), ident)}' + line_break for k in attrs]
    # return start + line_break.join(field_pars) + end

    

def key_value_to_string_base(get_keys, get_values, mapping_func=obj_to_string, ident='  ', start='{\n', end='}', line_break=',\n', base_ident=''):
    internal_ident = base_ident + ident
    def func(target, parents: RefPath):
        field_pars = [f'{internal_ident}{k}: {mapping_func(get_values(target, k), base_ident=internal_ident, parents=parents )}' for k in get_keys(target)]
        string = start + line_break.join(field_pars) + '\n' + internal_ident + end
        return string

    return func

def enumeration_to_string_base(mapping_func=obj_to_string, ident='  ', start='[', end=']', line_break=', ', base_ident=''):
    internal_ident = base_ident + ident
    def func(target, parents: RefPath):
        # if id(target) in already_referenced:
        #     return '<>'
        # else:
        field_pars = [f'{mapping_func(k, base_ident=internal_ident, parents=parents)}' for k in target]
        return start + line_break.join(field_pars) + end
    return func




