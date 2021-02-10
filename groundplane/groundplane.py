from datetime import datetime
from uuid import uuid4

import murd
from murd import Murd
from murdaws import DDBMurd

from groundplane.things import thing_types


def indenture(func):
    def inner(self, *args, **kwargs):
        return func(*args, **kwargs)
    return inner


class groundplane(Murd):
    class M(dict):
        def __init__(self, **kwargs):
            kwargs = {"GROUP": "MISC", "SORT": "_", **kwargs}
            self.update(kwargs)

        @property
        def thing_name(self):
            return self['SORT']

        @property
        def thing_type(self):
            return thing_types[self['DEVICE_TYPE']]

        @property
        def attributes(self):
            return {key: value for key, value in self.items()
                    if key not in ['GROUP', 'SORT', 'TYPE']}


    def __init__(self, murd_file=None):
        super().__init__(murd_file)
        self.ddbmurd = DDBMurd("hyperspace")
        if murd_file is not None:
            self.gpid = self.read_first(group="IDENTIFIER")["GPID"]
            self.name = self.read_first(group="NAME")["NAME"]
        else:
            self.gpid = str(uuid4())
            self.update([
                {"GROUP": "NAME", "SORT": "groundplane", "NAME": f"groundplane_{self.gpid}"},
                {"GROUP": "IDENTIFIER", "GPID": self.gpid}])

        for thing in self.things:
            thing.pop('GROUP')
            setattr(self, thing.thing_name,
                    thing.thing_type(**thing))

    @property
    def things(self):
        for thing in self.read(group="THING"):
            yield self.M(**thing)

    def add_thing(self, thing):
        self.update([thing.get_definition()])
        setattr(self, thing.thing_name, thing)

    def state(self):
        state = {"START_TIMESTAMP": datetime.utcnow().isoformat()}
        for thing in self.things:
            thing_name = thing.pop('SORT')
            state[thing_name] = getattr(self, thing_name).state()
        state["TIMESTAMP"] = datetime.utcnow().isoformat()
        return state

    def upload_state(self, state=None):
        state = self.state() if state is None else state
        self.ddbmurd.update([{"GROUP": self.gpid, "SORT": state['TIMESTAMP'], **state}])

    def request_state(self, requested_state):
        for thing in self.things:
            if thing.thing_name in requested_state:
                getattr(self,
                        thing.thing_name).request_state(requested_state.pop(thing.thing_name))
        return True

    def write(self, filepath):
        super().write_murd(filepath)

