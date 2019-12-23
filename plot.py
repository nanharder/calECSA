"""
负责图像的绘制
"""


# 对输入的x列和y列获取适当的边界
def get_bound(x, y):
    x_max = max(x)
    x_min = min(x)
    x_shift = 0.05 * (x_max - x_min)

    y_max = max(y)
    y_min = min(y)
    y_shift = 0.05 * (y_max - y_min)

    return x_min - x_shift, x_max + x_shift, y_min - y_shift, y_max + y_shift


# 绘制周期数据的图像
def raw_plot(plt, raw_data):
    x_col = raw_data.get_xcol()
    y_col = raw_data.get_ycol()

    bounds = get_bound(x_col, y_col)

    plt.scatter(x_col, y_col, 10, 'red')
    plt.set_xlim(bounds[0], bounds[1])
    plt.set_ylim(bounds[2], bounds[3])


# 设置好边界后绘制图像
def pre_plot(plt, data):
    bounds = get_bound(data[0] + data[2], data[1] + data[3])

    plt.scatter(data[0] + data[2], data[1] + data[3], 10, 'red')
    plt.vlines(data[2][0], bounds[2], bounds[3], color='blue', linewidth=1.5, linestyle='--')
    plt.vlines(data[2][-1], bounds[2], bounds[3], color='blue', linewidth=1.5, linestyle='--')
    plt.set_xlim(bounds[0], bounds[1])
    plt.set_ylim(bounds[2], bounds[3])
    # plt.show()


# 在数据本身之上添加拟合的背景的曲线
def cur_plot(plt, data):
    pre_plot(plt, data)
    plt.plot(data[4], data[5], "r--", color="blue")


# 绘制所有数据的图像,并将当前所选周期的数据红色表示
def pre_all_data(plt, all_data, index):
    all_x = []
    all_y = []
    for i in range(len(all_data)):
        x_col = all_data[i].get_xcol()
        y_col = all_data[i].get_ycol()
        all_x += x_col
        all_y += y_col
        if i == index - 1:
            plt.scatter(x_col, y_col, 10, 'red')
        else:
            plt.scatter(x_col, y_col, 10, 'black')

    bounds = get_bound(all_x, all_y)
    plt.set_xlim(bounds[0], bounds[1])
    plt.set_ylim(bounds[2], bounds[3])


# 绘制周期数据,并使用鼠标点击设置分割直线的位置
def find_pos(axs, fig, raw_data, bound):
    def call_back(event):
        axs.cla()
        raw_plot(axs, raw_data)
        axs.vlines(event.xdata, y_min - y_shift, y_max + y_shift, color='black', linewidth=1.5, linestyle='--')
        fig.canvas.draw()
        bound.set("%.4g" % event.xdata)

    raw_plot(axs, raw_data)
    y_min = min(raw_data.get_ycol())
    y_max = max(raw_data.get_ycol())

    y_shift = 0.05 * (y_max - y_min)
    fig.canvas.mpl_connect('button_press_event', call_back)


# 绘制周期数据,并使用鼠标点击设置取的点的位置
def find_bg(axs, fig, detail_data, bg_x, bg_y):
    def call_back(event):
        axs.cla()
        pre_plot(axs, detail_data)
        axs.scatter([event.xdata], [event.ydata], color='black', marker='+', s=80)
        fig.canvas.draw()
        bg_x.set("%.4g" % event.xdata)
        bg_y.set("%.4g" % event.ydata)

    pre_plot(axs, detail_data)
    fig.canvas.mpl_connect('button_press_event', call_back)
