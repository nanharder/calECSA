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
    # 初始化绘图窗口
    def frame_init():
        nonlocal frame_fig
        if frame_fig is not None:
            frame_fig.destroy()
            frame_fig = None
        frame_fig = Frame(win)
        frame_fig.place(relx=0.00, rely=0.12, relwidth=0.62, relheight=0.88)

    # 设置分隔符
    def set_sep():
        engine.set_sep(sep.get())

    # 询问文件路径
    def select_path():
        path_ = askopenfilename(filetypes=[("TXT", ".txt")])
        path.set(path_)

    # 加载数据
    def load_data_from_file():
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
            fig, axs = figure.plot(frame_fig)
            plot.pre_all_data(axs, engine.get_all_data(), 1)
            result.delete(1.0, END)
            result.insert(END, "加载数据完毕,共有%d个周期,当前显示的是第%d个周期" %
                          (engine.get_all_data_size(), 1))

    # 预览所选周期的数据
    def pre_select_data():
        try:
            index = int(data_index.get())
            if 0 < index <= engine.get_all_data_size():
                frame_init()
                fig, axs = figure.plot(frame_fig)
                plot.pre_all_data(axs, engine.get_all_data(), index)
                result.delete(1.0, END)
                result.insert(END, "加载数据完毕,共有%d个周期,当前红色曲线是第%d个周期" %
                              (engine.get_all_data_size(), index))
            else:
                mb.showerror("输入的值不在周期范围内")

        except ValueError:
            mb.showerror("请输入正确格式的值")

    # 选择数据周期
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

    # 根据变量名生成所需的找边界方法
    def gen_find_bound(bound_name):
        def find_bound():
            nonlocal left_bound, right_bound, left_peak, right_peak
            frame_init()
            fig, axs = figure.plot(frame_fig)
            plot.find_pos(axs, fig, engine.get_raw(), eval(bound_name))

        return find_bound

    # 根据变量名生成所需的找点方法
    def gen_find_bg(bg_x, bg_y):
        def find_bg():
            nonlocal x1, x2, y1, y2
            frame_init()
            fig, axs = figure.plot(frame_fig)
            plot.find_bg(axs, fig, engine.get_detail_data(), eval(bg_x), eval(bg_y))

        return find_bg

    # 设置边界并重新绘图
    def set_bound():
        try:
            left_bound_ = float(left_bound.get())
            right_bound_ = float(right_bound.get())
            left_peak_ = float(left_peak.get())
            right_peak_ = float(right_peak.get())

            if left_bound_ < left_peak_ < right_peak_ < right_bound_:
                engine.set_bound(left_bound_, right_bound_, left_peak_, right_peak_)
                res = engine.get_detail_data()
                frame_init()
                fig, axs = figure.plot(frame_fig)
                plot.pre_plot(axs, res)
            else:
                mb.showerror("设定参数大小顺序不正确")
        except ValueError as e:
            mb.showerror("请输入正确格式的数字")

    # 重置图像
    def reset_fig():
        frame_init()
        fig, axs = figure.plot(frame_fig)
        if engine.get_raw_index() >= 0:
            plot.raw_plot(axs, engine.get_raw())
        else:
            plot.pre_all_data(axs, engine.get_all_data(), 1)

        result.delete(1.0, END)
        result.insert(END, "重置完毕")

    # 拟合曲线背景
    def optimize_cur():
        try:
            level_ = int(level.get())
            data = engine.optimize_bg(level_)
            frame_init()
            fig, axs = figure.plot(frame_fig)
            plot.cur_plot(axs, data)
        except ValueError as e:
            mb.showerror("请输入正确格式的值")

    # 获得直线背景
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
                fig, axs = figure.plot(frame_fig)
                plot.cur_plot(axs, data)

        except ValueError:
            mb.showerror("请输入正确格式的值")

    # 积分得到结果并输出
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

    # 输出所选周期数据
    def output_data():
        writer = asksaveasfile(filetypes=[("TXT", ".txt")])
        engine.output(writer)

    def egg(event):
        mb.showinfo("Surprise!", "Author:Nan Hang\n"
                                 "Github:https://github.com/nanharder/calECSA")

    # -------------控件区-------------------------------------------------------
    # 初始化engine实例
    engine = Engine()

    # --------------文件读取区域--------------------------------------------------
    # 数据分割符选择, 默认为","
    Label(root, text="请选择数据的分隔符:").place(relx=0.1, rely=0.015, relheight=0.035)
    sep = StringVar()
    Radiobutton(root, text="逗号", value=",", command=set_sep, variable=sep)\
        .place(relx=0.4, rely=0.015, relheight=0.035)
    Radiobutton(root, text="空格", value=" ", command=set_sep, variable=sep)\
        .place(relx=0.6, rely=0.015, relheight=0.035)
    sep.set(",")

    # 选择文件加载数据
    Label(root, text="请选择原始数据文件:").place(relx=0.1, rely=0.06, relheight=0.035)

    path = StringVar()
    Entry(root, textvariable=path).place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.038)
    Button(root, text="文件选择", cursor="hand2", command=select_path)\
        .place(relx=0.1, rely=0.15, relwidth=0.2)
    Button(root, text="加载数据", cursor="hand2", command=load_data_from_file)\
        .place(relx=0.4, rely=0.15, relwidth=0.2)
    Button(root, text="重置图像", cursor="hand2", command=reset_fig)\
        .place(relx=0.7, rely=0.15, relwidth=0.2)

    # --------------数据处理区域--------------------------------------------------
    # 选择要处理的数据的周期
    data_index = StringVar()
    Label(root, text="数据周期编号:").place(relx=0.1, rely=0.2225, relheight=0.038)
    Entry(root, textvariable=data_index)\
        .place(relx=0.3, rely=0.225, relwidth=0.08, relheight=0.038)
    Button(root, text="预览数据", cursor="hand2", command=pre_select_data)\
        .place(relx=0.4, rely=0.225, relwidth=0.2)
    Button(root, text="选择数据", cursor="hand2", command=select_data)\
        .place(relx=0.7, rely=0.225, relwidth=0.2)

    # 设置峰和背景的范围
    left_bound = StringVar()
    right_bound = StringVar()
    left_peak = StringVar()
    right_peak = StringVar()

    Label(root, text=" 背景左边界:").place(relx=0.1, rely=0.3, relheight=0.038)
    Entry(root, textvariable=left_bound).place(relx=0.3, rely=0.3, relwidth=0.15, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bound('left_bound'))\
        .place(relx=0.47, rely=0.3, relwidth=0.05, relheight=0.038)

    Label(root, text=" 背景右边界:").place(relx=0.55, rely=0.3, relheight=0.038)
    Entry(root, textvariable=right_bound).place(relx=0.75, rely=0.3, relwidth=0.15, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bound('right_bound'))\
        .place(relx=0.92, rely=0.3, relwidth=0.05, relheight=0.038)

    Label(root, text=" 积分峰左边界:").place(relx=0.1, rely=0.35, relheight=0.038)
    Entry(root, textvariable=left_peak).place(relx=0.3, rely=0.35, relwidth=0.15, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bound('left_peak'))\
        .place(relx=0.47, rely=0.35, relwidth=0.05, relheight=0.038)

    Label(root, text=" 积分峰右边界:").place(relx=0.55, rely=0.35, relheight=0.038)
    Entry(root, textvariable=right_peak).place(relx=0.75, rely=0.35, relwidth=0.15, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bound('right_peak'))\
        .place(relx=0.92, rely=0.35, relwidth=0.05, relheight=0.038)

    Button(root, text="应用边界", cursor="hand2", command=set_bound)\
        .place(relx=0.1, rely=0.41, relwidth=0.2)

    # 拟合背景的数据
    # 曲线拟合模式
    level = StringVar()
    Label(root, text=" 背景曲线拟合级数:").place(relx=0.1, rely=0.5, relheight=0.038)
    Entry(root, textvariable=level).place(relx=0.35, rely=0.5, relwidth=0.13, relheight=0.038)

    Button(root, text="拟合背景", cursor="hand2", command=optimize_cur)\
        .place(relx=0.6, rely=0.5, relwidth=0.2)

    # 两点直线拟合模式
    x1 = StringVar()
    y1 = StringVar()
    x2 = StringVar()
    y2 = StringVar()

    Label(root, text=" x1:").place(relx=0.1, rely=0.55, relheight=0.038)
    Entry(root, textvariable=x1).place(relx=0.18, rely=0.55, relwidth=0.1, relheight=0.038)
    Label(root, text=" y1:").place(relx=0.3, rely=0.55, relheight=0.038)
    Entry(root, textvariable=y1).place(relx=0.38, rely=0.55, relwidth=0.1, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bg('x1', 'y1'))\
        .place(relx=0.5, rely=0.55, relwidth=0.05, relheight=0.038)

    Label(root, text=" x2:").place(relx=0.1, rely=0.6, relheight=0.038)
    Entry(root, textvariable=x2).place(relx=0.18, rely=0.6, relwidth=0.1, relheight=0.038)
    Label(root, text=" y2:").place(relx=0.3, rely=0.6, relheight=0.038)
    Entry(root, textvariable=y2).place(relx=0.38, rely=0.6, relwidth=0.1, relheight=0.038)
    Button(root, text="◎", cursor="hand2", command=gen_find_bg('x2', 'y2'))\
        .place(relx=0.5, rely=0.6, relwidth=0.05, relheight=0.038)

    btn_select_data = Button(root, text="直线背景", cursor="hand2", command=line_background)
    btn_select_data.place(relx=0.6, rely=0.575, relwidth=0.2)

    # ---------计算峰面积并进行处理------------------------------------------------------------
    formula = StringVar()
    Label(root, text=" 积分结果处理:").place(relx=0.1, rely=0.65, relheight=0.038)
    Entry(root, textvariable=formula).place(relx=0.3, rely=0.65, relwidth=0.35, relheight=0.038)
    Button(root, text="积分", cursor="hand2", command=intergrate)\
        .place(relx=0.7, rely=0.65, relwidth=0.2)

    result = Text(root)
    result.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

    Button(root, text="输出数据", cursor="hand2", command=output_data)\
        .place(relx=0.1, rely=0.92, relwidth=0.2)

    # 彩蛋环节
    win.bind("<Control-n>", egg)
