#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
import requests
import json
import rrdtool
from flask import Flask, render_template

def index():
    # Abrufen der Daten aus der RRD-Tool-Datenbank
    graph = rrdtool.graph(
        "-",
        "--start", "-1d",
        "--title", "Himmelswetter",
        "--width", "800",
        "--height", "400",
        "--vertical-label", "Temperature (°C)",
        "DEF:temperature=weather_StFP.rrd:solarRadiation:AVERAGE",
        "LINE1:Sonne#ff0000:Sonneneinstrahlung"
    )

    return render_template('index.html', graph=graph.decode())

''' Struktur des importierten Datensatze
0stationID,ILAUCH27		1obsTimeUtc,2023-07-16T13:01:52Z		2timeStamp,2023-07-16 15:01:52	3neighborhood,Lauchhammer
4softwareType,EasyWeatherV1.5.7	5country,DE	6solarRadiation,567.4	7lon,13.73	8realtimeFrequency,	9epoch,1689512512
10lat,51.479	11uv,5.0	12winddir,247	13humidity,40	14qcStatus,1	15AmbientTemp,29	16heatIndex,29	17Taupunkt,14	18windChill,29
19windSpeed,6	20windGust,7	21pressure,1010.13	22precipRate,0.0	23precipTotal,3.0	24elev,29	25init,True	26mode,drop detect
27dropCount,2960	28dropFreq,0	29init,True	30T_amb,48.29000092	31T_obj,33.64998627	32init,True	33Lux,8928.601563	34Visible,16233	35IR,7804
36Gain,0	37Timing,1
'''

#create rrdtool database with all necessary data fields
rrdtool.create(
	"weather_StFP.rrd", # Station Far Point = StFP
    "--step", "180",  # Datenpunkte alle 3 Minuten
    "DS:timeStamp:GAUGE:300::", # 2 Zeitstempel der Messung
	"DS:solarRadiation:GAUGE:300:0:1000", # 6 Sonnen-Strahlung
	"DS:epoch:GAUGE:300::",  # 9 Unix-Epoche - Zeit absolut seit ??
    "DS:UV-Index:GAUGE:300:0:10",  # 11 UV-Index
	"DS:WindRichtung:GAUGE:300:0:360",  # 12 Windrichtung 
	"DS:LFeuchte:GAUGE:300:0:100",  # 13 Luftfeuchtigkeit
	"DS:AussenTemp:GAUGE:300:-40:+50",  # 15 Außentemperatur
	"DS:Taupunkt:GAUGE:300:-40:+40",  # 17 Taupunkt
	"DS:Windgeschw:GAUGE:300:0:100",  # 19 Windgeschwindigkeit
	"DS:Boeen:GAUGE:300:0:180",  # 20 Windboeenstärke
	"DS:Luftdruck:GAUGE:300:900:1300",  # 21 Luftdruck
	"DS:NDrate:GAUGE:300:0:1000",  # 22 ND pro Stunde
	"DS:NDmenge:GAUGE:300:0:100",  # 23 ND pro Quadratmeter
	"DS:Regentropfen:GAUGE:300:0:10000",  # 27 Anzahle der Regentropfen
	"DS:RegenFrequenz:GAUGE:300:0:1000",  # 28 Tropfen pro Minute
	"DS:WolkenUmgTemp:GAUGE:300:-30:+40",  # 30 UmgebungsTemp
	"DS:Wolkentemp:GAUGE:300:-30:+40",  # 31 ObjektTemp
	"DS:Helligkeit:GAUGE:300:0:20000",  # 33 Helligkeit in LUX
	"DS:VIS-Helligkeit:GAUGE:300:0:20000",  # 34 VIS Helligkeit
	"DS:IR-Helligkeit:GAUGE:300:0:20000",  # 35 IR-Helligkeit
    "RRA:AVERAGE:0.5:20:1200",  # Durchschnittswerte für 6h (3 Minuten pro Datenpunkt)
    "RRA:AVERAGE:0.5:480:24",  # Durchschnittswerte für 1 Tag (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:3360:7",  # Durchschnittswerte für 7 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:480:30",  # Durchschnittswerte für 30 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:480:60",  # Durchschnittswerte für 60 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:480:90",  # Durchschnittswerte für 90 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:1:365",  # Durchschnittswerte für 1 Jahr (1 d pro Datenpunkt)
)
# API key von www.weather.com 
api_key = '46cf957af9f541488f957af9f561488e'

# base url variable to store url
base_url = 'https://api.weather.com/v2/pws/observations/current?'

# give city name 
stationID = 'ILAUCH27'
# complete_url variable to store
complete_url = base_url + "stationId=" + stationID + "&format=json&units=m&apiKey=" + api_key

#get method of requests module
#return response object 
response = requests.get(complete_url)

#json method of response object
# convert json format data into python format data 
observations = response.json()

# data from weatherradio
wr_url="http://192.168.178.74"
response = requests.get(wr_url)
weather=response.json()

#Variablendefinition
i=0 # Index for Messwerte
Messwerte=[]

# Werte in Liste Messwerte schreiben

  	# Beobachtungsdaten ausgeben und schreiben
for obs in observations['observations']:
	for key, value in obs.items():
		if key != 'metric':
			Messwerte.insert(i,value)
			i=i+1
            	
for obs in observations['observations']:
	metric = obs['metric']
	for key, value in metric.items():
		Messwerte.insert(i,value)
		i=i+1
    		
		# Wetterdaten schreiben
for sensor, data in weather['weather'].items():
	if 'RG11 Rain Sensor' in sensor:
		for key, value in data.items():
			Messwerte.insert(i,value)
			i=i+1
	if 'MLX90614' in sensor:
		for key, value in data.items():
			Messwerte.insert(i,value)
			i=i+1
	if 'TSL2591' in sensor:
		for key, value in data.items():
			Messwerte.insert(i,value)
			i=i+1
			
# Lesen Sie die deserialisierten Messwerte als Variable in die rrdtool DB ein
timeStamp= Messwerte [2]
solarRadiation = Messwerte [6]
epoch = Messwerte[9]
UV-Index = Messwerte[11]
WindRichtung=Messwerte[12]
LFeuchte = Messwerte[13]
AussenTemp = Messwerte[15]
Taupunkt = Messwerte[17]
Windgeschw = Messwerte [19]
Boeen = Messwerte [20]
Luftdruck = Messwerte[21]
NDrate = Messwerte[22]
NDmenge = Messwerte[23]
Regentropfen = Messwerte[27]
RegenFrequenz = Messwerte[28]
WolkenUmgTemp = Messwerte[30]
Wolkentemp = Messwerte[31]
Helligkeit = Messwerte[33]
VIS-Helligkeit = Messwerte[34]
IR-Helligkeit= Messwerte[35]

rrdtool.update(
    "weather_StFP.rrd",
	str(timeStamp) + ":" + str(solarRadiation) + ":" +str(epoch) + ":" +str(UV-Index) + ":" 
		+str(WindRichtung) + ":" +str(LFeuchte) + ":" +str(AussenTemp) + ":" +str(Taupunkt) + ":" +str(Windgeschw) + ":" +str(Boeen) + ":" 
		+str(Luftdruck) + ":" +str(NDrate) + ":" +str(NDmenge) + ":" +str(Regentropfen) + ":" +str(RegenFrequenz) + ":" +str(WolkenUmgTemp) + ":" 
		+str(Wolkentemp) + ":" +str(Helligkeit) + ":" +str(VIS-Helligkeit) + ":" +str(IR-Helligkeit)
)   

#RRDtool graf. Darstellung
app = Flask(__name__)
@app.route('/')
if __name__ == '__main__':
    app.run()

