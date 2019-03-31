# Smart clock
## Idea
The idea is to create a smart clock with simple web interface. The
device should be able to handle multiple alarms, snoozing, alarms on
set days of week etc. Alarms should be played from MP3 that user
uploads (maybe internet radio later).

**Soft alarm** feature will play a soft sound several minutes before
the set time.

The clock will connect to WiFi and serve its own website (accessible
only locally first, maybe remotely later).

The clock will have an enclosure with a display and buttons.

## 1. Software
Simple web app:

- list alarms, add/edit alarms
- First implementation - bare-bones HTML
- Alarms are saved in a JSON file
- Nice to have: pretty, mobile friendly web page

Clock:

- Multi-threaded app that keeps track of time, plays alarms and
listens for button presses

## 2. Electronic hardware
Use a Raspberry Pi W, amplifier/speaker shield, display shield. Add
buttons/vibration sensors.

Figure out how to power it using one power source.

## 3. Enclosure
Create an aesthetically pleasing enclosure.
