from flask import Flask, redirect, render_template, request

from alarm import Alarm, Storage
from form import AlarmForm

app = Flask(__name__)


STORAGE_FILE = "../data/alarms.json"


@app.route("/")
def list():
    storage = Storage(STORAGE_FILE)
    return render_template("index.html", alarms=storage.alarms, getattr=getattr)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    storage = Storage(STORAGE_FILE)

    delete_id = request.args.get("delete", None)

    if delete_id:
        storage.delete(int(delete_id))
        return redirect("/")

    alarm_id = request.args.get("id", None)

    if alarm_id:
        alarm = storage.get(int(alarm_id))
    else:
        alarm = Alarm()

    form = AlarmForm(request.form, obj=alarm)

    if request.method == "POST" and form.validate():
        alarm = form.to_alarm()
        if alarm_id:
            storage.update(int(alarm_id), alarm)
        else:
            storage.new(alarm)
        return redirect("/")

    return render_template("edit.html", form=form, alarm=alarm)
