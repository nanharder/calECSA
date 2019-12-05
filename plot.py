"""
负责图像的绘制
"""


def get_bound(x, y):
    x_max = max(x)
    x_min = min(x)
    x_shift = 0.05 * (x_max - x_min)

    y_max = max(y)
    y_min = min(y)
    y_shift = 0.05 * (y_max - y_min)

    return x_min - x_shift, x_max + x_shift, y_min - y_shift, y_max + y_shift


def raw_plot(plt, raw_data):
    x_col = raw_data.get_xcol()
    y_col = raw_data.get_ycol()

    bounds = get_bound(x_col, y_col)

    plt.scatter(raw_data.get_xcol(), raw_data.get_ycol(), 10, 'red')
    plt.set_xlim(bounds[0], bounds[1])
    plt.set_ylim(bounds[2], bounds[3])


def pre_plot(plt, data):
    bounds = get_bound(data[0] + data[2], data[1] + data[3])

    plt.scatter(data[0] + data[2], data[1] + data[3], 10, 'red')
    plt.vlines(data[2][0], bounds[2], bounds[3], color='blue', linewidth=1.5, linestyle='--')
    plt.vlines(data[2][-1], bounds[2], bounds[3], color='blue', linewidth=1.5, linestyle='--')
    plt.set_xlim(bounds[0], bounds[1])
    plt.set_ylim(bounds[2], bounds[3])


def cur_plot(plt, data):
    pre_plot(plt, data)
    plt.plot(data[4], data[5], "r--", color="blue")
