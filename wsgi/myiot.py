import setlightswithretry
import heatercontrol
from flask import Flask, request
import waitress
import logging
import sys
from requestlogger import WSGILogger, ApacheFormatter
import dtgweather

app = Flask("myiot")

@app.route("/scarletroom", methods=["POST", "GET"])
def scarletroom():
    print "Running scarletroom"
    myform = request.args if request.method == "GET" else request.form
    print myform
    if myform['key'] != "mhmlw":
        raise Exception("Invalid key")
    if myform['action'] == "night":
        attributes = {
            "brightness": 5,
            "hsvSaturation": 99,
            "hsvValue": 5,
            "hsvHue": 293,
            "colourMode": "COLOUR",
            "state": "ON"
        }
    elif myform['action'] == "day":
        attributes = {
            "brightness": 100,
            "colourMode": "TUNABLE",
            "colourTemperature": 3500,
            "state": "ON"
        }
    elif myform['action'] == "off":
        attributes = {"state": "OFF"}
    setter = setlightswithretry.ThreadedLightSetter("Scarlet Room", attributes, 0)
    setter.start()
    return "OK\n"

@app.route("/sunrisesunset", methods=["POST","GET"])
def sunrisesunset():
    print "Running sunrisesunset"
    myform = request.args if request.method == "GET" else request.form
    print myform
    if myform['key'] != "mhmlw":
        raise Exception("Invalid key")
    if myform['time'] == "sunrise":
        node = "Bedroom"
        attributes = {"brightness": 100, "colourTemperature": 5000}
        timeout = 18000
    elif myform['time'] == "sunset":
        node = "Bedroom"
        attributes = {"brightness": 70, "colourTemperature": 2900}
        timeout = 18000
    elif myform['time'] == "afternoon":
        if dtgweather.get_temperature() < 10: 
            node = "Conservatory"
            attributes = {"state": "ON"}
            timeout = 300
        else:
            return "Too warm\n"
    else:
        raise Exception("Unknown time")

    setter = setlightswithretry.ThreadedLightSetter(node, attributes, timeout)
    setter.start()
    return "OK\n"

if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    heatercontrol.start()
    loggingapp = WSGILogger(app, [ch], ApacheFormatter())
    waitress.serve(loggingapp, host='0.0.0.0', port=1025)
