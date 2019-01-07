# plik w którym znajdują się elementy na których można testować działanie API pogodowych

#!/usr/bin/python

from weatherApis import *
# from Factors import *
import csv
import json # only for development
import os

CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 18.5318800  # długość geograficzna
LAT = 54.5188900  # szerokość geograficzna
MODE = "current"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 3  # ilość dni do przodu na które można uzyskać prognoze pogody

weatherDataset = []

# TODO for loop all  .csv files from /config// directory
APIS = ["APIXU.csv", "OpenWeather.csv", "WAQI.csv", "Weatherbit.csv", "DarkSky.csv", "Climacell.csv","Airly.csv","Airvisual.csv"]


#APIS = ["APIXU.csv"]


"""for API in os.listdir("config/API/"):"""
for API in APIS:
  if API.endswith(".csv"):
    wa = WeatherApis()
    if wa.read_conf(API) == False:
      continue
    if wa.get_weather(MODE, LANG, DAYS, LON,LAT):
      weatherDataset.append( wa.parse_result(MODE, DAYS) )
    else:
      print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search)

CSV="api_name,"
for f in factors:
    CSV = CSV +f+","
    CSV=CSV+"\r\n"

for wynikiAPI in weatherDataset:
    for dzien in wynikiAPI:
        if(dzien!="api_name"):#print("-----    Wyniki/prognoza z "+wynikiAPI["api_name"]+"  DLA DNIA NUMER: "+str(dzien))
            for prognoza in wynikiAPI[dzien]:
                CSV = CSV + "\"" + str(wynikiAPI[dzien][prognoza]) + "\","
                CSV=CSV+"\r\n"

f = open( 'wyniki.csv', 'w' )
f.write( CSV )
f.close()


with open('data.json', 'w') as outfile:
    for WD in weatherDataset:
        json.dump(WD, outfile)
        #print(json.dumps(WD, sort_keys=False, indent=4))

