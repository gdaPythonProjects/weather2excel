#!/usr/bin/python
from ..factors import *
import pytest

@pytest.mark.parametrize("name,unit,type,min_val,max_val,alert_min_val,alert_max_val", [
    ("Temperatura","C","w",-273,100,-10,30),
    ("Temperatura","C",0,-273,100,-10,30),
    ("Temperatura","C",0,-273,100,-10,"silly_value"),
    ("","C",0,-273,100,-10,"silly_value"),
    (None,"C",0,-273,None,False,"silly_value"),
])
def test_create_object_weatherFactors(name,unit,type,min_val,max_val,alert_min_val,alert_max_val):
    try:
        T = WeatherFactors(name,unit,type,min_val,max_val,alert_min_val,alert_max_val)
    except:
        pytest.fail("Unexpected weatherFactorsError...")


#factors.check_limits() test
@pytest.mark.parametrize("temperature_limit,expected", [
    (-300,False),
    (0,True),
    (2000,False),
    (None,False),
])
def test_factor_limits(temperature_limit,expected):
	T = WeatherFactors("Temperatura","C","w",-273.15,1000,-10,30)
	assert T.check_limits(temperature_limit) == expected


#factors.check_alerts() test
@pytest.mark.parametrize("temperature_alert,expected", [
    (-12,True),
    (-10.1,True),
    (-10,False),
    (0,False),
    (30,False),
    (30.01,True),
    (33,True),
    (None,False),
])
def test_check_alerts(temperature_alert,expected):
	T = WeatherFactors("Temperatura","C","w",-273,100,-10,30)
	assert T.check_alerts(temperature_alert) == expected


#factors._convert_to_float() test
@pytest.mark.parametrize("float_value,expected", [
    (-12,-12),
    (0,0),
    ("",None),
    (None,None),
    (-30,-30),
])
def test__convert_to_float(float_value,expected):
	T = WeatherFactors("Temperatura","C","w",-273,100,-10,30)
	assert T._convert_to_float(float_value) == expected


def test_load_units_config():
    result = load_units_config()
    assert result != False


def test_load_timezones():
    result = load_timezones()
    assert result != False
    #T = ("Temperatura","C","w",-273,100,-10,30)


