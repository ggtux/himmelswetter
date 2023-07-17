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

# data from weatherradio

wr_url="http://192.168.178.74"

response = requests.get(wr_url)

y=response.json()

# combining both data sets

combined_data = {**x, **y}
path='/var/www/html'
#f=open(path+'/wetter_now.html','w') 

# converting to html code

html_code = "<html>\n\t<head>\n\t\t<title>Weather Data</title>\n\t</head>\n\t<body>\n\t\t<h1>Weather Data</h1>\n\t\t<ul>\n" 
for key, value in combined_data.items(): 
	html_code += "\t\t\t<li><b>{}</b>: {}</li>\n" .format(key, value) 
	print(html_code)
html_code += "\t\t</ul>\n\t</"
html_code += "\t\t</ul>\n\t</body>\n</html>"

print(html_code)
#f.write(html_code)

#f.close

