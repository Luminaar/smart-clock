import dataclasses
import json
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Alarm:
    id: Optional[int] = None
    enabled: bool = False
    name: str = ""
    owner: str = ""

    hour: int = 8
    minute: int = 0

    mon: bool = False
    tue: bool = False
    wed: bool = False
    thu: bool = False
    fri: bool = False
    sat: bool = False
    sun: bool = False

    snooze_duration: int = 0
    snooze_count: int = 0

    soft: bool = False

    sound_file: str = "faded-eminem.wav"


class Storage:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.alarms = self.load()

    def load(self) -> Dict[int, Alarm]:
        try:
            with open(self.storage_path) as f:
                return {int(k): Alarm(**v) for k, v in json.load(f).items()}
        except:
            return {}

    def new(self, alarm: Alarm) -> None:
        try:
            _id = max(self.alarms.keys()) + 1
        except ValueError:
            _id = 1

        alarm.id = _id

        self.alarms[_id] = alarm
        self._save()

    def _save(self):
        alarms = {k: dataclasses.asdict(v) for k, v in self.alarms.items()}
        with open(self.storage_path, "w") as f:
            json.dump(alarms, f, indent=1)

    def get(self, _id: int) -> Optional[Alarm]:
        return self.alarms.get(_id, None)

    def update(self, id: int, alarm: Alarm) -> None:
        alarm.id = id
        self.alarms[id] = alarm
        self._save()

    def delete(self, id: int) -> Optional[Alarm]:
        try:
            alarm = self.alarms.pop(id)
            self._save()
            return alarm
        except KeyError:
            return None
