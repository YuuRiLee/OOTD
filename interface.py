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


todayIndex = 1
selectedIndex = 1

# 날짜 선택 UI
BOX_SPACING = 15
BOX_WIDTH = 110

todayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/today_bg.png'))
selectedTodayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/selected_today_bg.png'))

otherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/other_day_bg.png'))
selectedOtherDayBgImage = ImageTk.PhotoImage(Image.open('./assets/img/other_day_bg.png'))


for i in range(7):
    x = BOX_SPACING + i * (BOX_WIDTH + BOX_SPACING)
    if (i == todayIndex and i == selectedIndex):
      image = selectedTodayBgImage
    elif (i == todayIndex):
      image = todayBgImage
    elif (i == selectedIndex):
      image = otherDayBgImage
    else:
      image = otherDayBgImage
    Button = canvas.create_image(x, 30, image=image, anchor=tk.NW)

root.mainloop()
