#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Module laden
import requests
import json
import csv

#API key von weather.com (weatherunderground)
api_key = '1111' # korrekt einsetzen

#base url variable to store url

base_url = 'https://api.weather.com/v2/pws/observations/current?'

#Stationsname
stationID = 'ILAUCH27' # anpassen!

# complete_url variable to store url adress

complete_url = base_url + "stationID=" + stationID + "&format=json&units=m&apiKey=" +api_key

#get methode of requests module, returns response object

response = requests.get(complete_url)

#json methode of response object, convert json format data into python format data

observations = response.json()

# #data von der Sensorbank zu Testzwecken auskommentiert
# wr_url = "http://192.168.178.74"
#response = request.get(wr_url)
#weather = response.json()
## Name für tem. Ausgabedatei in csv-Format

#dateiname = "/home/---/WetterDB/wetter_now-csv"

#CSV-Datei zum Schreiben öffnen
with open(dateiname,mode='w', newline=' ') as datei:
    schreiber = csv.writer(datei)
    #Beobachtungsdaten ausgeben und schreiben
    for obs in observations['observations']:
        for key, value in obs.items():
            if key != 'metric':
                schreiber.writerow([key,value])
    for obs in observations['observations']:
        metric = obs['metric']
        for key,value in metric.items():
            schreiber.writerow([key,value])
    '''
    # Sensordaten schreiben, wieder auskommentiert zu Testzwecken
    