#!/usr/bin/python3
#
# test script for adding the runtime of motors
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#
import requests
import json
import csv

# API-Endpunkte
api1_url = "https://api.weather.com/v2/pws/observations/current"
#api1_url = "https://api.weather.com/v2/pws/observations/current?stationId=ILAUCH27&format=json&units=m&apiKey=46cf957af9f541488f957af9f561488e"
api2_url = "http://192.168.178.74:80"
# Parameter für den ersten API-Aufruf
params1 = {
    "stationId": "ILAUCH27",
    "format": "json",
    "units": "m",
    "apiKey": "46cf957af9f541488f957af9f561488e"
}
# Parameter für den zweiten API-Aufruf
params2 = {}

# API-Aufrufe senden
response1 = requests.get(api1_url, params=params1)
response2 = requests.get(api2_url, params=params2)

# JSON-Daten aus API 1 abrufen
#response1 = requests.get(api1_url)
data1 = response1

# JSON-Daten aus API 2 abrufen
#response2 = requests.get(api2_url)
data2 = response2

# CSV-Datei erstellen und Header schreiben
csv_file = "data.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["stationID", "temperature", "humidity", "pressure"])

    # Daten aus API 1 in CSV schreiben
    for observation in data1["observations"]:
        writer.writerow([observation["stationID"],
                         observation["metric"]["temp"],
                         observation["humidity"],
                         observation["metric"]["pressure"]])

    # Daten aus API 2 in CSV schreiben
    writer.writerow([data2["weather"]["stationID"],
                     data2["weather"]["temperature"],
                     data2["weather"]["humidity"],
                     data2["weather"]["pressure"]])

# CSV-Datei anzeigen
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
