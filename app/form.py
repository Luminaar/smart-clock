from wtforms import BooleanField, Form, SelectField, StringField

from alarm import Alarm


class AlarmForm(Form):
    enabled = BooleanField("Enabled")
    name = StringField("Name")

    hour = StringField("Hour")
    minute = StringField("Minute")

    mon = BooleanField("P")
    tue = BooleanField("Ú")
    wed = BooleanField("S")
    thu = BooleanField("Č")
    fri = BooleanField("P")
    sat = BooleanField("S")
    sun = BooleanField("N")

    owner = StringField("Owner")

    durations = [("5", "5 minutes"), ("10", "10 minutes"), ("15", "15 minutes")]
    times = [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3")]
    snooze_duration = SelectField("Snooze duration", choices=durations)
    snooze_count = SelectField("Snooze times", choices=times)

    soft = BooleanField("SoftAlarm")

    def to_alarm(self):
        return Alarm(
            enabled=self.enabled.data,
            name=self.name.data,
            owner=self.owner.data,
            hour=self.hour.data,
            minute=self.minute.data,
            mon=self.mon.data,
            tue=self.tue.data,
            wed=self.wed.data,
            thu=self.thu.data,
            fri=self.fri.data,
            sat=self.sat.data,
            sun=self.sun.data,
            snooze_duration=self.snooze_duration.data,
            snooze_count=self.snooze_count.data,
            soft=self.soft.data,
        )
