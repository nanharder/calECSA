"""
负责程序的启动和结束
"""
from tkinter import *
import widget


def build_win(root):

    # 设置标题
    root.title("ECSA计算工具")

    # 获取屏幕大小
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()

    # 获取窗体大小
    win_height = 0.8 * screen_height
    win_width = 0.8 * screen_width

    # 获取窗体位置
    show_width = (screen_width - win_width) / 2
    show_height = (screen_height - win_height) / 2

    return win_width, win_height, show_width, show_height


win = Tk()
# 设置大小，位置
win.geometry("%dx%d+%d+%d" % build_win(win))
win.minsize(1344, 720)

# 设置窗体背景
frame1 = Frame(win, bg="#D9D9D9")
frame1.place(relx=0.00, rely=0.05, relwidth=0.62, relheight=0.90)

# 控件区
frame2 = Frame(win, bg="#808080")
frame2.place(relx=0.62, rely=0.05, relwidth=0.38, relheight=0.95)

widget.widget_main(win, frame2)
win.mainloop()
