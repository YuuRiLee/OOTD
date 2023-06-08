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
    data = forecast.forecast(
        soogsil["latitude"],
        soogsil["longitude"]
    )

interface.createCanvas(data)