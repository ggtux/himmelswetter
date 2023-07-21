#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
import requests
# import json wird nicht verwendet
import rrdtool

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
UVIndex = Messwerte[11]
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
VISHelligkeit = Messwerte[34]
IRHelligkeit= Messwerte[35]

#Pfad zur DB anpassen

rrdtool.update(
    "weather_StFP.rrd",
	str(timeStamp) + ":" + str(solarRadiation) + ":" +str(epoch) + ":" +str(UV-Index) + ":" 
		+str(WindRichtung) + ":" +str(LFeuchte) + ":" +str(AussenTemp) + ":" +str(Taupunkt) + ":" +str(Windgeschw) + ":" +str(Boeen) + ":" 
		+str(Luftdruck) + ":" +str(NDrate) + ":" +str(NDmenge) + ":" +str(Regentropfen) + ":" +str(RegenFrequenz) + ":" +str(WolkenUmgTemp) + ":" 
		+str(Wolkentemp) + ":" +str(Helligkeit) + ":" +str(VIS-Helligkeit) + ":" +str(IR-Helligkeit)
)   
