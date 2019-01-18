#!/usr/bin/python
import time

import pytest

from ..geocoder import geocoder


@pytest.mark.parametrize("city, expected", [
    ("pupax",0),
    ("Warsaw",9),
])
def test_query_results_city(city, expected):
	time.sleep(1)
	g = geocoder()
	num_results = g.getQueryResults(city)
	if num_results>= 0:
		assert num_results == expected
	else:
		assert num_results<0


@pytest.mark.parametrize("city, country, expected", [
    ("Sopot" ,"PL",1),
    ("Warsaw","PL",1),
])
def test_query_results_city_country(city, country, expected):
	time.sleep(1)
	g = geocoder()
	num_results = g.getQueryResults(city, country)
	if num_results>= 0:
		assert num_results == expected
	else:
		assert num_results<0


