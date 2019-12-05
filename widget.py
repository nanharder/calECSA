"""
负责程序控件的创建和布局
"""
from tkinter import *
from tkinter.filedialog import askopenfilename
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
        path_ = askopenfilename()
        path.set(path_)

    def load_data_from_file():
        nonlocal frame_fig
        filepath = path.get()
        engine.clear()
        engine.set_filepath(filepath)
        if filepath is None or len(filepath) == 0:
            mb.showerror("提示：路径不能为空")
        elif not os.path.exists(filepath):
            mb.showerror("目标文件不存在")
        else:
            engine.load_data()

            left_bound.set(str(engine.get_xmin()))
            right_bound.set(str(engine.get_xmax()))
            left_peak.set(str(engine.get_xmin()))
            right_peak.set(str(engine.get_xmax()))
            level.set(str(1))
            formula.set(engine.get_formula())

            frame_init()
            axs = figure.plot(frame_fig)
            plot.raw_plot(axs, engine.get_raw())

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

    def intergrate():
        formula_ = formula.get()
        engine.set_formula(formula_)
        res = engine.integrate()
        result.delete(1.0, END)
        result.insert(END, "峰积分结果:  %.4g \n" % res[0])
        result.insert(END, "背景积分结果: %.4g \n" % res[1])
        result.insert(END, "峰最终面积:  %.4g \n" % res[2])
        result.insert(END, "面积处理公式： %s \n" % res[3])
        result.insert(END, "最终结果： %.4g \n" % res[4])

    def test():
        result.insert(END, "%s \n" % (win.winfo_geometry()))

    # -------------控件区----------------

    """
    加载数据并显示原始数据图像
    """
    label = Label(root, text="请选择原始数据文件:")
    label.place(relx=0.1, rely=0.1)

    engine = Engine()
    path = StringVar()
    entry = Entry(root, textvariable=path)
    entry.place(relx=0.1, rely=0.15, relwidth=0.8)
    button = Button(root, text="文件选择", cursor="hand2", command=select_path)
    button.place(relx=0.1, rely=0.2, relwidth=0.2)

    btn_draw = Button(root, text="加载数据", cursor="hand2", command=load_data_from_file)
    btn_draw.place(relx=0.4, rely=0.2, relwidth=0.2)

    btn_reset = Button(root, text="重置图像", cursor="hand2", command=reset_fig)
    btn_reset.place(relx=0.7, rely=0.2, relwidth=0.2)

    """
    设置取点范围
    """
    left_bound = StringVar()
    right_bound = StringVar()
    left_peak = StringVar()
    right_peak = StringVar()

    Label(root, text="背景左边界：").place(relx=0.1, rely=0.3)
    entry1 = Entry(root, textvariable=left_bound)
    entry1.place(relx=0.3, rely=0.3, relwidth=0.15)
    Label(root, text="背景右边界：").place(relx=0.55, rely=0.3)
    entry2 = Entry(root, textvariable=right_bound)
    entry2.place(relx=0.75, rely=0.3, relwidth=0.15)

    Label(root, text="积分峰左边界：").place(relx=0.1, rely=0.35)
    entry3 = Entry(root, textvariable=left_peak)
    entry3.place(relx=0.3, rely=0.35, relwidth=0.15)
    Label(root, text="积分峰右边界：").place(relx=0.55, rely=0.35)
    entry4 = Entry(root, textvariable=right_peak)
    entry4.place(relx=0.75, rely=0.35, relwidth=0.15)

    btn_pre = Button(root, text="应用边界", cursor="hand2", command=set_bound)
    btn_pre.place(relx=0.1, rely=0.4, relwidth=0.2)

    level = StringVar()
    Label(root, text="背景曲线拟合级数：").place(relx=0.1, rely=0.5)
    entry5 = Entry(root, textvariable=level)
    entry5.place(relx=0.4, rely=0.5, relwidth=0.08)

    btn_optimize = Button(root, text="拟合背景", cursor="hand2", command=optimize_cur)
    btn_optimize.place(relx=0.55, rely=0.5, relwidth=0.2)

    formula = StringVar()
    Label(root, text="积分结果处理：").place(relx=0.1, rely=0.58)
    entry6 = Entry(root, textvariable=formula)
    entry6.place(relx=0.3, rely=0.58, relwidth=0.35)
    btn_inter = Button(root, text="积分", cursor="hand2", command=intergrate)
    btn_inter.place(relx=0.7, rely=0.58, relwidth=0.2)

    result = Text(root)
    result.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.2)

    '''
    test = Button(root, text="输出窗体大小", command=test)
    test.place(relx=0.1, rely=0.92)
    '''
