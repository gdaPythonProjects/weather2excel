#from ..factors import *
from ..weatherApis import WeatherApis

import pytest

APIS = ["APIXU.csv", "OpenWeather.csv", "WAQI.csv", "Weatherbit.csv", "DarkSky.csv", "Climacell.csv","Airly.csv","Airvisual.csv"]

def test_configuration_exists():
    R = 0
    for API in APIS:
        if API.endswith(".csv"):
            wa = WeatherApis()
            if wa.read_conf(API) == False:
                R=R+1

    assert R == 0