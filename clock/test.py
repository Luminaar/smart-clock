from alarm_handler import substract_time


def test_substract_time():

    hour, minute = substract_time(14, 13, 3)

    assert hour == 14
    assert minute == 10


def test_substract_time_cross_hours():

    hour, minute = substract_time(14, 1, 3)

    assert hour == 13
    assert minute == 58


def test_substract_time_midnight():

    hour, minute = substract_time(0, 0, 3)

    assert hour == 23
    assert minute == 57
