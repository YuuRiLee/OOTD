import tkinter as tk
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

leftSpeechBubblesImage = ImageTk.PhotoImage(Image.open('./assets/img/left_speech_bubbles.png'))
rightSpeechBubblesImage = ImageTk.PhotoImage(Image.open('./assets/img/right_speech_bubbles.png'))

dayButtons = []
dayTextImages = []
dayWeatherImages = []

bodyButtons = []

todayIndex = 1
# 초기 선택은 오늘 날짜
selectedIndex = 1
selectedDay = 'day'

def onDayClick(_event, newIndex):
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

def getWeatherImage(weather):
  image = ImageTk.PhotoImage(Image.open(f'./assets/icon/{weather}.png'))
  dayWeatherImages.append(image)
  
  return image
    
def createDayLabel(index):
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

def crateDays():
  for index in range(7):
    createDayLabel(index)
    dayImage = getDayImage(index)
    # FIXME 실제 데이터로 변환
    dayWeatherImage = getWeatherImage('01d')
    nightWeatherImage = getWeatherImage('01n')
    
    x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
    boxX = x + BOX_SPACING
    boxY = 30
    boxCenterY = BOX_HEIGHT / 2 + 30
    labelX = (BOX_WIDTH - dayTextImages[index].width()) / 2

    dayButton = canvas.create_image(x, boxY, image=dayImage, anchor=tk.NW)
    dayText = canvas.create_image(x + labelX, boxY + 10, image=dayTextImages[index], anchor='nw')
    dayWeather = canvas.create_image(x + 42, boxY + 34, image=dayWeatherImage, anchor='nw')
    nightWeather = canvas.create_image(x + 42, boxCenterY + 16, image=nightWeatherImage, anchor='nw')
    
    dayButtons.insert(index, (dayButton, dayText, dayWeather, nightWeather))
    
    canvas.create_text(boxX + 12, boxY + 56, text="낮", fill="#000000", font=('NanumGothicExtraBold', 12))
    canvas.create_line(boxX, boxCenterY, boxX + 82, boxCenterY, fill="#9A9A9A", width=3)
    canvas.create_text(boxX + 12, boxCenterY + 40, text="밤", fill="#000000", font=('NanumGothicExtraBold', 12))

    for item in dayButtons[index]:
      canvas.tag_bind(item, "<Button>", lambda event, index=index: onDayClick(event, index))

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
  
crateDays()
createBody()

root.mainloop()
