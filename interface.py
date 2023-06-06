import tkinter as tk
from PIL import Image, ImageTk
import daysInterface

WIDTH = 892
HEIGHT = 630
HALF_WIDTH = WIDTH /2
BG_WIDTH = 892 / 2

root = tk.Tk()
root.geometry("891x630")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bd=0)
canvas.place(x=0, y=0)

# 낮 배경 설정
dayBgImage = ImageTk.PhotoImage(Image.open("./assets/img/day_bg.png"))
dayBg = canvas.create_image(0, 0, image=dayBgImage, anchor=tk.NW)

# 밤 배경 설정
nightBgImage = ImageTk.PhotoImage(Image.open("./assets/img/night_bg.png"))
nightBg = canvas.create_image(HALF_WIDTH - 10, 0, image=nightBgImage, anchor=tk.NW)

# 날짜 선택 UI
BOX_SPACING = 15
BOX_WIDTH = 110
BOX_HEIGHT = 188

leftSpeechBubblesImage = ImageTk.PhotoImage(Image.open('./assets/img/left_speech_bubbles.png'))
rightSpeechBubblesImage = ImageTk.PhotoImage(Image.open('./assets/img/right_speech_bubbles.png'))

bodyButtons = []

todayIndex = 1
# 초기 선택은 오늘 날짜
selectedIndex = 1
selectedDay = 'day'

def onBodyClick(_event, dayType):
  global selectedDay
  selectedDay = dayType
  image = getSpeechImage()
  canvas.itemconfig(bodyButtons[0], image = image)

def getSpeechImage():
  return leftSpeechBubblesImage if selectedDay == 'day' else rightSpeechBubblesImage

def createBody():
  global bodyImage
  bodyImage = ImageTk.PhotoImage(Image.open('./assets/img/body.png'))
  speechBgImage = getSpeechImage()
  dayBodyButton = canvas.create_image(136, 216, image=bodyImage, anchor='nw')
  nightBodyButton = canvas.create_image(595, 216, image=bodyImage, anchor='nw')
  speechImage = canvas.create_image(42, 407, image=speechBgImage, anchor='nw')

  bodyButtons.insert(0, speechImage)

  canvas.tag_bind(dayBodyButton, "<Button>", lambda event: onBodyClick(event, 'day'))
  canvas.tag_bind(nightBodyButton, "<Button>", lambda event: onBodyClick(event, 'night'))
  
def createCanvas(data):
  print(data)
  dayManager = daysInterface.DayManager(todayIndex, selectedIndex, canvas)
  dayManager.createDays()
  createBody()

  root.mainloop()
