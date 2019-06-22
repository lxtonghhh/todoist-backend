from common.compiler.tree import create_plot

node_map = {
    "s": "S",
    "translation_unit": "TU",
    "external_declaration": "ED",
    "func_declaration": "FD",
    "declarator":"Do",
    "declaration": "Di",
    "declaration_specifiers": "DS",
    "init_declarator": "InD",
    "initializer": "I",
    "assignment_expression": "AE",
    "initializer_list": "IL",
    "declaration_list": "DL",
    "compound_stmt": "CS",
    "type_specifier": "TS",
    "parameter_type_list": "PTL",
    "parameter_list": "PL",
    "parameter_declaration": "PD",
    "stmt": "S",
    "iter_stmt": "IS",
    "selection_stmt": "SS",
    "expression_stmt": "ES",
    "stmt_list": "SL",
    "primary_expression": "PE",
    "constant": "C",
    "unary_op": "UO",
    "assignment_op": "AO",
    "compare_op": "CO",
    "factor_expression":"FE",
    "expression": "E",
    "unary_expression": "UE",
    "null": "$"
}


def create_node(node, value, sons):
    """

    :param node: Node
    :param value: string
    :param sons: string->Node
    :return:
    """

    if value == "<s>":
        n_sons = [Node(value=s, sons=[]) for s in sons]
        node = Node(value=value, sons=n_sons)
    else:
        if value[0] == "<":
            # 非终结符
            n_sons = [Node(value=s, sons=[]) for s in sons]
            node.sons = n_sons
        else:
            # 终结符
            n_sons = []
            node.sons = n_sons
            node.value = value

    return dict(node=node, sons=n_sons)


class Node(object):
    def __init__(self, value, sons):

        self.value = value
        self.sons = sons

    @property
    def short_value(self):
        if self.value[0] == "<":
            return node_map[self.value[1:-1]]
        else:
            return self.value

    def convert_to_dict(self, d=None, index=-1):

        if index == -1:
            next_d = {}
            i = 0
            for son in self.sons:
                son.convert_to_dict(d=next_d, index=i)
                i += 1

            return {self.short_value: next_d}
        else:
            next_d = {}
            i = 0
            for son in self.sons:
                son.convert_to_dict(d=next_d, index=i)
                i += 1
            if self.sons:
                d[index] = {self.short_value: next_d}
            else:
                d[index] = self.short_value

    def __repr__(self):
        return "{0}".format(self.value)


if __name__ == "__main__":
    s_sons = [Node(value="<son" + str(i + 1) + ">", sons=[]) for i in range(3)]
    ss_son = Node(value="<son" + str(4) + ">", sons=[Node(value="<sson" + str(0) + ">", sons=[])])
    s_sons.append(ss_son)
    start = Node(value="<s>", sons=s_sons)
    print(start.convert_to_dict())
    create_plot(start.convert_to_dict())


class Production(object):
    def __init__(self, left, right, select=None):
        self.left = left
        self.right = right
        self.select = set()

    def __str__(self):
        return self.left + ' -> ' + str(self.right) + ' Select: ' + str(self.select)


class Symbol(object):
    def __init__(self, symbol, first_set=None, follow_set=None, sym_type='N'):
        self.symbol = symbol
        self.first_set = first_set
        self.follow_set = follow_set
        self.sym_type = sym_type
        self.is_nullable = False
        self.attr = {}
        self.father = None
        self.children = []
        self.lexical_value = None

    def __str__(self):
        return self.symbol + ' Derive_empty:' + str(self.is_nullable) + ' First:' + str(
            self.first_set) + ' Follow:' + str(self.follow_set)

    def is_terminal(self):
        return self.sym_type == 'T'


class Entry(object):
    def __init__(self, type, length, name):
        self.type = type
        self.length = length
        self.name = name

    def __str__(self):
        return self.name + ' ' + self.type + ' ' + str(self.length)
