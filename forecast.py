from enum import Enum
import datetime
import holidays
import json
import remoteAPI

# parameter 데이터 받고, RemoteAPI 호출
def forecast(
        latitude,
        longitude,
        units="metric",  # api default = "standard"(Fahrenheit)
        mode="json",
        language="kr",
        exclude="minutely,hourly,alerts"
):
    parameters = {
        "lat": latitude,
        "lon": longitude,
        "units": units,
        "mode": mode,
        "lang": language,
        "exclude": exclude,
    }
    response = remoteAPI.getRequest("/onecall", parameters)
    jsonResponse = json.loads(response.text)
    print(list(map(asDomain, jsonResponse.get("daily"))))
    return list(map(asDomain, jsonResponse.get("daily")))

class Condition(Enum):
    Sunny = 0
    Clouds = 1
    Rain = 2
    Snow = 3

def getCondition(stringValue):
    if stringValue == "Sunny":
        return Condition.Sunny
    elif stringValue == "Clouds":
        return Condition.Clouds
    elif stringValue == "Rain":
        return Condition.Rain
    elif stringValue == "Snow":
        return Condition.Snow
    else:
        return Condition.Sunny

def getIsHoliday(date, country ="KR"):
    holidayList = holidays.CountryHoliday(country)
    return date in holidayList

def getClothesFileNames(temperature):
    if temperature >= 27:
        return ["clothes27_1", "clothes27_2"]
    elif 23 <= temperature <= 26.99:
        return ["clothes23_26_1", "clothes23_26_2"]
    elif 20 <= temperature <= 22.99:
        return ["clothes20_22_1", "clothes20_22_2"]
    elif 17 <= temperature <= 19.99:
        return ["clothes17_19_1", "clothes17_19_2"]
    else:
        return ["clothes_16_1", "clothes_16_2"]

# UI 표현에 필요한 데이터로 변경 및 전달
def asDomain(dailyWeather):
    date = datetime.datetime.fromtimestamp(dailyWeather.get("dt")).date()
    isHoliday = getIsHoliday(date)
    minimumTemperature = dailyWeather.get("temp").get("min")
    maximumTemperature = dailyWeather.get("temp").get("max")
    description = dailyWeather.get("summary")
    condition = getCondition(dailyWeather.get("weather")[0].get("main"))
    weatherIconFileName = dailyWeather.get("weather")[0].get("icon")
    isUmbrellaRequired = condition in [Condition.Rain, Condition.Snow]
    clothesFileNames = {
        "minimum": getClothesFileNames(minimumTemperature),
        "maximum": getClothesFileNames(maximumTemperature)
    }

    return {
        "date": date,
        "isHoliday": isHoliday,
        "minimumTemperature": minimumTemperature,
        "maximumTemperature": maximumTemperature,
        "condition": condition,
        "description": description,
        "isUmbrellaRequired": isUmbrellaRequired,
        "clothesFileNames": clothesFileNames,
        "weatherIconFileName": weatherIconFileName
    }