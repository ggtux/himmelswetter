#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
from numpy import sign
from math import log10, exp, pow, log
import requests
import csv

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

# Name der CSV-Datei
dateiname = "/home/geo/wetter_now.csv"

#Variablendefinition
calFac = 5.7
SQM = 19.0
#Wolkenbedeckung Konstanten anpassen!
K1 = 39.
K2 = 12.
K3 = 95.
K4 = 95.
K5 = 100.
K6 = 0.
K7 = 100.


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
			
# Lesen Sie die deserialisierten Messwerte als Variable ein
LFeuchte = Messwerte[13]
Ta = Messwerte[15]
Taupunkt = Messwerte[17]
Windgeschw = Messwerte [19]
Luftdruck = Messwerte[21]
NDmenge = Messwerte[23]
Regentropfen = Messwerte[27]
Tamb = Messwerte[30]
Tir = Messwerte[31]
Helligkeit = Messwerte[33]
VISHelligkeit = Messwerte[34]
IRHelligkeit= Messwerte[35]
SQM = calFac + (log((Helligkeit/108000.0),10)/-0.4)
#Wolkenbedeckung
if abs((K2/10-Tamb)) < 1:
    T67= sign(K6)*sign(Tamb-K2/10)*abs((K2/10-Tamb))
else:
     T67=K6/10*sign(Tamb-K2/10)*(log10(abs((K2/10-Tamb)))/log10(10)+K7/100)

Td=(K1/100)*(Tamb-K2/10)+(K3/100)*pow(exp(K4/1000*Tamb),(K5/100))+T67
Tsky=Tir-Td
Cldcov=100+((Tsky/8)*100)
print(format(Tsky,".2f"),format(Cldcov,".2f"),format(Ta,".2f"),format(Tamb,".2f"),format(Tir,".2f"))

# CSV-Datei zum Schreiben öffnen
with open(dateiname, mode='w', newline='') as datei:
            schreiber = csv.writer(datei)
            schreiber.writerow(["Temp/C: ", Ta])
            schreiber.writerow(["Druck/hPa: ", Luftdruck])
            schreiber.writerow(["Feuchte/%: ", LFeuchte])
            schreiber.writerow(["TauPkt/C: ", Taupunkt])
            schreiber.writerow(["WindV/m/s: ", Windgeschw])
            schreiber.writerow(["SQM/mag/bs² :",format (SQM,".1f")])
            schreiber.writerow(["Wolken/ % :", format (Cldcov,".1f")])
            schreiber.writerow(["NDmenge/mm/m²: ", NDmenge])
            #schreiber.writerow(["Tropfen: ", Regentropfen])
      
  	
#print('Alles fertig')

