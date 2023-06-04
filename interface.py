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
BOX_HEIGHT = 188

todayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/today_bg.png'))
selectedToday = Image.open('./assets/img/selected_today_bg.png')
selectedTodayBgImage = ImageTk.PhotoImage(selectedToday.resize((126, 202), Image.LANCZOS))

otherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/other_day_bg.png'))
selectedOtherDay = Image.open('./assets/img/selected_other_day_bg.png')
selectedOtherDayBgImage = ImageTk.PhotoImage(selectedOtherDay.resize((126, 202), Image.LANCZOS))

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
  font = ImageFont.truetype('./assets/font/NanumGothicExtraBold.ttf', 12)
  # FIXME 실 데이터로 변경
  text = f"6/{index+1} (목)"
  bbox = font.getbbox(text)
  textWidth = bbox[2]-bbox[0]
  x = (dayTextBgImage.width - textWidth) / 2
  # FIXME 실 데이터로 변경
  isHoliday = False
  textColor = '#B00505' if isHoliday else '#19007E' 
  draw.text((x, 2), text, font=font, fill=textColor)
  dayTextImage = ImageTk.PhotoImage(image_with_text)
  dayTextImages.append(dayTextImage)  # Keep a reference to the image

for index in range(7):
    createDayLabel()
    dayImage = getDayImage(index)
    
    x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
    boxX = x + BOX_SPACING
    boxY = 30
    boxCenterY = BOX_HEIGHT / 2 + 30
    labelX = (BOX_WIDTH - dayTextImages[index].width()) / 2
    
    dayButton = canvas.create_image(x, boxY, image=dayImage, anchor=tk.NW)
    dayText = canvas.create_image(x + labelX, boxY + 10, image=dayTextImages[index], anchor='nw')
    canvas.create_text(boxX + 12, boxY + 56, text="오전", fill="#000000", font=('NanumGothicExtraBold', 12))
    canvas.create_line(boxX, boxCenterY, boxX + 82, boxCenterY, fill="#9A9A9A", width=3)
    canvas.create_text(boxX + 12, boxCenterY + 40, text="오후", fill="#000000", font=('NanumGothicExtraBold', 12))

    canvas.tag_bind(dayButton, "<Button>", lambda event, index=index: onDayClick(event, index))
    
    dayButtons.insert(index, (dayButton, dayText))

root.mainloop()