import forecast
import interface

soogsil = {
    "latitude": 37.494705526855,
    "longitude": 126.95994559383
}

if __name__ == "__main__":
    # 날씨 예측 API 호출
    data = forecast.forecast(
        soogsil["latitude"],
        soogsil["longitude"]
    )
# Tkinter를 통해 UI 빌드
interface.createCanvas(data)
