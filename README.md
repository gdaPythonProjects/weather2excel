# weather2excel
W celu wykorzystnia aplikacji należy zarejestorwać się w co najmniej jednym z serwisów:
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
  <td></a></td>
 </tr>
 </table>
 1. https://www.apixu.com
 2. https://darksky.net
 3. https://www.weatherbit.io
 4. https://openweathermap.org
 5. http://aqicn.org
 6. https://www.climacell.co
 7. https://airly.eu

Klucz/token do korzystania z danego API powinien zostać zapisany w odpowiednim pliku w /config/API_keys/ w postaci: nazwa_portalu.key

# Zależności:
> pip3 install unit-converter\
> pip3 install --upgrade jsonpath-ng\
> pip3 install requests

# Uruchomienie
> python3 weather2excel.py

Wyjaśnienie symboli w wynikach:\
<span> <b>*</b>  API nie oferuje danych</span>\
<span> <b>#</b>  dane chwilowo niedostępne</span>\
<span> <b>_</b>  problem z konwersją danych</span>\
<span> <b><</b>  wartość poniżej dopuszczalnego przedziału</span>\
<span> <b>></b>  wartość powyżej dopuszczalnego przedziału</span>
