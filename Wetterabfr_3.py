#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
import requests
import json
import csv


# API key 
api_key = '46cf957af9f541488f957af9f561488e'

# base url variable to store url

base_url = 'https://api.weather.com/v2/pws/observations/current?'

# give city name 
stationID = 'ILAUCH27'

# complete_url variable to store

# complete url address

complete_url = base_url + "stationId=" + stationID + "&format=json&units=m&apiKey=" + api_key

#get method of requests module

#return response object 

response = requests.get(complete_url)

#json method of response object

# convert json format data into python format data 
x = response.json()

# data from weatherradio

wr_url="http://192.168.178.74"

response = requests.get(wr_url)

y=response.json()

# combining both data sets

combined_data = {**x, **y}

path='/home/geo'
csv_file=open(path+'/wetter_now.html','w') 

# converting to html code
# CSV-Datei erstellen und Header schreiben
#with open(csv_file, "w", newline="") as file:
    #writer = csv.writer(csv_file)
csvline=''
for key, value in combined_data.items():
		#csvline +='\n'.format(key,value)
		print(str().format(key,value))
		writer = csv.writer(csv_file)
		#csv_file(csvline)

# CSV-Datei anzeigen
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


