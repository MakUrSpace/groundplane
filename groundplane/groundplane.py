import json
from datetime import datetime
from uuid import uuid4

from murd import Murd
from groundplane.things import thing_types


class groundplane(Murd):
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
        return gp

    @property
    def things(self):
        return self.read(row="THING")

    def state(self):
        state = {"START_TIMESTAMP": datetime.utcnow().isoformat()}
        for thing in self.things:
            row = thing.pop('ROW')
            col = thing.pop('COL')
            thing_type = thing.pop('TYPE')
            state[col] = thing_types[thing_type](**thing).state()
        state["END_TIMESTAMP"] = datetime.utcnow().isoformat()
        return state

