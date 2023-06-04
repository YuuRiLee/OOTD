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
    print(asDomain(weathers))

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
def maximumTemperature(weathers):
    return max(list(map(lambda value: value.get("main").get("temp_max"), weathers)))
def minimumTemperature(weathers):
    return min(list(map(lambda value: value.get("main").get("temp_min"), weathers)))

def asDomain(weatherList):
    data = {}
    for weathers in weatherList.items():
        data.update({
            weathers[0]: {
                "maximumTemperature": maximumTemperature(weathers[1]),
                "minimumTemperature": minimumTemperature(weathers[1])
            }
        })
    return data













