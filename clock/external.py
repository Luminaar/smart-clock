import logging

import keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def snooze(app):
    while True:
        try:
            keyboard.wait("space")
            app.snooze()
        except:
            logger.info("Nothing to snooze")


def stop(app):
    while True:
        try:
            keyboard.wait("esc")
            app.stop()
        except:
            logger.info("Nothing to stop")
