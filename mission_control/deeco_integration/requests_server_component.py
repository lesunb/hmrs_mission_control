from deeco.core import Component, ComponentRole, BaseKnowledge

# Roles
class RequestsHandler(ComponentRole):
    __curr_requests_ids = None

    def __init__(self):
        super().__init__()
        self.requests = []
        self.mission_status = []
        

    def merge(self, o):
        n_ids = map(lambda n: n.id, o.requests)
        if self.curr_ids is None:
            self.__curr_requests_ids = map(lambda n: n.id, self.requests)
        
        diff = set(n_ids) - set(self.curr_ids)
        if diff is None:
            return 
        __curr_requests_ids = None
        to_add = filter(lambda n: __curr_requests_ids.contains(n.id), o.requests)
        self.requests.extends(to_add)
# Components
class MissionsServer(Component, RequestsHandler):

   # Knowledge definition
    class Knowledge(RequestsHandler, BaseKnowledge):
        def __init__(self):
            super().__init__()
