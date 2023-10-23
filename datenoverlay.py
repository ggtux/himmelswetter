#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
from numpy import sign
from math import log10, exp, pow, log
import requests
import csv
import time
from datetime import datetime, timezone, timedelta
import json



# API key von www.weather.com 
api_key = '4f9ffdab37989a944d92a452e4277819'

# base url variable to store url
base_url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?'

# give city name 
lat='51.4798'
lon='13.7319'

# Aktuelle Zeit als Unix-Zeitstempel
dt = int(time.time())
dts=str(dt)

# complete_url variable to store
complete_url = base_url + "lat="+lat + "&lon="+lon +"&dt=" + dts + "&units=metric" + "&appid=" + api_key

#get method of requests module
#return response object 
response = requests.get(complete_url)

#json method of response object
# convert json format data into python format data 
raw_data = response.json()

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
# Zugriff auf die benötigten Felder
sunrise = raw_data['data'][0]['sunrise']
sunset = raw_data['data'][0]['sunset']
temp = raw_data['data'][0]['temp']
pressure = raw_data['data'][0]['pressure']
dewpoint = raw_data['data'][0]['dew_point']
clouds = raw_data['data'][0]['clouds']
windspeed = raw_data['data'][0]['wind_speed']
weather_desc = raw_data['data'][0]['weather'][0]['description']

# Überprüfen, ob das 'rain'-Feld existiert
if 'rain' in raw_data['data'][0]:
    rain_1h = raw_data['data'][0]['rain']['1h']
else:
    rain_1h = None
    
# Umwandeln der Unix-Zeitstempel in Datetime-Objekte
sunrise_utc = datetime.fromtimestamp(sunrise, timezone.utc)
sunset_utc = datetime.fromtimestamp(sunset, timezone.utc)
utc_offset = timedelta(hours=2)
sunrise_utc2 = sunrise_utc.astimezone(timezone(utc_offset))
sunset_utc2 = sunset_utc.astimezone(timezone(utc_offset))
# Umwandeln in das gewünschte Zeitformat (z.B. 'YYYY-MM-DD HH:MM:SS')
sunrise_formatted = sunrise_utc2.strftime('%H:%M:%S')
sunset_formatted = sunset_utc2.strftime('%H:%M:%S')


Ta = Messwerte[12]
Taupunkt = dewpoint
Windgeschw = windspeed
Luftdruck = pressure
Bewölkung = clouds
Wetter = weather_desc
NDmenge = rain_1h
Regentropfen = Messwerte[2]
Tamb = Messwerte[5]
Tir = Messwerte[6]
Helligkeit = Messwerte[8]
VISHelligkeit = Messwerte[9]
IRHelligkeit= Messwerte[10]
SQM = calFac + (log((Helligkeit/108000.0),10)/-0.4)

#Wolkenbedeckung
if abs((K2/10-Tamb)) < 1:
    T67= sign(K6)*sign(Tamb-K2/10)*abs((K2/10-Tamb))
else:
     T67=K6/10*sign(Tamb-K2/10)*(log10(abs((K2/10-Tamb)))/log10(10)+K7/100)

Td=(K1/100)*(Tamb-K2/10)+(K3/100)*pow(exp(K4/1000*Tamb),(K5/100))+T67
Tsky=Tir-Td
Cldcov=100+((Tsky/8)*100)
# print(format(Tsky,".2f"),format(Cldcov,".2f"),format(Ta,".2f"),format(Tamb,".2f"),format(Tir,".2f"))

# CSV-Datei zum Schreiben öffnen
with open(dateiname, mode='w', newline='') as datei:
            schreiber = csv.writer(datei)
            schreiber.writerow(["Sonnenaufgang: ", sunrise_formatted])
            schreiber.writerow(["Wetter: ",Wetter])
            schreiber.writerow(["Temp/C: ", temp])
            schreiber.writerow(["Druck/hPa: ", Luftdruck])
            schreiber.writerow(["TauPkt/C: ", Taupunkt])
            schreiber.writerow(["Bewölkung/%: ", Bewölkung])
            schreiber.writerow(["WindV/m/s: ", Windgeschw])
            schreiber.writerow(["SQM/mag/bs² :",format (SQM,".1f")])
            schreiber.writerow(["Regen in 1h :", format (rain_1h)])
            schreiber.writerow(["NDmenge/mm/m²: ", NDmenge])
            schreiber.writerow(["Sonnenuntergang: ", sunset_formatted])
            schreiber.writerow(["Tropfen: ", Regentropfen])
      

#print('Alles fertig')
