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
    self.lockIcon = ImageTk.PhotoImage(Image.open('./assets/icon/lock.png'))

  # 오늘 데이터 + 미래 5일 데이터 button click event
  def onDayClick(self, _event, newIndex):
    self.selectedIndex = newIndex
    self.changeDayBg()
    self.callback(newIndex)
    
  # 어제 데이터 button click event
  def onBillingClick(self, _event, newIndex):
    self.selectedIndex = newIndex
    # 결제 안내 modal 띄우기
    modal = tk.Toplevel(self.canvas)
    modal.title("결제 안내")
    modal.geometry("300x200")

    label = tk.Label(modal, text="어제 데이터는 추가 결제가 필요합니다.")
    label.pack()
    
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

  # 날씨 icon name에 해당하는 icon image를 반환
  def getWeatherImage(self, weather):
    image = ImageTk.PhotoImage(Image.open(f'./assets/icon/{weather}.png'))
    self.dayWeatherImages.append(image)
    
    return image

  # label 배경 이미지와 날짜 텍스트를 병합한 후 반환
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
    # 휴일인 경우 빨간 텍스트로 표시
    textColor = '#B00505' if isHoliday else '#19007E' 
    draw.text((x, 2), text, font=font, fill=textColor)
    dayTextImage = ImageTk.PhotoImage(imageWithText)
    self.dayTextImages.append(dayTextImage)
  
  def createDays(self):
    for index in range(DAY_LENGTH):
      x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
      boxX = x + BOX_SPACING
      boxY = 30
      isBillingButton = index == 0
    
      dayImage = self.getDayImage(index)
      dayButton = self.canvas.create_image(x, boxY, image=dayImage, anchor=tk.NW)
 
      # 오늘 데이터 + 미래 5일 데이터 button 만들기
      if (isBillingButton == False):
        data = self.data[index]
        dayWeatherImage = self.getWeatherImage(data['weatherIconFileName'])
        
        self.createDayLabel(index)
        labelX = (BOX_WIDTH - self.dayTextImages[index - 1].width()) / 2
        
        minimumTemperature = round(data['minimumTemperature'])
        maximumTemperature = round(data['maximumTemperature'])
        
        dayText = self.canvas.create_image(x + labelX, boxY + 10, image=self.dayTextImages[index - 1], anchor='nw')
        
        # 날짜별 최고 온도 그려주기
        self.canvas.create_text(boxX + 14, boxY + 56, text="최고", fill="#000000", font=('NanumGothicExtraBold', 12))
        self.canvas.create_text(boxX + 70, boxY + 56, text=maximumTemperature, fill="#000000", font=('NanumGothicExtraBold', 16))
        
        # 날짜별 최저 온도 그려주기
        self.canvas.create_text(boxX + 14, boxY + 92, text="최저", fill="#000000", font=('NanumGothicExtraBold', 12))
        self.canvas.create_text(boxX + 70, boxY + 92, text=minimumTemperature, fill="#000000", font=('NanumGothicExtraBold', 16))

        self.canvas.create_line(boxX, boxY + 120, boxX + 82, boxY + 120, fill="#9A9A9A", width=3)
        
        # 날짜별 날씨 icon 그려주기
        dayWeather = self.canvas.create_image(x + 34, boxY + 128, image=dayWeatherImage, anchor='nw')

        self.dayButtons.insert(index, (dayButton, dayText, dayWeather))

        # 각 날짜 button들에 click event 달아주기
        # button 위에 다른 이미지나 텍스트가 놓인 경우 해당 위치로 마우스를 가져가면 이벤트가 발생하지 않을 수 있기 때문에 모든 요소들에 event 추가
        for item in self.dayButtons[index]:
          self.canvas.tag_bind(item, "<Button>", lambda event, index=index: self.onDayClick(event, index))
      # 어제 데이터 button 만들기
      else:
        lockButton = self.canvas.create_image(x + 40, boxY + 77, image=self.lockIcon, anchor=tk.NW)
        self.dayButtons.insert(index, (dayButton, lockButton))

        for item in self.dayButtons[index]:
          self.canvas.tag_bind(item, "<Button>", lambda event, index=index: self.onBillingClick(event, index))
