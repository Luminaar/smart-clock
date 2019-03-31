import logging
import time
from datetime import datetime
from os.path import dirname, join
from threading import Thread

from alarm_handler import AlarmHandler
from external import snooze, stop

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = join(dirname(__file__), "../data")
ALARM_FILE = join(DATA_DIR, "alarms.json")


def synchronize():
    """Block until second 0."""
    run = True
    while run:
        second = datetime.now().second

        if second == 0:
            run = False
        elif second < 50:
            time.sleep(5)


def get_current_time():
    """Return current time in format used by the clock (HHMM)"""

    d = datetime.now()
    minute = str(d.minute)
    if len(minute) == 1:
        minute = "0" + minute

    print(f"{d.hour}:{minute}")

    return int(str(d.hour) + minute)


if __name__ == "__main__":
    interval_seconds = 60.0

    handler = AlarmHandler()
    handler.load_alarms(ALARM_FILE)

    # Simulate stopping the alarm from another thread (for example by
    # Raspberry Pi GPIO)
    Thread(target=snooze, args=(handler,)).start()
    Thread(target=stop, args=(handler,)).start()

    synchronize()

    starttime = time.time()

    while True:
        current_time = get_current_time()

        if current_time == 0:
            handler.load_alarms(ALARM_FILE)

        handler.check_time(current_time)
        time.sleep(interval_seconds - ((time.time() - starttime) % interval_seconds))
