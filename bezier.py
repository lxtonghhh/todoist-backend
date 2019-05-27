import math


# params:
# input_arr: 8个数的数组（4个点）: x0,y0,x1,y1...
# base: 基准坐标轴，默认为x
# point_interval: 每次取点的间隔，默认为1
#
# output:
# 点的数组，形式同input_arr
def bezier(input_arr, base='x', point_interval=1):
    xs, ys = [], []
    for i, num in enumerate(input_arr):
        if i % 2 == 0:
            xs.append(num)
        else:
            ys.append(num)
    ts = []
    if base == 'x':
        num_max, num_min = peaks(xs)
        i = 0
        for i in range(int(num_min), int(num_max + 1), point_interval):
            for t in t_solve(xs, i):
                if -1e-15 <= t <= 1:
                    ts.append(t)
        if i != num_max:
            for t in t_solve(xs, num_max):
                if -1e-15 <= t <= 1:
                    ts.append(t)
    else:
        num_max, num_min = peaks(ys)
        i = 0
        print(num_min, num_max)
        for i in range(int(num_min), int(num_max + 1), point_interval):
            for t in t_solve(ys, i):
                if -1e-15 <= t <= 1:
                    ts.append(t)
                # print(t)
            # print(i)
        if i != num_max:
            for t in t_solve(ys, num_max):
                if -1e-15 <= t <= 1:
                    ts.append(t)
    ts.sort()
    out_points = []
    if ts[0] > 1e-3:
        out_points.append(input_arr[0])
        out_points.append(input_arr[1])
    for t in ts:
        out_points.append(func(xs, t))
        out_points.append(func(ys, t))
    if ts[-1] < 1 - 1e-3:
        out_points.append(input_arr[-2])
        out_points.append(input_arr[-1])
    return out_points


def func(nums, t):
    return nums[0] * (1 - t) ** 3 + 3 * nums[1] * t * (1 - t) ** 2 + 3 * nums[2] * t ** 2 * (
            1 - t) + nums[3] * t ** 3


def peaks(nums):
    a = 3 * (nums[3] - 3 * nums[2] + 3 * nums[1] - nums[0])
    b = 2 * (3 * nums[2] - 6 * nums[1] + 3 * nums[0])
    c = 3 * nums[1] - 3 * nums[0]
    op = b * b - 4 * a * c
    if a == 0:
        if b == 0:
            return max(nums[0], nums[3]), min(nums[0], nums[3])
        else:
            return max(nums[0], nums[3], func(nums, -c / b) if 0 <= -c / b <= 1 else nums[0]), \
                   min(nums[0], nums[3], func(nums, -c / b) if 0 <= -c / b <= 1 else nums[0])
    if op < 0:
        return max(nums[0], nums[3]), min(nums[0], nums[3])
    if op == 0:
        return max(nums[0], nums[3],
                   func(nums, -b / (2 * a)) if 0 <= -b / (2 * a) <= 1 else nums[0]), \
               min(nums[0], nums[3],
                   func(nums, -b / (2 * a)) if 0 <= -b / (2 * a) <= 1 else nums[0])
    op_ = pow(op, 0.5)

    return max(nums[0], nums[3],
               func(nums, (-b - op_) / (2 * a)) if 0 <= (-b - op_) / (2 * a) <= 1 else nums[0],
               func(nums, (-b + op_) / (2 * a)) if 0 <= (-b + op_) / (2 * a) <= 1 else nums[0]), \
           min(nums[0], nums[3],
               func(nums, (-b - op_) / (2 * a)) if 0 <= (-b - op_) / (2 * a) <= 1 else nums[0],
               func(nums, (-b + op_) / (2 * a)) if 0 <= (-b + op_) / (2 * a) <= 1 else nums[0])


def cubic_root(n):
    root = abs(pow(n, 1 / 3))
    if root * n < 0:
        root = -root
    return root


def t_solve(nums, Bt):
    a = -nums[0] + 3 * nums[1] - 3 * nums[2] + nums[3]
    b = -6 * nums[1] + 3 * nums[2] + 3 * nums[0]
    c = 3 * nums[1] - 3 * nums[0]
    d = nums[0] - Bt
    if a == 0:
        a = b
        b = c
        c = d
        op = b * b - 4 * a * c
        if op < 0:
            return []
        if a == 0:
            return [(Bt - c) / b]
        if op == 0:
            return [-b / (2 * a)]
        op_ = pow(op, 0.5)
        return [(-b - op_) / (2 * a), (-b + op_) / (2 * a)]
    A = b * b - 3 * a * c
    B = b * c - 9 * a * d
    C = c * c - 3 * b * d
    delta = B * B - 4 * A * C
    if A == 0 and B == 0:
        if c == 0:
            return [0]
        else:
            return [-c / b]
    if delta > 0:
        op = pow(delta, 0.5)
        Y1 = A * b + 3 * a * ((-B + op) / 2)
        Y2 = A * b + 3 * a * ((-B - op) / 2)
        return [(-b - (cubic_root(Y1) + cubic_root(Y2))) / (3 * a)]
    if delta == 0:
        K = B / A
        return [-b / a + K, -K / 2]
    if delta < 0:
        root_A = pow(A, 0.5)
        T = (2 * A * b - 3 * a * B) / (2 * A * root_A)
        theta = math.acos(T)
        return [(-b - 2 * root_A * math.cos(theta / 3)) / (3 * a),
                (-b + root_A * (math.cos(theta / 3) + pow(3, 0.5) * math.sin(theta / 3))) / (3 * a),
                (-b + root_A * (math.cos(theta / 3) - pow(3, 0.5) * math.sin(theta / 3))) / (3 * a)]


def derivative(nums, t):
    a = 3 * (nums[3] - 3 * nums[2] + 3 * nums[1] - nums[0])
    b = 2 * (3 * nums[2] - 6 * nums[1] + 3 * nums[0])
    c = 3 * nums[1] - 3 * nums[0]
    return a * t ** 2 + b * t + c


def bezier_dense(input_arr, point_interval=1):
    xs, ys = [], []
    for i, num in enumerate(input_arr):
        if i % 2 == 0:
            xs.append(num)
        else:
            ys.append(num)
    appro_len = 0.0
    for i in range(100):
        appro_len += derivative(xs, i / 100)
        appro_len += derivative(ys, i / 100)
    appro_len /= 10000 / point_interval  # 根号2 * 100
    # point_num = appro_len / point_interval
    out_point = [input_arr[0], input_arr[1]]
    t = 0.0
    while t < 1:
        delta_t = appro_len / pow((derivative(xs, t) ** 2) + (derivative(ys, t) ** 2), 0.5)
        t += delta_t
        print(t)
        if t > 1:
            break
        out_point.append(func(xs, t))
        out_point.append(func(ys, t))
    # for i in range(1, int(point_num)):
    #     out_point.append(func(xs, i / point_num))
    #     out_point.append(func(ys, i / point_num))
    out_point.append(input_arr[-2])
    out_point.append(input_arr[-1])
    return out_point
def get_nodes(nodes, _type, point_interval=10):
    if _type == '7':
        base = 'x'
    else:
        base = 'y'
    output = bezier(nodes, base=base, point_interval=point_interval)
    x = []
    y = []
    for i in range(len(output) // 2):
        x.append(output[2 * i])
        y.append(output[2 * i + 1])
    nodes = [dict(x=x, y=y) for x, y in zip(x, y)]
    print('After bezier:', nodes)
    return nodes

if __name__ == '__main__':
    get_nodes(nodes=[657.0661636363636, 313.81301851463206, 704.6216966942147, 372.06688181818174, 847.4208988556422, 505.79202099024525, 957.5137388429754, 715], _type='1', point_interval=1)
