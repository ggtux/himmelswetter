#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import rrdtool

rrdtool.create(
    "weather_data.rrd",
    "--step", "300",  # Datenpunkte alle 5 Minuten
    "DS:temperature:GAUGE:600:-50:50",  # Temperaturwerte
    "DS:humidity:GAUGE:600:0:100",  # Feuchtigkeitswerte
    "RRA:AVERAGE:0.5:1:2016",  # Durchschnittswerte für 7 Tage (5 Minuten pro Datenpunkt)
    "RRA:AVERAGE:0.5:12:864",  # Durchschnittswerte für 60 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:288:365"  # Durchschnittswerte für 1 Jahr (1 Tag pro Datenpunkt)
)

import rrdtool
import time

# Lesen Sie die deserialisierten Daten aus der JSON-Datei oder dem API-Aufruf
# und speichern Sie sie in Variablen (z.B. temperature und humidity).

timestamp = str(int(time.time()))  # Aktueller Zeitstempel in Sekunden
temperature = 12.5
humidity = 85

rrdtool.update(
    "weather_data.rrd",
    timestamp + ":" + str(temperature) + ":" + str(humidity)
)
'''    
from flask import Flask, render_template
import rrdtool

app = Flask(__name__)

@app.route('/')
def index():
    # Abrufen der Daten aus der RRD-Tool-Datenbank
    graph = rrdtool.graph(
        "-",
        "--start", "-1d",
        "--title", "Weather Data",
        "--width", "800",
        "--height", "400",
        "--vertical-label", "Temperature (°C)",
        "DEF:temperature=weather_data.rrd:temperature:AVERAGE",
        "LINE1:temperature#ff0000:Temperature"
    )

    return render_template('index.html', graph=graph.decode())

if __name__ == '__main__':
    app.run()
'''