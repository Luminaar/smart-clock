from clock import AlarmEvent, get_events

STORAGE_PATH = "test-alarms.json"


def test_get_events_single():

    alarms = {
        "1": {
            "id": "1",
            "enabled": True,
            "name": "Test",
            "owner": "Max",
            "hour": "7",
            "minute": "30",
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": False,
        }
    }

    events = get_events(alarms, 0)

    assert len(events) == 1
    event = events[0]
    assert event.name == "Test"
    assert event.time == 7 * 60 + 30


def test_get_events_single_soft():

    alarms = {
        "1": {
            "id": "1",
            "enabled": True,
            "name": "Test",
            "owner": "Max",
            "hour": "7",
            "minute": "30",
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": True,
        }
    }

    events = get_events(alarms, 0)

    assert len(events) == 1
    event = events[0]
    assert event.name == "Test"
    assert event.time == 7 * 60 + 30 - 3


def test_get_events_multiple():
    alarms = {
        "1": {  # Enabled
            "id": "1",
            "enabled": True,
            "name": "Test",
            "owner": "Max",
            "hour": "7",
            "minute": "30",
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": False,
        },
        "2": {  # Enabled
            "id": "2",
            "enabled": True,
            "name": "Test2",
            "owner": "Max",
            "hour": "8",
            "minute": "30",
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": False,
        },
        "3": {
            "id": "3",
            "enabled": True,
            "name": "Test2",
            "owner": "Max",
            "hour": "8",
            "minute": "30",
            "mon": False,  # Not today
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": False,
        },
        "4": {
            "id": "4",
            "enabled": False,  # Disabled
            "name": "Test3",
            "owner": "Max",
            "hour": "8",
            "minute": "30",
            "mon": True,
            "tue": True,
            "wed": True,
            "thu": True,
            "fri": True,
            "sat": False,
            "sun": False,
            "snooze_duration": "5",
            "snooze_count": "0",
            "soft": False,
        },
    }

    events = get_events(alarms, 0)

    assert len(events) == 2


def test_alarm_event_next():

    event = AlarmEvent("Test", 1000)

    assert event.next() is None


def test_alarm_event_next_soft():

    event = AlarmEvent("Test", 1000, soft=True)

    next_event = event.next()
    assert next_event.time == 1003
    assert next_event.soft is False


def test_alarm_event_next_snooze():

    event = AlarmEvent("Test", 1000, snooze_count=1, snooze_duration=5)

    next_event = event.next()

    assert next_event.time == 1005
    assert next_event.snooze_count == 0
