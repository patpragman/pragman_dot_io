# Digital Resume!
# Patrick Pragman
# Ciego Services
# 16APRIL2022
# Flask App to watch for changes in the weather

import os

from flask import Flask, render_template, request, jsonify, abort, send_file
from metar import Metar
from get_metar import get_metar
from wxdata import get_metars, get_tafs
from local_config import Path

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/wxwatch')
def wxwatch():
    return render_template('wxwatcher.html')

@app.route('/nbody.html')
def nbody():
    return render_template('nbody.html')

@app.route('/brief')
def brief():
    metars = get_metars()
    tafs = get_tafs()

    stations = ["PALP", "PAKU", "PASC", "PAQT", "PAAD", "PAKV", "PABR", "PABT"]

    for sta in stations:
        if sta not in metars:
            metars[sta] = {}
            metars[sta]['raw_text'] = \
                f"The station {sta} is currently unavailable.  Waiting on NWS data - try refreshing."
        if sta not in tafs:
            tafs[sta] = {}
            tafs[sta]['raw_text'] = \
                "The station {sta} is currently unavailable.  Waiting on NWS data - try refreshing."

    return render_template('brief.html', metars=metars, tafs=tafs, stations=stations)


@app.route('/brief2')
def brief2():
    metars = get_metars()
    tafs = get_tafs()

    stations = ["PALP", "PAKU", "PASC", "PAQT", "PAAD", "PAKV", "PABR", "PABT"]

    for sta in stations:
        if sta not in metars:
            metars[sta] = {}
            metars[sta][
                'raw_text'] = "The station " + sta + " is currently unavailable.  Waiting on NWS data - try refreshing."
        if sta not in tafs:
            tafs[sta] = {}
            tafs[sta][
                'raw_text'] = "The station " + sta + " is currently unavailable.  Waiting on NWS data - try refreshing."

    return render_template('brief2.html', metars=metars, tafs=tafs, stations=stations)


@app.route('/misc', defaults={'req_path': ''})
@app.route('/misc/<path:req_path>')
def misc(req_path):

    misc_files = os.listdir(f"{app.template_folder}/misc")

    if req_path in misc_files:
        return render_template(f"misc/{req_path}")
    else:
        return render_template('misc.html', files=misc_files)



@app.route('/get_metar', methods=['POST'])
def get_report():
    req_data = request.form['code']
    try:
        raw_report = get_metar(req_data)
        if raw_report[0]:
            # if the report returns, build it and send it.
            obs = Metar.Metar(raw_report[1])

            lowest = 100000
            for skc in obs.sky:
                # find the lowest ceiling
                ht = int(skc[1].value())

                # a ceiling is the lowest broken or overcast layer
                if (skc[0] == "BKN" or skc[0] == "OVC"):
                    if ht < lowest:
                        lowest = skc[1].value()

            # validate some of the things I want to send back
            # python gets angry if you don't make sure there is data to send
            try:
                vis = obs.vis.value()
            except:
                vis = 000
            try:
                wind = obs.wind_speed.value()
            except:
                wind = 0

            response = {"ICAO": obs.station_id,
                        "RAW": obs.code,
                        "VIS": vis,
                        "CX": lowest,
                        "WIND": wind,
                        "ERROR": False,
                        "ERROR_TYPE": "NA"}

            return jsonify(response)

        if not raw_report[0]:
            # if the report is unavailable, tell the user
            return jsonify({"ERROR": True,
                            "ICAO": req_data,
                            "ERROR_TYPE": raw_report[1]})
    except:
        # in the event that this process fails, we need to still send something back to the frontend
        # we'll call all of these "server errors" - at some point I should probably log these or something
        # I'm not sure what the best course of action for this would be.
        return jsonify({"ERROR": True,
                        "ICAO": req_data,
                        "ERROR_TYPE": "SERVER ERROR"})


@app.route('/get_stations', methods=['GET'])
def get_stations():
    # open up the stations list and send it as requested
    with open(Path.stations, "r") as station_list:
        data = station_list.read()
        return data


if __name__ == "__main__":
    app.run()
