import json
import remoteAPI

import datetime

def forecast(
        latitude,
        longitude,
        count,
        units="metric",  # api default = "standard"(Fahrenheit)
        mode="json",
        language="kr"
):
    parameters = {
        "lat": latitude,
        "lon": longitude,
        "cnt": count,
        "units": units,
        "mode": mode,
        "lang": language
    }
    response = remoteAPI.getRequest("/forecast", parameters)
    jsonResponse = json.loads(response.text)
    weathers = weathersForDay(jsonResponse["list"])
    print(json.dumps(weathers, indent=4))

def weathersForDay(weatherList):
    weathers = {}
    for weather in weatherList:
        unixDatetime = weather["dt"]
        date = datetime.datetime.utcfromtimestamp(unixDatetime).strftime("%Y-%m-%d")
        if date in weathers:
            weathers[date].append(weather)
        else:
            weathers[date] = [weather]
    return weathers

# def maximumTemperature(weather):
#     return min(map(minimumTemperature, weather.values()))
#
#     # maximumTemperature = weather["temp_max"]
#     # # minimumTemperature = weather["temp_min"]
#     # return maximumTemperature
#
# def minimumTemperature(weather):
#     return weather["temp_min"]














