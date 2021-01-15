import json
from datetime import datetime
from uuid import uuid4

from murd import Murd, MurdMemory
from groundplane.things import thing_types


class murdt(MurdMemory):
    @property
    def thing_name(self):
        return self['COL']
    
    @property
    def thing_type(self):
        return thing_types[self['TYPE']]

    @property
    def attributes(self):
        return {key: value for key, value in self.items()
                if key not in ['ROW', 'COL', 'TYPE']}


class groundplane(Murd):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for thing in self.things:
            setattr(self, thing.thing_name,
                    thing.thing_type(**thing.attributes))

    @staticmethod
    def break_new_ground():
        gpid = str(uuid4())
        mems = [
            {"ROW": "GPID", "COL": gpid},
            {"ROW": "THING", "COL": "top_fdm", "TYPE": "wemo_insight", "DEVICE_NAME": "TopModFdm"},
            {"ROW": "THING", "COL": "bot_fdm", "TYPE": "wemo_plug", "DEVICE_NAME": "Nooxlay"},
            {"ROW": "THING", "COL": "latch_top", "TYPE": "latch", "PIN": 1},
            {"ROW": "THING", "COL": "latch_bot", "TYPE": "latch", "PIN": 2},
            {"ROW": "THING", "COL": "latch_cab", "TYPE": "latch", "PIN": 3},
            {"ROW": "THING", "COL": "ms_top", "TYPE": "mag_sensor", "PIN": 4},
            {"ROW": "THING", "COL": "ms_bot", "TYPE": "mag_sensor", "PIN": 5},
            {"ROW": "THING", "COL": "ms_cab", "TYPE": "mag_sensor", "PIN": 6},
            *[{"ROW": "THING", "COL": f"camera_{cam}", "TYPE": "camera", "DEVICE_NUMBER": cam}
              for cam in range(0, 16, 2)],
        ]
        gp = groundplane()
        gp.update(mems)
        gp = groundplane(murd=gp.murd)
        return gp

    @property
    def things(self):
        for thing in self.read(row="THING"):
            yield murdt(**thing)

    def state(self):
        state = {"START_TIMESTAMP": datetime.utcnow().isoformat()}
        for thing in self.things:
            row = thing.pop('ROW')
            thing_name = thing.pop('COL')
            thing_type = thing.pop('TYPE')
            state[thing_name] = getattr(self, thing_name).state() 
        state["END_TIMESTAMP"] = datetime.utcnow().isoformat()
        state["TIMESTAMP"] = state["END_TIMESTAMP"]
        return state
    
    def request_state(self, requested_state):
        for thing in self.things:
            if thing.thing_name in requested_state:
                getattr(self, thing.thing_name).request_state(requested_state.pop(thing.thing_name))
        return True
