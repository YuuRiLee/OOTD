import forecast

soogsil = {
    "latitude": 37.494705526855,
    "longitude": 126.95994559383
}

if __name__ == "__main__":
    forecast.forecast(
        soogsil["latitude"],
        soogsil["longitude"],
        50
    )
