#!/usr/bin/python

import cgi
import cgitb
import subprocess

cgitb.enable()

print "Content-type: text/plain\n"

form = cgi.FieldStorage()

time_of_day = form['time'].value

if time_of_day == "sunset":
    cmd = "python -u /home/pi/lightcontrol/setlightswithretry.py -n Bedroom -t 18000 brightness=70 colourTemperature=2900 2>&1 | logger -t lightcontrol"
elif time_of_day == "sunrise":
    cmd = "python -u /home/pi/lightcontrol/setlightswithretry.py -n Bedroom -t 18000 brightness=100 colourTemperature=5000 2>&1 | logger -t lightcontrol"
else:
    raise Exception("Only sunrise/sunset are valid")

subprocess.Popen(cmd, shell=True)
print "OK"
