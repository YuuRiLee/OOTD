import forecast
import interface
import json
import datetime
from enum import Enum

soogsil = {
    "latitude": 37.494705526855,
    "longitude": 126.95994559383
}

if __name__ == "__main__":
    forecast.forecast(
        soogsil["latitude"],
        soogsil["longitude"]
    )

class Condition(Enum):
    Sunny = 0
    Clouds = 1
    Rain = 2
    
def convertData(data):
    for item in data:
        # 날짜를 문자열에서 datetime.date 객체로 변환
        dateStr = item["date"].replace("datetime.date(", "").replace(")", "")
        year, month, day = map(int, dateStr.split(", "))
        item["date"] = datetime.date(year, month, day)

    return data

with open('mock_domain_data.json', 'r') as jsonFile:
    data = json.load(jsonFile)
    data = convertData(data)
    interface.createCanvas(data)
