from numpy import polyfit, poly1d, arange, trapz


class Engine(object):

    def __init__(self):
        self.file_source = ''
        self.separator = ','
        self.left_bound = -1
        self.right_bound = -1
        self.left_peak = -1
        self.right_peak = -1

        self.raw_data = Pair()
        self.peak_data = Pair()
        self.bg_data = Pair()
        self.bg_curve = Pair()
        self.formula = 'x'
        self.peak_area = 0
        self.final_res = 0

    def clear(self):
        self.file_source = ''
        self.left_bound = -1
        self.right_bound = -1
        self.left_peak = -1
        self.right_peak = -1

        self.raw_data = Pair()
        self.peak_data = Pair()
        self.bg_data = Pair()
        self.bg_curve = Pair()
        self.peak_area = 0
        self.final_res = 0

    def set_filepath(self, path):
        self.file_source = path

    def get_filepath(self):
        return self.file_source

    def get_xmin(self):
        return min(self.raw_data.get_xcol())

    def get_xmax(self):
        return max(self.raw_data.get_xcol())

    def load_data(self):
        with open(self.file_source, 'r+', encoding='utf-8') as f:
            nums = [i[:-1].split(self.separator) for i in f.readlines()]
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
        x = [float(i[0].strip()) for i in nums[index:]]
        y = [float(i[1].strip()) for i in nums[index:]]
        step = x[1] - x[0]
        if step > 0:
            num = int((max(x) - x[0]) / step + 1)
        else:
            num = int((x[0] - min(x)) / abs(step) + 1)
        self.raw_data.set_cols(x[:num], y[:num])

    def set_bound(self, l_bound, r_bound, l_peak, r_peak):
        self.left_peak = l_peak
        self.right_peak = r_peak
        self.left_bound = l_bound
        self.right_bound = r_bound

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

    def optimize_bg(self, level):
        parameter = polyfit(self.bg_data.get_xcol(), self.bg_data.get_ycol(), level)
        func = poly1d(parameter)
        x_peak = self.peak_data.get_xcol()
        x_opt = arange(x_peak[0], x_peak[-1], x_peak[1] - x_peak[0])
        y_opt = func(x_opt)
        self.bg_curve.set_cols(x_opt, y_opt)

        return self.bg_data.get_cols() + self.peak_data.get_cols() + self.bg_curve.get_cols()

    def get_raw(self):
        return self.raw_data

    def get_formula(self):
        return self.formula

    def set_formula(self, formula):
        self.formula = formula

    def integrate(self):
        if self.peak_data.size() == 0 or self.bg_curve.size() == 0:
            return []
        else:
            area1 = trapz(self.peak_data.get_ycol(), self.peak_data.get_xcol())
            area2 = trapz(self.bg_curve.get_ycol(), self.bg_curve.get_xcol())
            self.peak_area = abs(area1 - area2)
            x = self.peak_area
            try:
                self.final_res = eval(self.formula)
            except Exception as e:
                self.formula = 'x'
                self.final_res = eval(self.formula)
            return area1, area2, self.peak_area, self.formula, self.final_res


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
