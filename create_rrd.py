#!/usr/bin/python3 
# -*- coding: utf-8 -*-

# Module laden
import requests
# import json wird nicht verwendet
import rrdtool

''' Struktur des importierten Datensatze
0stationID,ILAUCH27		1obsTimeUtc,2023-07-16T13:01:52Z		2timeStamp,2023-07-16 15:01:52	3neighborhood,Lauchhammer
4softwareType,EasyWeatherV1.5.7	5country,DE	6solarRadiation,567.4	7lon,13.73	8realtimeFrequency,	9epoch,1689512512
10lat,51.479	11uv,5.0	12winddir,247	13humidity,40	14qcStatus,1	15AmbientTemp,29	16heatIndex,29	17Taupunkt,14	18windChill,29
19windSpeed,6	20windGust,7	21pressure,1010.13	22precipRate,0.0	23precipTotal,3.0	24elev,29	25init,True	26mode,drop detect
27dropCount,2960	28dropFreq,0	29init,True	30T_amb,48.29000092	31T_obj,33.64998627	32init,True	33Lux,8928.601563	34Visible,16233	35IR,7804
36Gain,0	37Timing,1
'''

#create rrdtool database with all necessary data fields, Pfad zur DB angeben

rrdtool.create(
	"weather_StFP.rrd", # Station Far Point = StFP
    "--step", "180",  # Datenpunkte alle 3 Minuten
    "DS:timeStamp:GAUGE:300::", # 2 Zeitstempel der Messung
	"DS:solarRadiation:GAUGE:300:0:1000", # 6 Sonnen-Strahlung
	"DS:epoch:GAUGE:300::",  # 9 Unix-Epoche - Zeit absolut seit ??
    "DS:UVIndex:GAUGE:300:0:10",  # 11 UV-Index
	"DS:WindRichtung:GAUGE:300:0:360",  # 12 Windrichtung 
	"DS:LFeuchte:GAUGE:300:0:100",  # 13 Luftfeuchtigkeit
	"DS:AussenTemp:GAUGE:300:-40:+50",  # 15 Außentemperatur
	"DS:Taupunkt:GAUGE:300:-40:+40",  # 17 Taupunkt
	"DS:Windgeschw:GAUGE:300:0:100",  # 19 Windgeschwindigkeit
	"DS:Boeen:GAUGE:300:0:180",  # 20 Windboeenstärke
	"DS:Luftdruck:GAUGE:300:900:1300",  # 21 Luftdruck
	"DS:NDrate:GAUGE:300:0:1000",  # 22 ND pro Stunde
	"DS:NDmenge:GAUGE:300:0:100",  # 23 ND pro Quadratmeter
	"DS:Regentropfen:GAUGE:300:0:10000",  # 27 Anzahle der Regentropfen
	"DS:RegenFrequenz:GAUGE:300:0:1000",  # 28 Tropfen pro Minute
	"DS:WolkenUmgTemp:GAUGE:300:-30:+40",  # 30 UmgebungsTemp
	"DS:Wolkentemp:GAUGE:300:-30:+40",  # 31 ObjektTemp
	"DS:Helligkeit:GAUGE:300:0:20000",  # 33 Helligkeit in LUX
	"DS:VISHelligkeit:GAUGE:300:0:20000",  # 34 VIS Helligkeit
	"DS:IRHelligkeit:GAUGE:300:0:20000",  # 35 IR-Helligkeit
    "RRA:AVERAGE:0.5:1m:6h",  # Durchschnittswerte für 6h (3 Minuten pro Datenpunkt)
    "RRA:AVERAGE:0.5:5m:1d",  # Durchschnittswerte für 1 Tag (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:15m:7d",  # Durchschnittswerte für 7 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:1h:30d",  # Durchschnittswerte für 30 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:1h:60d",  # Durchschnittswerte für 60 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:1h:90d",  # Durchschnittswerte für 90 Tage (1 Stunde pro Datenpunkt)
    "RRA:AVERAGE:0.5:1h:1y",  # Durchschnittswerte für 1 Jahr (1 h pro Datenpunkt)
    "RRA:AVERAGE:0.5:1d:10y"  # Durchschnittswerte für 1 Jahr (1 d pro Datenpunkt)
)
