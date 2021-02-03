from datetime import datetime
from uuid import uuid4

import murd
from murd import Murdi

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


class groundplane:
    def __init__(self, murd_file=None):
        if murd_file is not None:
            murd.open_murd(murd_file)
            self.gpid = murd.read_first(REGION="IDENTIFIER")["GPID"]
            self.name = murd.read_first(REGION="NAME")["NAME"]
        else:
            self.gpid = str(uuid4())
            murd.update([
                {"REGION": "NAME", "SORT": "groundplane", "NAME": f"groundplane_{self.gpid}"},
                {"REGION": "IDENTIFIER", "GPID": self.gpid}])

        for thing in self.things:
            setattr(self, thing.thing_name,
                    thing.thing_type(**thing.attributes))

    @property
    def things(self):
        for thing in murd.read(region="THING"):
            yield Murdt(**thing)

    def state(self):
        state = {"START_TIMESTAMP": datetime.utcnow().isoformat()}
        for thing in self.things:
            thing.pop(Murdt.region_key)
            thing.pop('TYPE')
            thing_name = thing.pop(Murdt.sort_key)
            state[thing_name] = getattr(self, thing_name).state()
        state["END_TIMESTAMP"] = datetime.utcnow().isoformat()
        state["TIMESTAMP"] = state["END_TIMESTAMP"]
        return state

    def request_state(self, requested_state):
        for thing in self.things:
            if thing.thing_name in requested_state:
                getattr(self,
                        thing.thing_name).request_state(requested_state.pop(thing.thing_name))
        return True
