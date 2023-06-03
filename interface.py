import tkinter as tk
from PIL import Image, ImageTk

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

dayButtons = []

todayIndex = 1
# 초기 선택은 오늘 날짜
selectedIndex = 1

def onDayClick(event, newIndex):
  print(event, newIndex)
  global selectedIndex, dayButtons
  selectedIndex = newIndex
  changeDayBg()

def changeDayBg():
  for index in range(7):
    image = getDayImage(index)
    canvas.itemconfig(dayButtons[index], image = image)

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

for index in range(7):
    x = BOX_SPACING + index * (BOX_WIDTH + BOX_SPACING)
    image = getDayImage(index)
    
    dayButtons.insert(index, canvas.create_image(x, 30, image=image, anchor=tk.NW))
    canvas.tag_bind(dayButtons[index], "<Button>", lambda event, index=index: onDayClick(event, index)) 

root.mainloop()
