import requests
import csv
import time
from datetime import datetime, timezone, timedelta
from math import log10, exp, pow, log
from numpy import sign

# API key von www.openweather.com
api_key = 'cc8422f9b9feae7e10d4d30561f5a71a'

# base url variable to store url
base_url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?'

# give city name
lat = '51.4798'
lon = '13.7319'

# Aktuelle Zeit als Unix-Zeitstempel
dt = int(time.time())
dts = str(dt)

# complete_url variable to store
complete_url = base_url + "lat=" + lat + "&lon=" + lon + "&dt=" + dts + "&units=metric" + "&appid=" + api_key

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into python format data
raw_data = response.json()

# Name der CSV-Ausgabedatei
#dateiname = "/home/pi/wetter_now.csv"
# Name der CSV-Ausgabedatei
dateiname1 = "/home/pi/wetter_rec.csv"
dateiname2 = "C:/Users/X0GEOR1/wetter_now.csv"

# Lesen Sie die deserialisierten Messwerte als Variable ein
# Zugriff auf die benötigten Felder
datetime = dts
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

# Werte aus der JSON-Datei der PWS
wr_url = "http://192.168.178.74"
response = requests.get(wr_url)
wetterdaten = response.json()

RG11_init = wetterdaten['weather']['RG11 Rain Sensor']['init']
RG11_mode = wetterdaten['weather']['RG11 Rain Sensor']['mode']
RG11_count = wetterdaten['weather']['RG11 Rain Sensor']['count']
RG11_drop_freq = wetterdaten['weather']['RG11 Rain Sensor']['drop freq']

BME280_init = wetterdaten['weather']['BME280']['init']
BME280_temp = wetterdaten['weather']['BME280']['Temp']
BME280_pres = wetterdaten['weather']['BME280']['Pres']
BME280_hum = wetterdaten['weather']['BME280']['Hum']

DHT_init = wetterdaten['weather']['DHT']['init']
DHT_temp = wetterdaten['weather']['DHT']['Temp']
DHT_hum = wetterdaten['weather']['DHT']['Hum']

MLX90614_init = wetterdaten['weather']['MLX90614']['init']
MLX90614_t_amb = wetterdaten['weather']['MLX90614']['T amb']
MLX90614_t_obj = wetterdaten['weather']['MLX90614']['T obj']

TSL2591_init = wetterdaten['weather']['TSL2591']['init']
TSL2591_lux = wetterdaten['weather']['TSL2591']['Lux']
TSL2591_visible = wetterdaten['weather']['TSL2591']['Visible']
TSL2591_ir = wetterdaten['weather']['TSL2591']['IR']
TSL2591_gain = wetterdaten['weather']['TSL2591']['Gain']
TSL2591_timing = wetterdaten['weather']['TSL2591']['Timing']

# Umwandeln der Unix-Zeitstempel in Datetime-Objekt
sunrise_utc = datetime.fromtimestamp(sunrise, timezone.utc)
sunset_utc = datetime.fromtimestamp(sunset, timezone.utc)
datetime_utc = datetime.fromtimestamp(timestamp, timezone.utc)
utc_offset = timedelta(hours=2)
sunrise_utc2 = sunrise_utc.astimezone(timezone(utc_offset))
sunset_utc2 = sunset_utc.astimezone(timezone(utc_offset))
datetime_utc2 = datetime_utc.astimezone(timezone(utc_offset))
# Umwandeln in das gewünschte Zeitformat (z.B. 'YYYY-MM-DD HH:MM:SS')
sunrise_formatted = sunrise_utc2.strftime('%H:%M:%S')
sunset_formatted = sunset_utc2.strftime('%H:%M:%S')
datetime_formatted = datetime_utc2.strftime('%YYYY-%MM-%DD %H:%M:%S')

Ta = DHT_temp
Taupunkt = dewpoint
Windgeschw = windspeed
Luftdruck = pressure
Bewoelkung = clouds
Wetter = weather_desc
NDmenge = rain_1h
Regentropfen = RG11_count
Tamb = MLX90614_t_amb
Tir = MLX90614_t_obj
Helligkeit = TSL2591_lux
VISHelligkeit = TSL2591_visible
IRHelligkeit = TSL2591_ir

# Korrektur und Berechnung der Sky Quality
calFac = 5.7
SQM = calFac + (log((Helligkeit / 108000.0), 10) / -0.4)

# Wolkenbedeckung Konstanten anpassen!
K1 = 39.
K2 = 12.
K3 = 95.
K4 = 95.
K5 = 100.
K6 = 0.
K7 = 100.

if abs((K2 / 10 - Tamb)) < 1:
    T67 = sign(K6) * sign(Tamb - K2 / 10) * abs((K2 / 10 - Tamb))
else:
    T67 = K6 / 10 * sign(Tamb - K2 / 10) * (log10(abs((K2 / 10 - Tamb))) / log10(10) + K7 / 100)

Td = (K1 / 100) * (Tamb - K2 / 10) + (K3 / 100) * pow(exp(K4 / 1000 * Tamb), (K5 / 100)) + T67
Tsky = Tir - Td
Cldcov = 100 + ((Tsky / 8) * 100)

# Ausgabe
# print(format(Tsky, ".2f"), format(Cldcov, ".2f"), format(Ta, ".2f"), format(Tamb, ".2f"), format(Tir, ".2f"))

# CSV-Datei zum Schreiben öffnen
with open(dateiname2, mode='w', newline='') as datei:
    schreiber = csv.writer(datei)
    schreiber.writerow(["Sonnenaufgang: ", sunrise_formatted])
    schreiber.writerow(["Wetter: ", Wetter])
    schreiber.writerow(["Temp/C: ", temp])
    schreiber.writerow(["Druck/hPa: ", Luftdruck])
    schreiber.writerow(["TauPkt/C: ", Taupunkt])
    schreiber.writerow(["Bewoelkung/%: ", Bewoelkung])
    schreiber.writerow(["WindV/m/s: ", Windgeschw])
    schreiber.writerow(["SQM/mag/bs² :", format(SQM, ".1f")])
    schreiber.writerow(["Regen in 1h :", format(rain_1h)])
    schreiber.writerow(["NDmenge/mm/m²: ", NDmenge])
    schreiber.writerow(["Sonnenuntergang: ", sunset_formatted])
    schreiber.writerow(["Tropfen: ", Regentropfen])


#Ausgabe
# CSV-Datei zum Schreiben öffnen
with open(dateiname1, mode='a', newline='') as datei:
            schreiber = csv.writer(datei)
            schreiber.writerow([datetime_formatted,temp,Tamb, Tir,clouds])
            
# print('Alles fertig')