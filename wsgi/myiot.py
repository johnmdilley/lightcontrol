import setlightswithretry
import heatercontrol
from flask import Flask, request
import waitress

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
    heatercontrol.start()
    waitress.serve(app, host='0.0.0.0', port=1025)
