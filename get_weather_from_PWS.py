#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
from time import *
import shutil
import requests,urllib,json,os.path

# Variablen anlegen:
key = "46cf957af9f541488f957af9f561488e" #API-Key bei Wunderground
ort = "Lauchhammer" #Ort der Abfrage
land = "Germany" #Land der Abfrage
wetterdatei = "/home/geo/PWS-Daten/wetterdatei" #Pfad zur Datendatei
backupordner = "/home/geo/PWS-Daten/Backup" #Ordner für Backup der Datendatei

# Ab hier muss nichts mehr verändert werden:
liste = [0,0,0,0,0,0,0,0,0,0]
degreeChar = u'\N{DEGREE SIGN}' #Gradzeichen erzeugen
fcast = []
# Aktuelles Datum und Uhrzeit
lt = localtime()
datum = strftime("%d.%m.%Y", lt)
zeit = strftime("%H:%M", lt)
# Pfad zur Backup-Datei erstellen:
timestamp = strftime("%Y_%m_%d", lt)

# Hier startet das Hauptprogramm:
print("Hole Daten von Wunderground...")

url = 'https://api.weather.com/v2/pws/observations/current?stationId=ILAUCH27&format=json&units=m&apiKey=46cf957af9f541488f957af9f561488e'
f = urllib.request.urlopen(url)
json_string = f.read()
parsed_json = json.loads(json_string)
parsed_json = parsed_json['observations'][0]
stationID = parsed_json['stationID']
obsTimeLocal= parsed_json['obsTimeLocal']
location = parsed_json['neighborhood']
humidity=parsed_json['humidity']
temp = parsed_json['metric']['temp']
windSpeed = parsed_json['metric']['windSpeed']
precipRate = parsed_json['metric']['precipRate']
if precipRate>0.01:
    meldung='Regen'
meldung ='kein Regen'
f.close()

# Wetterdaten in Liste schreiben:
liste[0] = obsTimeLocal #Zeit
liste[1] = temp #Aktuelle Temperatur
liste[2] = humidity #Luftfeuchtigkeit
liste[3] = windSpeed #Windgeschw.
liste[4] = precipRate #Regenmenge
liste[5] = meldung #regnet es?


# Zeile für Wetterdatei generieren:
line = (str(liste[0])+";"+str(liste[1])+";"+str(liste[2])+";"+str(liste[3])+ \
       ";"+str(liste[4])+";"+(liste[5]))

# Falls Wetterdatei noch nicht existiert, diese anlegen:
if not os.path.exists(wetterdatei):
    fout=open(wetterdatei,"w")
    fout.close()

# Backup Wetterdatei anlegen:
backupdatei=str(backupordner + '/' + timestamp + '_backup.cat')
if not os.path.exists(backupdatei): #Nur einmal am Tag Backup anlegen, falls Datei noch nicht existiert
    shutil.copyfile(wetterdatei,backupdatei)
    print("Backup erstellt in " + backupdatei)
else:
    print("Backup wurde heute schon einmal erstellt - Skipped")

# Zeile an Wetterdatei anhängen:
fout=open(wetterdatei,"a")
fout.writelines(line + '\n')
fout.close()
print(wetterdatei+" wurde ergänzt.")

# Programm wird beendet:
print("Die neue Zeile sieht so aus:\n" + line)
