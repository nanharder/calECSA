"""
画布文件，实现绘图区域的显示
"""
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import figure


def plot(root):
    fig = figure(dpi=120)
    axs = fig.add_subplot(1, 1, 1)

    # 创建画布
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # 创建工具栏
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack()

    # 返回画布对象
    return axs
