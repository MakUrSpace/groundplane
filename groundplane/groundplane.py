from datetime import datetime
from uuid import uuid4

import murd
from murd import Murdi
import murd_ddb

from groundplane.things import thing_types


class Murdt(Murdi):
    @property
    def thing_name(self):
        return self['SORT']

    @property
    def thing_type(self):
        return thing_types[self['DEVICE_TYPE']]

    @property
    def attributes(self):
        return {key: value for key, value in self.items()
                if key not in [Murdi.region_key, Murdi.sort_key, 'TYPE']}


def indenture(func):
    def inner(self, *args, **kwargs):
        return func(*args, **kwargs)
    return inner


class groundplane:
    def __init__(self, murd_file=None):
        if murd_file is not None:
            murd.open_murd(murd_file)
            self.gpid = murd.read_first(region="IDENTIFIER")["GPID"]
            self.name = murd.read_first(region="NAME")["NAME"]
        else:
            self.gpid = str(uuid4())
            murd.update([
                {"REGION": "NAME", "SORT": "groundplane", "NAME": f"groundplane_{self.gpid}"},
                {"REGION": "IDENTIFIER", "GPID": self.gpid}])

        for thing in self.things:
            thing.pop('REGION')
            setattr(self, thing.thing_name,
                    thing.thing_type(**thing))

    @property
    def things(self):
        for thing in murd.read(region="THING"):
            yield Murdt(**thing)

    def add_thing(self, thing):
        murd.update([thing.get_definition()])
        setattr(self, thing.thing_name, thing)

    def state(self):
        state = {"START_TIMESTAMP": datetime.utcnow().isoformat()}
        for thing in self.things:
            thing_name = thing.pop(Murdt.sort_key)
            state[thing_name] = getattr(self, thing_name).state()
        state["TIMESTAMP"] = datetime.utcnow().isoformat()
        return state

    def upload_state(self):
        state = self.state()
        murd_ddb.update([{"REGION": self.gpid, "SORT": state['TIMESTAMP'], **state}])

    def request_state(self, requested_state):
        for thing in self.things:
            if thing.thing_name in requested_state:
                getattr(self,
                        thing.thing_name).request_state(requested_state.pop(thing.thing_name))
        return True

    update = indenture(murd.update)
    read = indenture(murd.read)
    delete = indenture(murd.delete)
    write_to_file = indenture(murd.write_murd)
    read_groundplane_file = indenture(murd.open_murd)
