import matplotlib.pyplot as plt
import matplotlib
# pylint: disable=redefined-outer-name

# 定义文本框和箭头格式
decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def retrieve_tree(i):
    list_of_trees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                     {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                     ]
    return list_of_trees[i]


def get_num_leafs(mytree):
    '''
    获取叶子节点数
    '''
    num_leafs = 0
    first_str = list(mytree.keys())[0]
    second_dict = mytree[first_str]

    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1

    return num_leafs


def get_tree_depth(mytree):
    '''
    获取树的深度
    '''
    max_depth = 0
    first_str = list(mytree.keys())[0]
    second_dict = mytree[first_str]

    for key in second_dict.keys():
        # 如果子节点是字典类型，则该节点也是一个判断节点，需要递归调用
        # get_tree_depth()函数
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1

        if this_depth > max_depth:
            max_depth = this_depth

    return max_depth


def plot_node(ax, node_txt, center_ptr, parent_ptr, node_type):
    '''
        绘制带箭头的注解
    '''
    ax.annotate(node_txt, xy=parent_ptr, xycoords='axes fraction',
                xytext=center_ptr, textcoords='axes fraction',
                va="center", ha="center", bbox=node_type, arrowprops=arrow_args)


def plot_mid_text(ax, center_ptr, parent_ptr, txt):
    '''
    在父子节点间填充文本信息
    '''
    x_mid = (parent_ptr[0] - center_ptr[0]) / 2.0 + center_ptr[0]
    y_mid = (parent_ptr[1] - center_ptr[1]) / 2.0 + center_ptr[1]

    ax.text(x_mid, y_mid, txt)


def plot_tree(ax, mytree, parent_ptr, node_txt):
    '''
    绘制决策树
    '''
    # 计算宽度
    num_leafs = get_num_leafs(mytree)

    first_str = list(mytree.keys())[0]
    center_ptr = (plot_tree.x_off + (1.0 + float(num_leafs)) / 2.0 / plot_tree.total_width, plot_tree.y_off)

    # 绘制特征值，并计算父节点和子节点的中心位置，添加标签信息
    plot_mid_text(ax, center_ptr, parent_ptr, node_txt)
    plot_node(ax, first_str, center_ptr, parent_ptr, decision_node)

    second_dict = mytree[first_str]
    # 采用的自顶向下的绘图，需要依次递减Y坐标
    plot_tree.y_off -= 1.0 / plot_tree.total_depth

    # 遍历子节点，如果是叶子节点，则绘制叶子节点，否则，递归调用plot_tree()
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            plot_tree(ax, second_dict[key], center_ptr, str(key))
        else:
            plot_tree.x_off += 1.0 / plot_tree.total_width
            plot_mid_text(ax, (plot_tree.x_off, plot_tree.y_off), center_ptr, str(key))
            plot_node(ax, second_dict[key], (plot_tree.x_off, plot_tree.y_off), center_ptr, leaf_node)

    # 在绘制完所有子节点之后，需要增加Y的偏移
    plot_tree.y_off += 1.0 / plot_tree.total_depth


def create_plot(in_tree):
    #sb lib
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 20)

    ax_props = dict(xticks=[], yticks=[])
    ax = plt.subplot(111, frameon=False, **ax_props)
    plot_tree.total_width = float(get_num_leafs(in_tree))
    plot_tree.total_depth = float(get_tree_depth(in_tree))
    plot_tree.x_off = -0.5 / plot_tree.total_width
    plot_tree.y_off = 1.0
    plot_tree(ax, in_tree, (0.5, 1.0), "")
    #     plot_node(ax, "a decision node", (0.5, 0.1), (0.1, 0.5), decision_node)
    #     plot_node(ax, "a leaf node", (0.8, 0.1), (0.3, 0.8), leaf_node)
    plt.show()
    fig.savefig('tree.png', dpi=100)


if __name__ == '__main__':
    #     create_plot()
    mytree = retrieve_tree(1)
    mytree['no surfacing'][2] = "maybe"
    mytree['no surfacing'][3] = {"test":{"0":"no","1":"111","2":{"test":{"0":"no","1":"111"}}}}
    print(mytree)
    create_plot(mytree)
