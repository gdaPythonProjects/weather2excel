# weather2excel [![Build Status](https://travis-ci.org/gdaPythonProjects/weather2excel.svg?branch=master)](https://travis-ci.org/gdaPythonProjects/weather2excel)
W celu wykorzystnia aplikacji należy zarejestorwać się w co najmniej jednym z <b>8 serwisów</b>:
<table>
 <tr>
  <td><a href='https://www.apixu.com' target='_blank'><img src='logo/apixu.png'></a></td>
  <td><a href='https://darksky.net' target='_blank'><img src='logo/darksky.png'></a></td>
  <td><a href='https://www.weatherbit.io' target='_blank'><img src='logo/weatherbit.png'></a></td>
  <td><a href='https://openweathermap.org' target='_blank'><img src='logo/openweathermap.png'></a></td>
 </tr>
 <tr>
  <td><a href='http://aqicn.org' target='_blank'><img src='logo/waqi.jpeg'></a></td>
  <td><a href='https://www.climacell.co' target='_blank'><img src='logo/climacell.png'></a></td>
  <td><a href='https://airly.eu' target='_blank'><img src='logo/airly.jpg'></a></td>
  <td><a href='https://www.airvisual.com' target='_blank'><img src='logo/airvisual.png'></a></td>
 </tr>
 </table>

<br>
<b>Aplikacja nie korzysta z gotowych modułów Python do API pogodowych.</b>
Dodawanie nowego serwisu odbywa się przez stworzenie nowego pliku konfiguracyjnego .csv w katalogu config/API/. Aplikacja jest w stanie połączyć się z serwisami udostępniającymi dane pogodowe i środowiskowe w formacie JSON za pomocą metod POST lub GET (w tym poprzez przesyłanie danych w nagłówkach HTTP). 
<br>Tabela przedstawiająca ogólne możliwe do wykorzystania funkcjonalności Weather API<br>
<img src='logo/tabela_api.png'>

Geokodowanie i odwrotne geokodowanie odbywa się przy użyciu **Nominatim** API korzystającego z danych:<br>
<a href='https://www.openstreetmap.org' target='_blank'><img src='logo/OpenStreetMap_logo.jpg' width='126' height='90'></a>
<br>

# Konfiguracja
Klucz/token do korzystania z danego API powinien zostać dopisany w odpowiednim pliku w katalogu <b>config/API_keys/</b>.<br>
Prognozy i bieżące wyniki będą podawane w czasie UTC. Aby uzyskać je w <b><i>czasie lokalnym</i></b> dla wyszukiwanych miejsc, należy skonfigurować co najmniej jednen z serwisów: <b>APIXU</b>, <b>DarkSky</b>.

# Zależności:
    pip install requests
    pip install unit-converter
    pip install python-dateutil
    pip install --upgrade jsonpath-ng
    pip install openpyxl
# Uruchomienie i sposób użycia:
    python weather2excel.py                 #wybór paramentrów przez interaktywne menu
    python weather2excel.py --mode=current  --city="Gdynia" --lang=pl  #aktualna pogoda w Gdynia z opisem w języku polskim
    python weather2excel.py --mode=forecast --city="Gdynia" --days=5   #prognoza pogody dla Gdyni na 5 dni
    python weather2excel.py --mode=current  --lon=19.23 --lat=54.23    #aktulna pogoda dla współrzędnych dł.geog. 19.23 i szer. geogr. 54.23 
    python weather2excel.py --mode=forecast --lon=19.23 --lat=54.23    #prognoza pogody dla współrzędnych dł.geog. 19.23 i szer. geogr. 54.23 

# Wyniki
Przykładowe pliki wynikowe zostaną umieszczone w folderze examples.

<b>Jednostki fizyczne wielkości przedstawiono poniżej:</b> (aplikacja automatycznie konwertuje do podanych jednostek)\
pressure [hPa] - weather\
humidity [%] - weather\
temperature [°C] - weather\
apparent-temperature [°C] - weather\
dew-point [°C] - weather\
clouds [%] - weather\
wind-speed [m/s] - weather\
wind-direction [°] - weather\
precip-intensity [mm/h] - weather\
precip-accumulation [mm] - weather\
visibility [km] - weather\
uv [] - weather\
so2 [ppm] - pollution\
no2 [ppm] - pollution\
co [ppm] - pollution\
o3 [ppm] - pollution\
pm25 [ppm] - pollution\
pm10 [ppm] - pollution\
pm1 [ppm] - pollution\

<b>Wyjaśnienie symboli pojawiających się w wynikach w plikach .csv lub .xls:</b>\
<span> <b>*</b>&nbsp;  API nie oferuje danych</span>\
<span> <b>#</b>&nbsp;  dane chwilowo niedostępne</span>\
<span> <b>_</b>&nbsp; problem z konwersją danych</span>\
<span> <b><</b>&nbsp;  wartość poniżej dopuszczalnego przedziału</span>\
<span> <b>></b>&nbsp;  wartość powyżej dopuszczalnego przedziału</span>
