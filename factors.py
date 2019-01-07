#!/usr/bin/python
import csv

class WeatherFactors:
  def __init__(self,name,unit,type,min_val,max_val,alert_min_val,alert_max_val):
    self.name=name
    self.unit=unit
    self.type=type
    self._min_val=self._convert_to_float(min_val)
    self._max_val=self._convert_to_float(max_val)
    self._alert_min_val=self._convert_to_float(alert_min_val)
    self._alert_min_val=self._convert_to_float(alert_max_val)

  def print(self):
    if self.type == "w":
      ftype = "weather"
    elif self.type == "p":
     ftype = "pollution"

    print(self.name+" ["+self.unit+"] - "+ftype)
  
  def check_limits(self,value):
    return check_upper_limit(value) and check_lowwer_limit()

  def check_upper_limit(self,value):
    if self._max_val!=None and value>self._max_val:
      return False
    else:
     return True

  def check_lowwer_limit(self,value):
    if self._min_val!=None and value<self._min_val:
      return False
    else:
     return True

  def check_alerts(value):
    if value>=self._alert_min_val and value <=self._alert_min_val:
      return True
    else:
     return False

  def _convert_to_float(self,value):
    try:
      return float(value)
    except (ValueError) as e:
      return None


def load_units_config():
  factorsDict={}
  with open("config/.units/units.csv", 'r') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
      for row in reader:
        factorsDict[ row["par"].strip() ] = WeatherFactors(row["par"],row["unit"],row["type"],row["min_val"],row["max_val"],row["alert_min_val"],row["alert_max_val"])
  return factorsDict

def load_timezones():
  factorsDict={}
  with open("config/.units/timezones.csv", 'r', encoding="utf8") as csvfile:
      reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
      for row in reader:
        factorsDict[ row["TZ"].strip() ] = row["UTC_offset"].strip() 
  return factorsDict

def list_factors_unis(factorsDict):
  for key, value in factorsDict.items():
    if(factorsDict[key].type=="w" or factorsDict[key].type=="p"):
      factorsDict[key].print()

def get_factors(factorsDict):
  f = []
  for key,value in factorsDict.items():
    if(factorsDict[key].type=="w" or factorsDict[key].type=="p" or factorsDict[key].type=="wf" or factorsDict[key].type=="t" or factorsDict[key].type=="tz"):
      f.append(key)
  return f




