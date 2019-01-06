#!/usr/bin/python
import re
import csv
import requests
from jsonpath_ng import jsonpath#, parse
from jsonpath_ng.ext import parse
from factors import *
import json # only for development
from unit_converter.converter import convert, converts
import time
import datetime as dt
import dateutil.parser
from datetime import timedelta

API_PATH ="config/API/"
API_KEY_PATH ="config/API_keys/"
TIME_ZONES = {}


#load units configuration
factorsDict=load_units_config()
#list_factors_unis(factorsDict)
factors = get_factors(factorsDict)
#TIME_ZONES = load_timezones()

# API returning name of time zones


class WeatherApis:

  TZ_API = ["APIXU","DarkSky"]
  TZ=""

  def __init__(self):
    self.url_search=""
    self.api_token=""
    self.correct=1
    self.JSON=""
    self.config={}


  def print_config(self):
    print(self.config)


  def read_conf(self,file):
    try:
      with open(API_PATH+file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
          par = row["par"].strip()
          val = row["val"].strip()
          unit = row["unit"].strip()
          self.config[ par ] = val
          if factorsDict[par].type!="":
            self.config[ par+"_u" ] = unit
    except EnvironmentError:
      print("*!!* Brak pliku konfiguracyjnego: "+file)
      return False    #self.config["filename"] = file
    
    self.api_token = self._read_api_token(file)#print(self.api_token)    except:
    if self.api_token == False:
      print("*!!* W folderze config/API_keys/ brak pliku z kluczem(tokenem) dla API: "+self.config[ "api_name"]  )
      return False
    
    return True


  def get_weather(self, *args):  # MODE-0, LANG-1, DAYS-2, city-3     MODE-0, LANG-1, DAYS-2,lon-3, lat-4
    if len(args) == 4:# building url with city
      self.url_search = self.config["url_"+args[0]+"_city_endpoint"].replace("{city}", args[3])
      if len(self.url_search)<10:
        return self.get_weather(args[0],args[1],args[2],str(54.51889),str(18.53188)) #TODO #getLONLATfromCity
    elif len(args) == 5:# building url with lon/lat
      self.url_search = self.config["url_"+args[0]+"_lonlat_endpoint"].replace("{lat}", str(args[4])).replace("{lon}", str(args[3]))
    else:
      return False  #print( "REPL:    "+self._replacer(self.url_search, {"{token}":self.api_token,"{lang}":args[1]} )  )
    
    self.url_search = self._replacer(self.url_search, {"{token}":self.api_token, "{lang}":args[1], "{days}":str(args[2]) })

    print("URL_SEARCH: "+self.url_search)
    headers = self._set_headers(args[0])  #print("headers: "+str(headers))
    try:
      if self.config["method_"+args[0]] == "get":#print("GET REQUEST......")
        r = requests.get(self.url_search,headers=headers)
      else: #POST
        data = self._replacer(self.config["post_data_"+args[0]], {"{lon}":args[3], "{lat}":args[4] })   #print("POST DATA: "+data)
        r = requests.post(self.url_search, headers=headers, data = data )

      self.JSON = r.json()#print(self.JSON)
      self._write_JSON_resp_to_file()
      print("STATUS CODE:"+str(r.status_code))
      if r.status_code == 200 and self._check_result():
        return True
    except:
      raise
      return False

  def _set_headers(self,mode):
    R={}
    headers = self.config["header_request_"+mode]
    if headers!="":
      h = headers.split(';')
      for idx, val in enumerate(h):
        kv = val.split(":")
        kv[1] = kv[1].replace("{token}", self.api_token) 
        R[kv[0]] = kv[1]
    return R


  def _replacer(self, input_string, replace):
    for key,val in replace.items():
      input_string = input_string.replace(key, str(val))    #print(key, '->', val)
    return input_string

  def _check_result(self): #print("ok_value=") print(self.config["ok_key"])#print("ok_JSON")print(self.JSON[ self.config["ok_key"]  ])
    if self.config["ok_key"]=="":
      return True
    
    try:
      if self.config["ok_value"] == "<exist>" and self.JSON[ self.config["ok_key"]  ]!="":
        return True
      elif  str(self.JSON[ self.config["ok_key"]  ]) == str(self.config["ok_value"]) :
        return True
    except:
      print("*** W odpowiedzi z serwera brak wymaganego pola: '"+self.config["ok_key"]+"'" )
      raise
      return False


  def parse_result(self, mode, days):
    DATA = {}
    #global TZ,TZ_API
    DATA["api_name"]=self.config["api_name"]
    for day_number in range(0,days):
      WDS = {}
      WDS["api_name"]=self.config["api_name"]
      for f in factors:
        if f in self.config and self.config[f]!="":#print(self.config[f])
          WDS[f] = "#"   # no information defined in config file
          if mode=="current":
            json_path = self.config[f]
          else:
            if self.config["forecast_root"]!="":
              json_path = self.config["forecast_root"]+".["+str(day_number)+"]."+self.config[f]
            else:
              if "@" in self.config[f]:
                json_path = self.config[f].replace("nnn",str(day_number))
              else:
                json_path = "["+str(day_number)+"]."+self.config[f]
          
          #print("JSON_PATH: "+json_path)

          try:
            x = parse(json_path).find(self.JSON)   
            #print(x)
            for match in x:
              #print("JSON_PATH: "+json_path+"  val:"+str(match.value) )
              if str(factorsDict[f].unit) == str(self.config[f+"_u"]): 
                WDS[f] = match.value
              else:
                if self.config[f+"_u"]!="": #print(" f:"+self.config[f]+" u:"+self.config[f+"_u"]+" UNIT:"+factorsDict[f].unit+"   build_str:"+str(match.value)+" "+self.config[f+"_u"])
                  number_string = str(match.value)+" "+self.config[f+"_u"]
                  number_string = re.sub(r'/(.){1,3}', '*\g<1>^-1', number_string)
                  unit_to = re.sub(r'/(.){1,3}', '*\g<1>^-1', factorsDict[f].unit) #print("conversion: number_string: "+number_string+"  unitto:"+unit_to)
                  WDS[f] = round( float( converts(number_string, unit_to)),2 ) #"_"+str(match.value)#str("_"+match.value)#TODO convert values
                else:
                  if str(factorsDict[f].unit)=='%':
                    WDS[f] = 100*match.value
                  else:
                    WDS[f] = "_"
              if(WDS[f] != "_" and not factorsDict[f].check_lowwer_limit(WDS[f])):
                WDS[f]="<"
              if(WDS[f] != "_" and not factorsDict[f].check_upper_limit(WDS[f])):
                WDS[f]=">"

          except (KeyError, AttributeError, NameError) as e:
              print("* Problem KeyError with field: "+f+" in "+self.config["api_name"])#("+e.errno+": "+e.strerror+")"
              WDS[f] = "_"
              #raise
          except:
              WDS[f] = "__"
              print("** Problem with field: "+f+" in "+self.config["api_name"])
              #raise
        else:
          WDS[f] = "*";# no information found

      if WeatherApis.TZ =="" and self.config["api_name"] in WeatherApis.TZ_API: 
        WeatherApis.TZ = self._get_timezone_offset( WDS["timezone"] )
      
      #convert time to DD/MM/YYY HH:MM 
      WDS["timestamp"] = self._convert_datetime_to_human(WDS["timestamp"],WeatherApis.TZ)
      WDS["timestamp-forecast"] = self._convert_datetime_to_human(WDS["timestamp-forecast"],WeatherApis.TZ)
      
      
      DATA[day_number] = WDS
      if(mode == "current"):
        break
    return DATA


  def _read_api_token(self,file):
    file_key = file.replace(".csv",".key")
    try:
      with open(API_KEY_PATH+file_key, 'r') as keyfile:
        key = keyfile.read().replace('\n', '').replace('\r\n', '')
      return key
    except:
      #raise
      return False


  def _check_api_key(self):
    self.get_weather("current","en",1,0,0)
    return self._check_result()

  def _get_timezone_offset(self, timezone):
    global TIME_ZONES
    try:
      return TIME_ZONES[ timezone ]
    except KeyError:
      return ""
      


  def print_api_verification(self):
    if self._check_api_key() == True:
      result = "OK"
    else: 
      result = "BAD CONFIGURATION"
    print(self.config["api_name"]+": "+result)


  def is_correct(self):#check if object is complete //TODO
    self.correct = 1

  ### helper method to write JSON from API response to file
  def _write_JSON_resp_to_file(self):
      with open(self.config["api_name"]+'.json', 'w') as outfile:
          json.dump(self.JSON, outfile)
  
  def _convert_datetime_to_human(self,time,tz):    #print("TIME======"+str(time) + "   TZ="+str(tz))
      t_str=""
      H = M = 0
      try:
        arrHM = str(tz).split(":")
        if len(arrHM) == 2:
          H = int(arrHM[0])
          M = int(arrHM[1])
      except ValueError:
        print("--> Time zone parsing problem...")

      isEpoch = re.search("\d{10,}", str(time))
      if isEpoch:
        try:
          t = dt.datetime.utcfromtimestamp(time) + timedelta(seconds=0, minutes=M, hours=H)
          t_str = t.strftime("%Y/%m/%d %H:%M")
        except:
          print("--> Adding timezone to time problem")
        return t_str

      isISO8601 = re.search("^\d{4}-\d{2}-\d{2}T", time)
      if isISO8601:
        try:
          t = dateutil.parser.parse(time) + timedelta(seconds=0, minutes=M, hours=H)
          t_str = t.strftime("%Y/%m/%d %H:%M")
        except:
          print("--> Adding timezone to time problem")
        return t_str

      return "#"+str(time)
  
  #def setApiToken(token)
  #def santizizeSearch
  #def getLONLATfromCity
  #def checkToken