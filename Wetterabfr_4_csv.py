import csv

# Beobachtungen
observations = [{'stationID': 'ILAUCH27', 'obsTimeUtc': '2023-07-06T05:37:44Z', 'obsTimeLocal': '2023-07-06 07:37:44', 'neighborhood': 'Lauchhammer', 'softwareType': 'EasyWeatherV1.5.7', 'country': 'DE', 'solarRadiation': 194.3, 'lon': 13.73, 'realtimeFrequency': None, 'epoch': 1688621864, 'lat': 51.479, 'uv': 1.0, 'winddir': 166, 'humidity': 65, 'qcStatus': 1, 'metric': {'temp': 18, 'heatIndex': 18, 'dewpt': 12, 'windChill': 18, 'windSpeed': 1, 'windGust': 2, 'pressure': 1013.24, 'precipRate': 0.0, 'precipTotal': 0.0, 'elev': 29}}]

# Wetterdaten
weather = {'RG11 Rain Sensor': {'init': True, 'mode': 'drop detect', 'count': 17385, 'drop freq': 0}, 'BME280': {'init': True, 'Temp': 53.90999985, 'Pres': 1007.815613, 'Hum': 10.43652344}, 'DHT': {'init': True, 'Temp': 54.09999847, 'Hum': 22}, 'MLX90614': {'init': True, 'T amb': 53.89000702, 'T obj': 33.06999969}, 'TSL2591': {'init': True, 'Lux': 60517.15234, 'Visible': 64145, 'IR': 20523, 'Gain': 0, 'Timing': 1}}

# Name der CSV-Datei
dateiname = "/home/geo/wetter_now.csv"

# CSV-Datei zum Schreiben öffnen
with open(dateiname, mode='w', newline='') as datei:
		schreiber = csv.writer(datei)
	# Beobachtungsdaten ausgeben und schreiben
		for obs in observations:
			station_id = obs['stationID']
			#datei.write(str(["StationID", station_id]))
			obs_time_utc = obs['obsTimeUtc']
			obs_time_local = obs['obsTimeLocal']
			#print("Ortszeit", obs_time_local)
			neighborhood = obs['neighborhood']
			country = obs['country']
			humidity = obs['humidity']
			#print("Luftfeuchte",humidity)	
			wind_dir=obs['winddir']
			#print("Windrichtung",wind_dir)	
		schreiber.writerow(['Wetterstation',station_id,'\n', 'Ortszeit:',obs_time_local,'\n', 'Luftfeuchte:',humidity,'\n', 'Windrichtung:',wind_dir])	
		for obs in observations:
			metric = obs['metric']
			for key, value in metric.items():
				print(key, value)
				schreiber.writerow([key,value])     
		# Wetterdaten schreiben
		for sensor, data in weather.items():
				if 'RG11 Rain Sensor' in sensor:
					for key, value in data.items():
						print(key, value)
						schreiber.writerow([key,value])	
				if 'MLX90614' in sensor:
					for key, value in data.items():
						print(key, value)		
						schreiber.writerow([key,value])
				if 'TSL2591' in sensor:
					for key, value in data.items():
						print(key, value)
						schreiber.writerow([key,value])
			
			
