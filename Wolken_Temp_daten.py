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

# API key von www.openweather.com 
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

# data from PWS lokales "weatherradio"
wr_url="http://192.168.178.74"
response = requests.get(wr_url)
wetterdaten=response.json()

# Name der CSV-Ausgabedatei
dateiname = "~/wetter_rec.csv"

# Lesen Sie die deserialisierten Messwerte als Variable ein
# Zugriff auf die benötigten Felder
temp = raw_data['data'][0]['temp']
clouds = raw_data['data'][0]['clouds']

# Werte aus der JSON-Datei der PWS
BME280_temp = wetterdaten['weather']['BME280']['Temp']
DHT_temp = wetterdaten['weather']['DHT']['Temp']
MLX90614_t_amb = wetterdaten['weather']['MLX90614']['T amb']
MLX90614_t_obj = wetterdaten['weather']['MLX90614']['T obj']

Ta = temp
Bewoelkung = clouds
Tamb = MLX90614_t_amb
Tir = MLX90614_t_obj

#Variablendefinition und Berechnung der Bewölkung
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
if abs((K2/10-Tamb)) < 1:
    T67= sign(K6)*sign(Tamb-K2/10)*abs((K2/10-Tamb))
else:
     T67=K6/10*sign(Tamb-K2/10)*(log10(abs((K2/10-Tamb)))/log10(10)+K7/100)
Td=(K1/100)*(Tamb-K2/10)+(K3/100)*pow(exp(K4/1000*Tamb),(K5/100))+T67
Tsky=Tir-Td
Cldcov=100+((Tsky/8)*100)
# print(format(Tsky,".2f"),format(Cldcov,".2f"),format(Ta,".2f"),format(Tamb,".2f"),format(Tir,".2f"))

#Ausgabe
# CSV-Datei zum Schreiben öffnen
with open(dateiname, mode='a', newline='') as datei:
            schreiber = csv.writer(datei)
            schreiber.writerow([temp,Tamb, Tir,clouds])

#print('Alles fertig')
