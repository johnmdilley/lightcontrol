import setlightswithretry
import heatercontrol
from flask import Flask, request
app = Flask("myiot")


@app.route("/sunrisesunset", methods=["POST"])
def sunrisesunset():
    if request.form['time'] == "sunrise":
        node = "Bedroom"
        attributes = {"brightness": 100, "colourTemperature": 5000}
    elif request.form['time'] == "sunset":
        node = "Bedroom"
        attributes = {"brightness": 70, "colourTemperature": 2900}
    elif request.form['time'] == "test":
        node = "Bedroom1"
        attributes = {"brightness": 70, "colourTemperature": 2900}

    setter = setlightswithretry.ThreadedLightSetter(node, attributes, 18000)
    setter.start()
    return "OK\n"

heatercontrol.start()

if __name__ == "__main__":
    app.run()
