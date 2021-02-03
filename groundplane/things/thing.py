from datetime import datetime
from inspect import signature


class thing:
    def __init__(self, SORT):
        self.SORT = SORT

    @classmethod
    def get_definition_keys(cls):
        return [p for p in signature(cls.__init__).parameters.keys() if p != 'self']

    def get_definition(self):
        return {"REGION": "THING", "SORT": self.SORT,
                **{key: self.__dict__[key] for key in self.get_definition_keys()}}

    def state(self):
        return {"TIMESTAMP": datetime.utcnow().isoformat()}

    def request_state(self, requested_state):
        return True
