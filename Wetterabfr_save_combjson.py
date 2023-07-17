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
observations = response.json()

# data from weatherradio

wr_url="http://192.168.178.74"

response = requests.get(wr_url)

weather=response.json()

