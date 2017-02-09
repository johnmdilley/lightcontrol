import setlightswithretry
import heatercontrol
from flask import Flask, request
import waitress
import logging
import sys
from requestlogger import WSGILogger, ApacheFormatter


app = Flask("myiot")

@app.route("/sunrisesunset", methods=["POST"])
def sunrisesunset():
    if request.form['time'] == "sunrise":
        node = "Bedroom"
        attributes = {"brightness": 100, "colourTemperature": 5000}
        timeout = 18000
    elif request.form['time'] == "sunset":
        node = "Bedroom"
        attributes = {"brightness": 70, "colourTemperature": 2900}
        timeout = 18000
    elif request.form['time'] == "coldafternoon":
        node = "Conservatory"
        attributes = {"state": "ON"}
        timeout = 300

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
