#!/usr/bin/python
import csv
import sys
EPSILON = sys.float_info.epsilon 
colors = {
  "rgb": [(0, 0, 255), (0, 255, 0), (255, 0, 0)],
  "rg" : [(255, 0, 0), (127, 127 , 0),(0, 255, 0) ],
  "gr" : [(0, 255, 0), (127, 127 , 0), (255, 0, 0)]
} 
class WeatherFactors:
  

  def __init__(self,name,unit,type,min_val,max_val,alert_min_val,alert_max_val,color_scale):
    self.name=str(name)
    self.unit=str(unit)
    self.type=str(type)
    self._min_val=self._convert_to_float(min_val)
    self._max_val=self._convert_to_float(max_val)
    self._alert_min_val=self._convert_to_float(alert_min_val)
    self._alert_max_val=self._convert_to_float(alert_max_val)
    if color_scale in colors:
      self.color_scale=color_scale
    else:
      self.color_scale="rgb"


  def print(self):
    if self.type == "w":
      ftype = "weather"
    elif self.type == "p":
     ftype = "pollution"

    print(self.name+" ["+self.unit+"] - "+ftype)
 

  def convert_to_rgb(self,val): #code from https://stackoverflow.com/a/20793850
    if(self._alert_max_val is None or self._alert_min_val is None):
      return "FFFFFF"
    
    if(val>self._alert_max_val):
      val = self._alert_max_val
    if(val<self._alert_min_val):
      val = self._alert_min_val
    # "colors" is a series of RGB colors delineating a series of
    # adjacent linear color gradients between each pair.
    # Determine where the given value falls proportionality within
    # the range from minval->maxval and scale that fractional value
    # by the total number in the "colors" pallette.
    try:
      i_f = float(val-self._alert_min_val) / float(self._alert_max_val-self._alert_min_val) * (len(colors)-1)
    except:
      #print("RGB PROBLEM"+self.name)
      return "FFFFFF"
    # Determine the lower index of the pair of color indices this
    # value corresponds and its fractional distance between the lower
    # and the upper colors.
    i, f = int(i_f // 1), i_f % 1  # Split into whole & fractional parts.
    # Does it fall exactly on one of the color points?
    if f < EPSILON:
        return self.rgb2hex(colors[self.color_scale][i][0], colors[self.color_scale][i][1], colors[self.color_scale][i][2])
    else:  # Otherwise return a color within the range between them.
        (r1, g1, b1), (r2, g2, b2) = colors[self.color_scale][i], colors[self.color_scale][i+1]
        #return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))
        return self.rgb2hex(int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1)) )


  def rgb2hex(self,r,g,b):
    return "{:02x}{:02x}{:02x}".format(r,g,b)


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
    with open("config/.units/units.csv", 'r', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
          factorsDict[ row["par"].strip() ] = WeatherFactors(row["par"],row["unit"],row["type"],row["min_val"],row["max_val"],row["alert_min_val"],row["alert_max_val"],row["color_scale"])
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