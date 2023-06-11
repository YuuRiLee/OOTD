import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import random

import daysInterface
import translate

WIDTH = 892
HEIGHT = 630
HALF_WIDTH = WIDTH / 2
BG_WIDTH = 892 / 2

root = tk.Tk()
root.geometry("891x630")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
textContainer = tk.Canvas(root, width=200, height=100, bd=0, highlightthickness=0, background="white")

canvas.place(x=0, y=0)

# 날씨 description이 길어졌을 때 scroll 추가
scrollbar = tk.Scrollbar(textContainer, orient=tk.VERTICAL)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)

# 낮 배경 설정
dayBgImage = ImageTk.PhotoImage(Image.open("./assets/img/day_bg.png"))
dayBg = canvas.create_image(0, 0, image=dayBgImage, anchor=tk.NW)

# 밤 배경 설정
nightBgImage = ImageTk.PhotoImage(Image.open("./assets/img/night_bg.png"))
nightBg = canvas.create_image(HALF_WIDTH - 10, 0, image=nightBgImage, anchor=tk.NW)

speechBubblesImage = ImageTk.PhotoImage(Image.open('./assets/img/speech_bubbles.png'))

speechText = None
selectedClothes = []

clothes = []
data = []
# 초기 선택은 오늘 날짜
selectedIndex = 1

# 최고 온도, 최저 온도에 따른 옷차림 image 반환
def createClothesImage():
  for index in range(7):
    if data[index] is None:
      clothes.insert(index, (None, None))
      continue

    minimumClothesList = data[index]['clothesFileNames']['minimum']
    maximumClothesList = data[index]['clothesFileNames']['maximum']
    
    # 각 기온에 따른 옷차림을 랜덤하게 추출
    minimumClothes = random.choice(minimumClothesList)
    maximumClothes = random.choice(maximumClothesList)
    
    minimumImage = ImageTk.PhotoImage(Image.open(f'./assets/clothes/{minimumClothes}.png'))
    maximumImage = ImageTk.PhotoImage(Image.open(f'./assets/clothes/{maximumClothes}.png'))
  
    # 날짜를 변경해도 랜덤하게 결정된 옷차림 데이터는 변경되지 않도록 변수에 저장
    clothes.insert(index, (maximumImage, minimumImage))

# 마스코트(슝슝이) 그리기
def createBody():
  global bodyImage, speechText, selectedClothes
  bodyImage = ImageTk.PhotoImage(Image.open('./assets/img/body.png'))
  [maximumImage, minimumImage] = clothes[selectedIndex]
  canvas.create_image(83, 197, image=bodyImage, anchor='nw')
  maximumClothes = canvas.create_image(175, 355, image=maximumImage, anchor='nw')
  canvas.create_image(525, 197, image=bodyImage, anchor='nw')
  minimumClothes = canvas.create_image(618, 355, image=minimumImage, anchor='nw')
  canvas.create_image(42, 457, image=speechBubblesImage, anchor='nw')

  selectedClothes = [maximumClothes, minimumClothes]
  speechDescription = translate.translatedText(data[selectedIndex]['description'])

  speechFrame = tk.Frame(canvas, width=500, height=50)
  speechFrame.place(x=110, y=478)
  # 날씨 description 영역에 최대 width와 최대 height 지정
  speechText = scrolledtext.ScrolledText(
        speechFrame,
        width=48,
        height=4,
        wrap=tk.WORD,
        font=("Arial", 24),
        background="white",
        foreground="black",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
      )
  speechText.insert("end", speechDescription)
  speechText.pack(fill="both", expand=True)
  speechText.configure(state="disabled")

  scrollbar.config(command=speechText.yview)

# 날짜 클릭했을 때 description 업데이트
def onDayChange(newIndex):
  global selectedIndex
  selectedIndex = newIndex
  # 영어로된 description을 한국어로 번역
  speechDescription = translate.translatedText(data[selectedIndex]['description'])
  # description을 변경하기 위해 normal로 상태 변경
  speechText.configure(state="normal")
  speechText.delete("1.0", tk.END)
  speechText.insert(tk.END, speechDescription)
  speechText.configure(state="disabled")
  
  [maximumImage, minimumImage] = clothes[selectedIndex]
  canvas.itemconfig(selectedClothes[0], image = maximumImage)
  canvas.itemconfig(selectedClothes[1], image = minimumImage)

def createCanvas(initialData):
  global data
  data = [None] + initialData
  dayManager = daysInterface.DayManager(canvas, data, selectedIndex, onDayChange)
  dayManager.createDays()
  createClothesImage()
  createBody()

  root.mainloop()
