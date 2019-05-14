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
        for i in range(int(num_min), int(num_max + 1), point_interval):
            for t in t_solve(ys, i):
                if -1e-15 <= t <= 1:
                    ts.append(t)
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
            return max(nums[0], nums[3], func(nums, -c / b)), \
                   min(nums[0], nums[3], func(nums, -c / b))
    if op < 0:
        return max(nums[0], nums[3]), min(nums[0], nums[3])
    if op == 0:
        return max(nums[0], nums[3], func(nums, -b / (2 * a))), \
               min(nums[0], nums[3], func(nums, -b / (2 * a)))
    op_ = pow(op, 0.5)
    return max(nums[0], nums[3], func(nums, (-b - op_) / (2 * a)),
               func(nums, (-b + op_) / (2 * a))), \
           min(nums[0], nums[3], func(nums, (-b - op_) / (2 * a)), func(nums, (-b + op_) / (2 * a)))


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
    get_nodes(nodes=[337, 389, 271.2679682729529, 419.56380412322596, 162.21986434067054,
                     419.54920947506906, 5, 435], _type='1', point_interval=1)
