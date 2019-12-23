"""
储存数据的对象,具有处理数据的方法
"""

from numpy import polyfit, poly1d, arange, trapz


class Engine(object):

    def __init__(self):
        # 数据来源
        self.file_source = ''
        # 分隔符
        self.separator = ','
        # 背景与峰的边界
        self.left_bound = -1
        self.right_bound = -1
        self.left_peak = -1
        self.right_peak = -1

        # 全部读取的数据
        self.all_data = []
        # 处理数据的周期
        self.raw_data_index = -1
        # 处理的周期的数据
        self.raw_data = Pair()
        # 分割出的峰的数据
        self.peak_data = Pair()
        # 分割出的背景的数据
        self.bg_data = Pair()
        # 拟合得到的背景的数据
        self.bg_curve = Pair()

        # 对积分结果处理的公式,积分结果为x
        self.formula = 'x'
        # 积分结果
        self.peak_area = 0
        # 积分结果经公式处理后的最终值
        self.final_res = 0

    # 文件重载时清理已储存的数据
    def clear(self):
        self.file_source = ''
        self.left_bound = -1
        self.right_bound = -1
        self.left_peak = -1
        self.right_peak = -1

        self.all_data = []
        self.raw_data_index = 0
        self.raw_data = Pair()
        self.peak_data = Pair()
        self.bg_data = Pair()
        self.bg_curve = Pair()
        self.peak_area = 0
        self.final_res = 0

    ##############################
    # 数据读取和处理的方法
    ##############################

    # 从文件中读取数据
    def load_data(self):
        # 初步读取数据,根据分隔符的不同,读取方式不同
        with open(self.file_source, 'r+', encoding='utf-8') as f:
            if self.separator == ",":
                nums = [i[:-1].split(self.separator) for i in f.readlines()]
            else:
                nums = [i[:-1].split() for i in f.readlines()]

        # 去除文件头不符合规范的数据
        index = 0
        while index < len(nums):
            if len(nums[index]) == 2:
                try:
                    float(nums[index][0].strip())
                    float(nums[index][1].strip())
                    break
                except ValueError as e:
                    pass
            index += 1

        # 得到全部数据的x, y
        x = [float(i[0].strip()) for i in nums[index:]]
        y = [float(i[1].strip()) for i in nums[index:]]

        # 根据x的最大最小值分割周期
        min_x = min(x)
        max_x = max(x)
        left = 0
        right = 1
        while right < len(x):
            if x[right] == min_x or x[right] == max_x:
                pair = Pair()
                pair.set_cols(x[left:right], y[left:right])
                self.all_data.append(pair)
                left = right
            right += 1

        # 如果还有多余数据也要加入进来
        if right - left > 1:
            pair = Pair()
            pair.set_cols(x[left:right], y[left:right])
            self.all_data.append(pair)

    # 设置所要处理的周期数据
    def set_raw_index(self, index):
        tar = index - 1
        # 不符合规范的数据返回false, 设置成功返回True
        if tar < 0 or tar > len(self.all_data):
            return False
        else:
            self.raw_data_index = tar
            self.raw_data = self.all_data[tar]
            return True

    # 设置背景和峰的边界并返回背景和峰的数据
    def set_bound(self, l_bound, r_bound, l_peak, r_peak):
        self.left_peak = l_peak
        self.right_peak = r_peak
        self.left_bound = l_bound
        self.right_bound = r_bound

        # 通过设定的边界分割数据
        x_back = []
        y_back = []
        x_peak = []
        y_peak = []
        x_raw = self.raw_data.get_xcol()
        y_raw = self.raw_data.get_ycol()
        for i in range(len(x_raw)):
            if l_peak < x_raw[i] < r_peak:
                x_peak.append(x_raw[i])
                y_peak.append(y_raw[i])
            elif l_bound < x_raw[i] < r_bound:
                x_back.append(x_raw[i])
                y_back.append(y_raw[i])
        self.bg_data.set_cols(x_back, y_back)
        self.peak_data.set_cols(x_peak, y_peak)
        return x_back, y_back, x_peak, y_peak

    # 根据提供的背景数据和背景的级数拟合出背景的曲线
    # 返回[背景, 峰, 拟合背景]数据
    def bg_helper(self, x_bg, y_bg, level):
        parameter = polyfit(x_bg, y_bg, level)
        func = poly1d(parameter)
        x_peak = self.peak_data.get_xcol()
        x_opt = arange(x_peak[0], x_peak[-1], x_peak[1] - x_peak[0])
        y_opt = func(x_opt)
        self.bg_curve.set_cols(x_opt, y_opt)

        return self.bg_data.get_cols() + self.peak_data.get_cols() + self.bg_curve.get_cols()

    # 根据背景拟合
    def optimize_bg(self, level):
        return self.bg_helper(self.bg_data.get_xcol(), self.bg_data.get_ycol(), level)

    # 根据两点拟合直线背景
    def optimize_line(self, x1, y1, x2, y2):
        return self.bg_helper([x1, x2], [y1, y2], 1)

    # 积分方法
    def integrate(self):
        # 判断所需数据是否为空
        if self.peak_data.size() == 0 or self.bg_curve.size() == 0:
            return []
        else:
            # 对峰和背景积分并取差值
            area1 = trapz(self.peak_data.get_ycol(), self.peak_data.get_xcol())
            area2 = trapz(self.bg_curve.get_ycol(), self.bg_curve.get_xcol())
            self.peak_area = abs(area1 - area2)
            x = self.peak_area

            # 执行公式处理积分结果,若出现错误,按默认公式处理
            try:
                self.final_res = eval(self.formula)
            except Exception as e:
                self.formula = 'x'
                self.final_res = eval(self.formula)
            return area1, area2, self.peak_area, self.formula, self.final_res

    # 输出积分所在周期数据
    def output(self, writer):
        index = self.get_raw_index() // 2
        cv1 = self.all_data[index * 2]
        cv2 = self.all_data[index * 2 + 1]

        out_x = cv1.get_xcol() + cv2.get_xcol()
        out_y = cv1.get_ycol() + cv2.get_ycol()

        i = 0
        while i < len(out_x):
            writer.write('%g, %g\n' % (out_x[i], out_y[i]))
            i += 1
        writer.close()

    #############################
    #      getter and setter
    #############################

    def set_filepath(self, path):
        self.file_source = path

    def get_filepath(self):
        return self.file_source

    def get_xmin(self):
        return min(self.raw_data.get_xcol())

    def get_xmax(self):
        return max(self.raw_data.get_xcol())

    def set_sep(self, sep):
        self.separator = sep

    def get_all_data(self):
        return self.all_data

    def get_all_data_size(self):
        return len(self.all_data)

    def get_raw(self):
        return self.raw_data

    def get_raw_index(self):
        return self.raw_data_index

    def get_formula(self):
        return self.formula

    def set_formula(self, formula):
        self.formula = formula

    def get_detail_data(self):
        return self.bg_data.get_xcol(), self.bg_data.get_ycol(), self.peak_data.get_xcol(), self.peak_data.get_ycol()


# 用于储存x,y数据列
class Pair(object):

    def __init__(self):
        self.xcol = []
        self.ycol = []

    def set_cols(self, xcol, ycol):
        self.xcol = xcol
        self.ycol = ycol

    def get_xcol(self):
        return self.xcol

    def get_ycol(self):
        return self.ycol

    def get_cols(self):
        return self.xcol, self.ycol

    def size(self):
        return len(self.get_xcol())
