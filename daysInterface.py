import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

BOX_SPACING = 15
BOX_WIDTH = 110
BOX_HEIGHT = 188
DAY_LENGTH = 7
TODAY_INDEX = 1

DAY_OF_WEEK_KR = ['월', '화', '수', '목', '금', '토', '일']

class DayManager:
  def __init__(self, canvas, data, selectedIndex, callback):
    self.selectedIndex = selectedIndex
    self.canvas = canvas
    self.data = data
    self.dayButtons = []
    self.dayTextImages = []
    self.dayWeatherImages = []
    self.callback = callback
    
    self.todayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/today_bg.png'))
    selectedToday = Image.open('./assets/img/selected_today_bg.png')
    self.selectedTodayBgImage = ImageTk.PhotoImage(selectedToday.resize((126, 202), Image.LANCZOS))
    self.otherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/other_day_bg.png'))
    selectedOtherDay = Image.open('./assets/img/selected_other_day_bg.png')
    self.selectedOtherDayBgImage = ImageTk.PhotoImage(selectedOtherDay.resize((126, 202), Image.LANCZOS))
    self.dayTextBgImage = Image.open('./assets/img/day_text_bg.png')

  def onDayClick(self, _event, newIndex):
    self.selectedIndex = newIndex
    self.changeDayBg()
    self.callback(newIndex)
    
  def changeDayBg(self):
    for index in range(DAY_LENGTH):
      image = self.getDayImage(index)
      self.canvas.itemconfig(self.dayButtons[index][0], image = image)

  def getDayImage(self, index):
    if (index == TODAY_INDEX and index == self.selectedIndex):
      image = self.selectedTodayBgImage
    elif (index == TODAY_INDEX):
      image = self.todayBgImage
    elif (index == self.selectedIndex):
      image = self.selectedOtherDayBgImage
    else:
      image = self.otherDayBgImage
    return image

  def getWeatherImage(self, weather):
    image = ImageTk.PhotoImage(Image.open(f'./assets/icon/{weather}.png'))
    self.dayWeatherImages.append(image)
    
    return image

  def createDayLabel(self, index):
    imageWithText = self.dayTextBgImage.copy()
    data = self.data[index]
    date = data['date']
    isHoliday = data['isHoliday'] or date.weekday() == 6

    draw = ImageDraw.Draw(imageWithText)
    font = ImageFont.truetype('./assets/font/NanumGothicExtraBold.ttf', 12)
    text = f"{date.month}/{date.day} ({DAY_OF_WEEK_KR[date.weekday()]})"
    bbox = font.getbbox(text)
    textWidth = bbox[2]-bbox[0]
    x = (self.dayTextBgImage.width - textWidth) / 2
    textColor = '#B00505' if isHoliday else '#19007E' 
    draw.text((x, 2), text, font=font, fill=textColor)
    dayTextImage = ImageTk.PhotoImage(imageWithText)
    self.dayTextImages.append(dayTextImage)  # Keep a reference to the image
  
  def createDays(self):
    for index in range(7):
      self.createDayLabel(index)
      dayImage = self.getDayImage(index)
      # FIXME 실제 데이터로 변환
      dayWeatherImage = self.getWeatherImage('01d')
      nightWeatherImage = self.getWeatherImage('01n')
      
      x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
      boxX = x + BOX_SPACING
      boxY = 30
      boxCenterY = BOX_HEIGHT / 2 + 30
      labelX = (BOX_WIDTH - self.dayTextImages[index].width()) / 2

      dayButton = self.canvas.create_image(x, boxY, image=dayImage, anchor=tk.NW)
      dayText = self.canvas.create_image(x + labelX, boxY + 10, image=self.dayTextImages[index], anchor='nw')
      dayWeather = self.canvas.create_image(x + 42, boxY + 34, image=dayWeatherImage, anchor='nw')
      nightWeather = self.canvas.create_image(x + 42, boxCenterY + 16, image=nightWeatherImage, anchor='nw')
      
      self.dayButtons.insert(index, (dayButton, dayText, dayWeather, nightWeather))
      
      self.canvas.create_text(boxX + 12, boxY + 56, text="낮", fill="#000000", font=('NanumGothicExtraBold', 12))
      self.canvas.create_line(boxX, boxCenterY, boxX + 82, boxCenterY, fill="#9A9A9A", width=3)
      self.canvas.create_text(boxX + 12, boxCenterY + 40, text="밤", fill="#000000", font=('NanumGothicExtraBold', 12))

      for item in self.dayButtons[index]:
        self.canvas.tag_bind(item, "<Button>", lambda event, index=index: self.onDayClick(event, index))

        