"""
负责程序控件的创建和布局
"""
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.messagebox as mb

import os
from DataObject import *
import figure
import plot


def widget_main(win, root):
    """
    win : 窗体对象
    root : 绘图区容器对象
    """
    frame_fig = None

    # -------------功能区---------------
    def frame_init():
        nonlocal frame_fig
        if frame_fig is not None:
            frame_fig.destroy()
            frame_fig = None
        frame_fig = Frame(win)
        frame_fig.place(relx=0.00, rely=0.12, relwidth=0.62, relheight=0.88)

    def select_path():
        path_ = askopenfilename(filetypes=[("TXT", ".txt")])
        path.set(path_)

    def load_data_from_file():
        nonlocal frame_fig
        filepath = path.get()
        engine.clear()
        result.delete(1.0, END)
        engine.set_filepath(filepath)
        if filepath is None or len(filepath) == 0:
            mb.showerror("提示:路径不能为空")
        elif not os.path.exists(filepath):
            mb.showerror("目标文件不存在")
        else:
            engine.load_data()

            data_index.set(str(1))
            frame_init()
            axs = figure.plot(frame_fig)
            # plot.raw_plot(axs, engine.get_raw())
            plot.pre_all_data(axs, engine.get_add_data(), 1)
            result.delete(1.0, END)
            result.insert(END, "加载数据完毕,共有%d个周期,当前显示的是第%d个周期" %
                          (engine.get_all_data_size(), engine.get_raw_index() + 1))

    def pre_select_data():
        try:
            index = int(data_index.get())
            if 0 < index <= engine.get_all_data_size():
                frame_init()
                axs = figure.plot(frame_fig)
                plot.pre_all_data(axs, engine.get_add_data(), index)
                result.delete(1.0, END)
                result.insert(END, "加载数据完毕,共有%d个周期,当前显示的是第%d个周期" %
                              (engine.get_all_data_size(), engine.get_raw_index() + 1))
            else:
                mb.showerror("输入的值不在周期范围内")

        except ValueError:
            mb.showerror("请输入正确格式的值")

    def select_data():
        try:
            index = int(data_index.get())
            res = engine.set_raw_index(index)

            if res:
                left_bound.set(str(engine.get_xmin()))
                right_bound.set(str(engine.get_xmax()))
                left_peak.set(str(engine.get_xmin()))
                right_peak.set(str(engine.get_xmax()))
                level.set(str(5))
                formula.set(engine.get_formula())
                reset_fig()
                result.delete(1.0, END)
                result.insert(END, "加载数据完毕,共有%d个周期,当前显示的是第%d个周期" %
                              (engine.get_all_data_size(), engine.get_raw_index() + 1))
            else:
                mb.showerror("输入的值不在周期范围内")

        except ValueError:
            mb.showerror("请输入正确格式的值")

    def set_bound():
        try:
            left_bound_ = float(left_bound.get())
            right_bound_ = float(right_bound.get())
            left_peak_ = float(left_peak.get())
            right_peak_ = float(right_peak.get())

            if left_bound_ < left_peak_ < right_peak_ < right_bound_:
                res = engine.set_bound(left_bound_, right_bound_, left_peak_, right_peak_)
                frame_init()
                axs = figure.plot(frame_fig)
                plot.pre_plot(axs, res)
            else:
                mb.showerror("设定参数大小顺序不正确")
        except ValueError as e:
            mb.showerror("请输入正确格式的数字")

    def reset_fig():
        frame_init()
        axs = figure.plot(frame_fig)
        plot.raw_plot(axs, engine.get_raw())

    def optimize_cur():
        try:
            level_ = int(level.get())
            data = engine.optimize_bg(level_)
            frame_init()
            axs = figure.plot(frame_fig)
            plot.cur_plot(axs, data)
        except ValueError as e:
            mb.showerror("请输入正确格式的值")

    def line_background():
        try:
            x1_ = float(x1.get())
            x2_ = float(x2.get())
            y1_ = float(y1.get())
            y2_ = float(y2.get())
            if x1_ == x2_ and y1_ == y2_:
                mb.showerror("请输入两个不同的点")
            else:
                data = engine.optimize_line(x1_, y1_, x2_, y2_)
                frame_init()
                axs = figure.plot(frame_fig)
                plot.cur_plot(axs, data)

        except ValueError:
            mb.showerror("请输入正确格式的值")

    def intergrate():
        formula_ = formula.get()
        engine.set_formula(formula_)
        res = engine.integrate()
        result.delete(1.0, END)
        result.insert(END, "峰积分结果:  %.4g \n" % res[0])
        result.insert(END, "背景积分结果: %.4g \n" % res[1])
        result.insert(END, "峰最终面积:  %.4g \n" % res[2])
        result.insert(END, "面积处理公式: %s \n" % res[3])
        result.insert(END, "最终结果: %.4g \n" % res[4])

    def output_data():
        writer = asksaveasfile(filetypes=[("TXT", ".txt")])
        engine.output(writer)

    def test():
        result.insert(END, "%s \n" % (win.winfo_geometry()))

    def egg(event):
        mb.showinfo("Surprise!", "Author:Nan Hang\n"
                                 "Github:https://github.com/nanharder/calECSA")

    # -------------控件区----------------

    """
    加载数据并显示原始数据图像
    """
    label = Label(root, text="请选择原始数据文件:")
    label.place(relx=0.1, rely=0.05, relheight=0.035)

    engine = Engine()
    path = StringVar()
    entry = Entry(root, textvariable=path)
    entry.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.038)
    button = Button(root, text="文件选择", cursor="hand2", command=select_path)
    button.place(relx=0.1, rely=0.15, relwidth=0.2)

    btn_draw = Button(root, text="加载数据", cursor="hand2", command=load_data_from_file)
    btn_draw.place(relx=0.4, rely=0.15, relwidth=0.2)

    btn_reset = Button(root, text="重置图像", cursor="hand2", command=reset_fig)
    btn_reset.place(relx=0.7, rely=0.15, relwidth=0.2)

    data_index = StringVar()
    Label(root, text=" 数据周期编号:").place(relx=0.1, rely=0.2225, relheight=0.038)
    entry_index = Entry(root, textvariable=data_index)
    entry_index.place(relx=0.3, rely=0.225, relwidth=0.08, relheight=0.038)

    btn_pre_select = Button(root, text="预览数据", cursor="hand2", command=pre_select_data)
    btn_pre_select.place(relx=0.4, rely=0.225, relwidth=0.2)

    btn_select_data = Button(root, text="选择数据", cursor="hand2", command=select_data)
    btn_select_data.place(relx=0.7, rely=0.225, relwidth=0.2)

    """
    设置取点范围
    """
    left_bound = StringVar()
    right_bound = StringVar()
    left_peak = StringVar()
    right_peak = StringVar()

    Label(root, text=" 背景左边界:").place(relx=0.1, rely=0.3, relheight=0.038)
    entry1 = Entry(root, textvariable=left_bound)
    entry1.place(relx=0.3, rely=0.3, relwidth=0.15, relheight=0.038)
    Label(root, text=" 背景右边界:").place(relx=0.55, rely=0.3, relheight=0.038)
    entry2 = Entry(root, textvariable=right_bound)
    entry2.place(relx=0.75, rely=0.3, relwidth=0.15, relheight=0.038)

    Label(root, text=" 积分峰左边界:").place(relx=0.1, rely=0.35, relheight=0.038)
    entry3 = Entry(root, textvariable=left_peak)
    entry3.place(relx=0.3, rely=0.35, relwidth=0.15, relheight=0.038)
    Label(root, text=" 积分峰右边界:").place(relx=0.55, rely=0.35, relheight=0.038)
    entry4 = Entry(root, textvariable=right_peak)
    entry4.place(relx=0.75, rely=0.35, relwidth=0.15, relheight=0.038)

    btn_pre = Button(root, text="应用边界", cursor="hand2", command=set_bound)
    btn_pre.place(relx=0.1, rely=0.41, relwidth=0.2)

    level = StringVar()
    Label(root, text=" 背景曲线拟合级数:").place(relx=0.1, rely=0.5, relheight=0.038)
    entry5 = Entry(root, textvariable=level)
    entry5.place(relx=0.35, rely=0.5, relwidth=0.13, relheight=0.038)

    btn_optimize = Button(root, text="拟合背景", cursor="hand2", command=optimize_cur)
    btn_optimize.place(relx=0.6, rely=0.5, relwidth=0.2)

    x1 = StringVar()
    y1 = StringVar()
    x2 = StringVar()
    y2 = StringVar()

    Label(root, text=" x1:").place(relx=0.1, rely=0.55, relheight=0.038)
    entry6 = Entry(root, textvariable=x1)
    entry6.place(relx=0.18, rely=0.55, relwidth=0.1, relheight=0.038)
    Label(root, text=" y1:").place(relx=0.3, rely=0.55, relheight=0.038)
    entry7 = Entry(root, textvariable=y1)
    entry7.place(relx=0.38, rely=0.55, relwidth=0.1, relheight=0.038)

    Label(root, text=" x2:").place(relx=0.1, rely=0.6, relheight=0.038)
    entry8 = Entry(root, textvariable=x2)
    entry8.place(relx=0.18, rely=0.6, relwidth=0.1, relheight=0.038)
    Label(root, text=" y2:").place(relx=0.3, rely=0.6, relheight=0.038)
    entry9 = Entry(root, textvariable=y2)
    entry9.place(relx=0.38, rely=0.6, relwidth=0.1, relheight=0.038)

    btn_select_data = Button(root, text="直线背景", cursor="hand2", command=line_background)
    btn_select_data.place(relx=0.6, rely=0.575, relwidth=0.2)

    formula = StringVar()
    Label(root, text=" 积分结果处理:").place(relx=0.1, rely=0.65, relheight=0.038)
    entry10 = Entry(root, textvariable=formula)
    entry10.place(relx=0.3, rely=0.65, relwidth=0.35, relheight=0.038)
    btn_inter = Button(root, text="积分", cursor="hand2", command=intergrate)
    btn_inter.place(relx=0.7, rely=0.65, relwidth=0.2)

    result = Text(root)
    result.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

    btn_inter = Button(root, text="输出数据", cursor="hand2", command=output_data)
    btn_inter.place(relx=0.1, rely=0.92, relwidth=0.2)

    '''
    test = Button(root, text="输出窗体大小", command=test)
    test.place(relx=0.1, rely=0.92)
    '''

    # 彩蛋环节
    win.bind("<Control-n>", egg)
