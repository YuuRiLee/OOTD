import tkinter as tk
from tkinter import Label
from PIL import Image, ImageDraw, ImageFont, ImageTk

WIDTH = 892
HEIGHT = 630
HALF_WIDTH = WIDTH /2
BG_WIDTH = 892 / 2

DAY_LENGTH = 7

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

todayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/today_bg.png'))
selectedTodayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/selected_today_bg.png'))

otherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/other_day_bg.png'))
selectedOtherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/selected_other_day_bg.png'))

dayTextBgImage = Image.open('./assets/img/day_text_bg.png')
dayButtons = []
dayTextImages = []

todayIndex = 1
# 초기 선택은 오늘 날짜
selectedIndex = 1

def onDayClick(event, newIndex):
  print(event, newIndex)
  global selectedIndex
  selectedIndex = newIndex
  changeDayBg()

def changeDayBg():
  for index in range(7):
    image = getDayImage(index)
    canvas.itemconfig(dayButtons[index][0], image = image)

def getDayImage(index):
  if (index == todayIndex and index == selectedIndex):
    image = selectedTodayBgImage
  elif (index == todayIndex):
    image = todayBgImage
  elif (index == selectedIndex):
    image = selectedOtherDayBgImage
  else:
    image = otherDayBgImage
  return image

def createDayLabel():
  global dayTextImages
  image_with_text = dayTextBgImage.copy()
  draw = ImageDraw.Draw(image_with_text)
  font = ImageFont.load_default()
  draw.text((10, 10), f"Day {index+1}", font=font, fill=(255, 255, 255))
  dayTextImage = ImageTk.PhotoImage(image_with_text)
  dayTextImages.append(dayTextImage)  # Keep a reference to the image
  
for index in range(7):
    createDayLabel()
    dayImage = getDayImage(index)
    
    x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
    
    dayButton = canvas.create_image(x, 30, image=dayImage, anchor=tk.NW)
    dayText = canvas.create_image(x, 30, image=dayTextImages[index], anchor='nw')
    
    canvas.tag_bind(dayButton, "<Button>", lambda event, index=index: onDayClick(event, index))
    
    dayButtons.insert(index, (dayButton, dayText))

root.mainloop()
