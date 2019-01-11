from factors import *
import pytest
'''
@pytest.mark.parametrize("name,unit,type,min_val,max_val,alert_min_val,alert_max_val,expected", [
    ("Temperatura","C","w",-273,100,-10,30)
])
'''

@pytest.mark.parametrize("temperature_limit,expected", [
    (-300,False),
    (0,True),
    (2000,False),
])
def test_factor_limits(temperature_limit,expected):
	T = WeatherFactors("Temperatura","C","w",-273.15,1000,-10,30)
	assert T.check_limits(temperature_limit) == expected


@pytest.mark.parametrize("temperature_alert,expected", [
    (-12,True),
    (-10.1,True),
    (-10,False),
    (0,False),
    (30,False),
    (30.01,True),
    (33,True),
])
def test_factor_alerts(temperature_alert,expected):
	T = WeatherFactors("Temperatura","C","w",-273,100,-10,30)
	assert T.check_alerts(temperature_alert) == expected
