import dataclasses
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from os.path import dirname, join
from queue import PriorityQueue
from threading import RLock
from typing import Optional

from simpleaudio import WaveObject

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DAYS = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
DATA_DIR = join(dirname(__file__), "../data/sounds")


def substract_time(hour, minute, n):
    """Substract 'n' minutes from time."""

    d = datetime(2, 2, 2, hour, minute) - timedelta(0, n * 60)

    return d.hour, d.minute


@dataclass
class AlarmEvent:

    name: str
    time: int
    snooze_count: int = 0
    snooze_duration: int = 0
    soft: bool = False
    music_object: Optional[WaveObject] = None

    def next(self):
        if self.soft:
            return dataclasses.replace(self, time=self.time + 3, soft=False)

        elif self.snooze_count > 0:
            return dataclasses.replace(
                self,
                time=self.time + self.snooze_duration,
                snooze_count=self.snooze_count - 1,
            )
        else:
            return None

    def start(self):
        self.play_obj = self.music_object.play()

    def stop(self):
        self.play_obj.stop()


class AlarmHandler:
    def __init__(self):
        self.queue = PriorityQueue()
        self.active = None
        self.active_lock = RLock()

    def load_alarms(self, alarm_file):
        def events():
            with open(alarm_file) as f:
                alarms_json = json.load(f)

            for k, v in alarms_json.items():

                if v["enabled"] and v[DAYS[datetime.now().weekday()]]:

                    minute = int(v["minute"])
                    hour = int(v["hour"])

                    # Handle 'soft' time
                    if v["soft"]:
                        hour, minute = substract_time(hour, minute, 3)

                    if len(v["minute"]) == 1:
                        minute = "0" + str(minute)

                    # Load music object
                    path = join(DATA_DIR, v["sound_file"])
                    music_obj = WaveObject.from_wave_file(path)

                    yield AlarmEvent(
                        name=v["name"],
                        time=int(str(hour) + str(minute)),
                        snooze_count=int(v["snooze_count"]),
                        snooze_duration=int(v["snooze_duration"]),
                        music_object=music_obj,
                    )

        logger.info("# Loading alarms")
        for alarm in events():
            self.add_event(alarm)

    def add_event(self, event: AlarmEvent):
        self.queue.put((event.time, event))
        logger.info(
            f"  {event.name}, {event.time} ({event.snooze_count}: {event.snooze_duration})"
        )

    def check_time(self, time: int):
        """Get first event from the queue and check it agains the
        passed time. If the time matches, play the event.
        Otherwise, put it back into the queue."""

        with self.active_lock:
            if not self.queue.empty():
                if self.active:
                    self.snooze()
                first = self.queue.get()
                if first and first[1].time == time:
                    first = first[1]
                    self.active = first
                    self.active.start()
                    logger.info(f"Activating '{first.name}'")
                elif first:
                    self.queue.put(first)

    def stop(self):
        with self.active_lock:
            name = self.active.name
            if self.active:
                self.active.stop()
                self.active = None
            logger.info(f"Alarm '{name}' stopped")

    def snooze(self):
        with self.active_lock:
            name = self.active.name
            if self.active:
                self.active.stop()
                next_event = self.active.next()
                if next_event:
                    logger.info(f"Adding next alarm '{name}' at {next_event.time}")
                    self.queue.put((next_event.time, next_event))
                self.active = None
            logger.info(f"Alarm '{name}' snoozed")
