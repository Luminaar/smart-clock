# Idea
Create a smart clock, that has a simple web interface to set multiple
alarm clocks. Set repeatable alarms, alarms on days of week etc.
Unlimited number of alarms. Alarms are played from mp3s.

"Soft" alarm - like on android phone (start playing a soft toon
shortly before set time).

Create a physical clock with speakers, display, snooze/off buttons.

Make it as pretty as possible.

# 1. Software
Simple web app

- list alarms, add/edit alarms
- Copy the interface from android alarm
- First implementation - barebones HTML
- Nice to have: pretty, mobile
friendly web page.
- Save alarms in simple format in a file (no databases)

MP3 Player

- A component that can load, play, stop MP3s
- Fade in/out, pause

Timer

- A (async?) loop that checks time and plays correct alarms
- Alarm in progress must be possible to stop with user input

# 2. Electronic hardware
Use a Raspberry Pi W, amplifier/speaker shield, display shield. Add
buttons/vibration sensors.

Figure out how to power it using one power source.

# 3. Enclosure
Create an aesthetically pleasing enclosure
