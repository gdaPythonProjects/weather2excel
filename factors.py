#!/usr/bin/python
import csv

class WeatherFactors:
  def __init__(self,name,unit,type,min_val,max_val,alert_min_val,alert_max_val):
    self.name=str(name)
    self.unit=str(unit)
    self.type=str(type)
    self._min_val=self._convert_to_float(min_val)
    self._max_val=self._convert_to_float(max_val)
    self._alert_min_val=self._convert_to_float(alert_min_val)
    self._alert_max_val=self._convert_to_float(alert_max_val)


  def print(self):
    if self.type == "w":
      ftype = "weather"
    elif self.type == "p":
     ftype = "pollution"

    print(self.name+" ["+self.unit+"] - "+ftype)
 

  def check_limits(self,value):
    return self.check_upper_limit(value) and self.check_lowwer_limit(value)


  def check_upper_limit(self,value):
    if(self._max_val=="" or self._max_val is None):
      return True
    try:
      if value<=self._max_val:
        return True
      else:
        return False
    except:
      return False


  def check_lowwer_limit(self,value):
    if(self._min_val=="" or self._min_val is None):
      return True
    try:
      if value>=self._min_val:
        return True
      else:
        return False
    except:
      return False


  def check_alerts(self,value):
    try:
      if value<self._alert_min_val or value>self._alert_max_val:
        return True
      else:
       return False
    except:
      return False


  def _convert_to_float(self,value):
    try:
      return float(value)
    except:
      return None

############################################## END OD CLASS DEFINITION ############################################## 

def load_units_config():
  factorsDict={}
  try:
    with open("config/.units/units.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
          factorsDict[ row["par"].strip() ] = WeatherFactors(row["par"],row["unit"],row["type"],row["min_val"],row["max_val"],row["alert_min_val"],row["alert_max_val"])
    return factorsDict
  except:
    return False


def load_timezones():
  factorsDict={}
  try:
    with open("config/.units/timezones.csv", 'r', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
          factorsDict[ row["TZ"].strip() ] = row["UTC_offset"].strip() 
    return factorsDict
  except:
    return False


def list_factors_unis(factorsDict):
  for key, value in factorsDict.items():
    if(factorsDict[key].type=="w" or factorsDict[key].type=="p"):
      factorsDict[key].print()


#w-weather, p-pollution, wf-weather forecast, t-obseration time,  tf-time of forecast, tz- time zone
def get_factors(factorsDict):
  f = []
  for key,value in factorsDict.items():
    if (factorsDict[key].type == "w" or factorsDict[key].type == "p" or factorsDict[key].type == "wf" or factorsDict[key].type == "tf" or factorsDict[key].type == "t" or factorsDict[key].type == "tz"):
      f.append(key)
  return f




