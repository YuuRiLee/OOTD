import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

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

# 날짜 선택 UI
BOX_SPACING = 15
BOX_WIDTH = 110
BOX_HEIGHT = 188

speechText = {}
data = []
# 초기 선택은 오늘 날짜
selectedIndex = 1

def createBody():
  global bodyImage, speechText
  bodyImage = ImageTk.PhotoImage(Image.open('./assets/img/body.png'))
  canvas.create_image(83, 197, image=bodyImage, anchor='nw')
  canvas.create_image(525, 197, image=bodyImage, anchor='nw')
  canvas.create_image(42, 457, image=speechBubblesImage, anchor='nw')

  speechDescription = translate.translateText(data[selectedIndex]['description'])

  speechFrame = tk.Frame(canvas, width=500, height=50)
  speechFrame.place(x=110, y=478)
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

def onDayChange(newIndex):
  global selectedIndex
  selectedIndex = newIndex
  speechDescription = translate.translateText(data[selectedIndex]['description'])
  speechText.configure(state="normal")
  speechText.delete("1.0", tk.END)
  speechText.insert(tk.END, speechDescription)
  speechText.configure(state="disabled")

def createCanvas(initialData):
  global data
  data = [None] + initialData
  dayManager = daysInterface.DayManager(canvas, data, selectedIndex, onDayChange)
  dayManager.createDays()
  createBody()

  root.mainloop()
