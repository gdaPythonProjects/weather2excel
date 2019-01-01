#!/usr/bin/python
import re
import csv
import requests
from jsonpath_ng import jsonpath, parse
from factors import *
from unit_converter.converter import convert, converts

API_PATH ="config/API/"
API_KEY_PATH ="config/API_keys/"
#load units configuration

factorsDict=load_units_config()
list_factors_unis(factorsDict)
factors = get_factors(factorsDict)

class WeatherApis:
  def __init__(self):
    self.url_search=""
    self.api_token=""
    self.correct=1
    self.JSON=""
    self.config={}

  def print_config(self):
    print(self.config)

  def read_conf(self,file):
    with open(API_PATH+file, 'r') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
      for row in reader:
        par = row["par"].strip()
        val = row["val"].strip()
        unit = row["unit"].strip()
        self.config[ par ] = val
        self.config[ par+"_u" ] = unit

    self.config["filename"] = file
    self.api_token = self._read_api_token(file)
    #print(self.api_token)

  def get_weather(self, *args):
    if   len(args) == 1:# building url with city
      self.url_search = self.config["url_current_city_endpoint"].replace("{city}", args[0])
      if len(self.url_search)<10:
        return self.get_weather(str(18.53188),str(54.51889))#TODO #getLONLATfromCity
    elif len(args) == 2:# building url with lon/lat
      self.url_search = self.config["url_current_lonlat_endpoint"].replace("{lon}", args[0])
      self.url_search = self.url_search.replace("{lat}", args[1])#print(r.status_code)#print(r.headers) #print(r.content) #print(r.json())    #print(self.url_search_city)
    else:
      return False
    
    self.url_search = self.url_search.replace("{token}", self.api_token) #print("URL= "+self.url_search)
    r = requests.get(self.url_search)
    self.JSON = r.json()
    if r.status_code == 200 and self._check_result():
      return True

  def _check_result(self): #print("ok_value=")print(self.config["ok_value"])print("ok_JSON")print(self.JSON[ self.config["ok_key"]  ])
    if( str(self.JSON[ self.config["ok_key"]  ]) == str(self.config["ok_value"]) ):
      return True
    elif self.config["ok_value"] == "<exist>" and self.JSON[ self.config["ok_key"]  ]!=None:
      return True

  def parse_result(self):
    WDS = {}
    WDS["api_name"]=self.config["api_name"]
    for f in factors:
      if f in self.config and self.config[f]!="":#print(self.config[f])
        WDS[f] = "#"   # no information defined in config file
        try:
          x = parse(self.config[f]).find(self.JSON)
          
          for match in x:
            if str(factorsDict[f].unit) == str(self.config[f+"_u"]): 
              WDS[f] = match.value
            else:
              if self.config[f+"_u"]!="":   #print(" f:"+self.config[f]+" u:"+self.config[f+"_u"]+" UNIT:"+factorsDict[f].unit+"   build_str:"+str(match.value)+" "+self.config[f+"_u"])
                number_string = str(match.value)+" "+self.config[f+"_u"]
                number_string = re.sub(r'/(.){1,3}', '*\g<1>^-1', number_string)
                unit_to = re.sub(r'/(.){1,3}', '*\g<1>^-1', factorsDict[f].unit) #print("conversion: number_string: "+number_string+"  unitto:"+unit_to)
                WDS[f] = round( float( converts(number_string, unit_to)),2 )#"_"+str(match.value)#str("_"+match.value)#TODO convert values
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
            WDS[f] = "_"
            print("** Problem with field: "+f+" in "+self.config["api_name"])
            #raise
      else:
        WDS[f] = "*";# no information found

    return WDS

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
    self.get_weather("Gdynia")
    return self._check_result()

  def print_api_verification(self):
    if self._check_api_key() == True:
      result = "OK"
    else: 
      result = "BAD CONFIGURATION"
    print(self.config["api_name"]+": "+result)

  def is_correct(self):#check if object is complete //TODO
    self.correct = 1

  #def setApiToken(token)
  #def santizizeSearch
  #def getLONLATfromCity
  #def checkToken