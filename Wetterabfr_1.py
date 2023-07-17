#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
import requests
import json

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

# data from another source

data = {"weather":{"RG11 Rain Sensor":{"init":True,"mode":"drop detect","count":17343,"drop freq":0},

"BME280":{"init":True,"Temp":41.72000122,"Pres":1002.323364,"Hum":14.43164063},

"DHT":{"init":True,"Temp":44.79999924,"Hum":16},

"MLX90614":{"init":True,"T amb":44.89000702,"T obj":31.5700016},

"TSL2591":{"init":True,"Lux":11694.69824,"Visible":15479,"IR":6059,"Gain":0,"Timing":1}}}

# combining both data sets

combined_data = {**x, **data}

# converting to html code

html_code = "<html>\n\t<head>\n\t\t<title>Weather Data</title>\n\t</head>\n\t<body>\n\t\t<h1>Weather Data</h1>\n\t\t<ul>\n" 
for key, value in combined_data.items(): 
	html_code += "\t\t\t<li><b>{}</b>: {}</li>\n" .format(key, value) 
html_code += "\t\t</ul>\n\t</"
html_code += "\t\t</ul>\n\t</body>\n</html>"

print(html_code)
#(html_code,"heute.html")

 
