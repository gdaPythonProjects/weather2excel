#!/usr/bin/python
import pytest


from ..weatherApis import WeatherApis


APIS = ["APIXU.csv", "OpenWeather.csv", "WAQI.csv", "Weatherbit.csv", "DarkSky.csv", "Climacell.csv","Airly.csv","Airvisual.csv"]


def test_configuration_exists():
    R = 0
    for API in APIS:
        if API.endswith(".csv"):
            wa = WeatherApis()
            if wa.read_conf(API) == False:
                R=R+1

    assert R == 0


@pytest.mark.parametrize("input_string, replace, expected", [
    ("{a}",{"{a}":"1"},"1"),
    ("{c},{a},{b}",{"{a}":"aaa","{b}":"bbb","{c}":"ccc"},"ccc,aaa,bbb"),
    ("",{"{a}":"343535,12323"},""),
    (None,{"{a}":"343535,12323"},None),
])
def test_replacer(input_string, replace, expected):
	wa = WeatherApis()
	result = wa._replacer(input_string, replace)
	assert result == expected


@pytest.mark.parametrize("time, tz, expected", [
    ("2019-01-12T15:19:21","-11:00","2019/01/12 04:19"),
    ("2019-01-12T22:19:21","04:00","2019/01/13 02:19"),
    ("2019-01-12T15:19:21","","2019/01/12 15:19"),
    (1547327892,"00:00","2019/01/12 21:18"),
    (1547327892,"-03:00","2019/01/12 18:18"),
    (1547327892,"+05:00","2019/01/13 02:18"),
    ("","-03:00","#"),
    ("2019.01.12 15:19","01:00","#2019.01.12 15:19"),
])
def test_convert_datetime_to_human(time,tz,expected):
	wa = WeatherApis()
	result = wa._convert_datetime_to_human(time,tz)
	assert result == expected
