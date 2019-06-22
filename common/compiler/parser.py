#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common.compiler.lexer2 as lexer2
import base64
from common.compiler.util import Production, Symbol, create_plot, create_node

TERMINAL_SET = set()

NON_TERMINAL_SET = set()

SYMBOL_DICT = {}

PRODUCTION_LIST = []

PARSING_TABLE = {}

SYMBOL_STACK = []

SYMBOL_TABLE = {}

LAST_STACK_TOP_SYMBOL = None


def symbol_for_str(string):
    return SYMBOL_DICT[string]


def is_terminal(string):
    return string in TERMINAL_SET


def syntax_error(msg, line=None, row=None):
    if line is None:
        line = lexer2.current_line + 1
    if row is None:
        row = lexer2.current_row + 1
    print(str(line) + ':' + str(row) + ' Syntax error: ' + msg)
    return (str(line) + ':' + str(row) + ' Syntax error: ' + msg)


def prepare_symbols_and_productions():
    f = open('grammar.txt', 'r')
    lines = f.readlines()
    terminal = False
    production = False
    for l in lines:
        if l.strip() == '*terminals':
            terminal = True
            production = False
            continue
        if l.strip() == '*productions':
            terminal = False
            production = True
            continue
        if l.strip() == '*end':
            break
        if terminal:
            # print("terminal ", l.strip())
            TERMINAL_SET.update([l.strip()])
        if production:
            left = l.split('::=')[0].strip()
            NON_TERMINAL_SET.update([left])
            # print("production ", left)
            try:
                right = l.split('::=')[1].strip()
                if right == '':
                    raise IndexError
                p = Production(left, right.split(' '))
            except IndexError:
                p = Production(left, ['null'])

            PRODUCTION_LIST.append(p)

    for s in TERMINAL_SET:
        sym = Symbol(s, sym_type='T')
        SYMBOL_DICT[s] = sym

    for s in NON_TERMINAL_SET:
        sym = Symbol(s, sym_type='N')
        SYMBOL_DICT[s] = sym
    # _show_SYMBOL_DICT()
    # _show_PRODUCTION_LIST()


def _show_SYMBOL_DICT():
    print("===SYMBOL_DICT===")
    for v in SYMBOL_DICT.values():
        print(v)


def _show_PRODUCTION_LIST():
    print("===PRODUCTION_LIST===")
    for p in PRODUCTION_LIST:
        print(p)


def get_nullable():
    """
    Calculate and mark non-terminals found that is nullable(can derive null).
    We do this first, so we can use the result when calculating First and Follow.
    """
    changes = True
    while changes:
        changes = False
        for p in PRODUCTION_LIST:
            if not symbol_for_str(p.left).is_nullable:
                if p.right[0] == 'null':
                    symbol_for_str(p.left).is_nullable = True
                    changes = True
                    continue
                else:
                    right_is_nullable = symbol_for_str(p.right[0]).is_nullable
                    # For X -> Y1 ... YN, Nullable(X) = Nullable(Y1) &
                    # Nullable(Y2) ... & Nullable(YN)
                    for r in p.right[1:]:
                        if r.startswith('P'):
                            continue
                        right_is_nullable = right_is_nullable & symbol_for_str(
                            r).is_nullable

                    if right_is_nullable:
                        changes = True
                        symbol_for_str(p.left).is_nullable = True


def get_first():
    """
    Calculate First set of each symbol.
    """
    for s in TERMINAL_SET:
        # For each terminal, initialize First with itself.
        sym = SYMBOL_DICT[s]
        sym.first_set = set([s])

    for s in NON_TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        if sym.is_nullable:
            sym.first_set = set(['null'])
        else:
            sym.first_set = set()

    while True:
        first_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if p.right[0] == 'null':
                sym_left.first_set.update(set(['null']))
                continue
            previous_first_set = set(sym_left.first_set)

            for s in p.right:
                # For X -> Y..., First(X) = First(X) U First(Y)
                sym_right = symbol_for_str(s)
                sym_left.first_set.update(sym_right.first_set)
                # For X -> Y1 Y2 ... Yi-1 , if Y1...Yi-1 is all nullable
                # Then First(X) = First(X) U First(Y1) U First(Y2) ...
                if sym_right.is_nullable:
                    continue
                else:
                    break

            if previous_first_set != sym_left.first_set:
                first_set_is_stable = False

        if first_set_is_stable:
            break


def get_follow():
    """
    Calculate Follow set of each symbol.
    """
    for s in NON_TERMINAL_SET:
        sym = symbol_for_str(s)
        sym.follow_set = set()

    symbol_for_str('<s>').follow_set.update(set(['#']))

    while True:
        follow_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if sym_left.is_terminal():
                continue
            for s in p.right:
                if s == 'null':
                    continue
                if s.startswith('P'):
                    continue
                if symbol_for_str(s).is_terminal():
                    continue
                current_symbol = symbol_for_str(s)
                previous_follow_set = set(current_symbol.follow_set)
                next_is_nullable = True
                for s2 in p.right[p.right.index(s) + 1:]:
                    if s2.startswith('P'):
                        continue
                    # For X -> sYt, Follow(Y) = Follow(Y) U First(t)
                    next_symbol = symbol_for_str(s2)
                    current_symbol.follow_set.update(next_symbol.first_set)
                    if next_symbol.is_nullable:
                        continue
                    else:
                        next_is_nullable = False
                        break
                if next_is_nullable:
                    # For X -> sYt, if t is nullable, Follow(Y) = Follow(Y) U
                    # Follow(X)
                    current_symbol.follow_set.update(sym_left.follow_set)

                if current_symbol.follow_set != previous_follow_set:
                    follow_set_is_stable = False

        if follow_set_is_stable:
            break


def get_select():
    """
    Calculate Select set for each production.
    """
    while True:
        select_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            previous_select = set(p.select)
            if p.right[0] == 'null':
                # For A -> a, if a is null, Select(i) = Follow(A)
                p.select.update(sym_left.follow_set)
                continue
            sym_right = symbol_for_str(p.right[0])
            # Otherwise, Select(i) = First(a)
            p.select.update(sym_right.first_set)
            # If a is nullable, Select(i) = First(a) U Follow(A)
            if sym_right.is_nullable:
                p.select.update(sym_right.first_set.union(sym_left.follow_set))
            if previous_select != p.select:
                select_set_is_stable = False
        if select_set_is_stable:
            break


def get_parsing_table():
    """
    Calculate parsing table.
    """
    global PARSING_TABLE
    for non_terminal in NON_TERMINAL_SET:
        PARSING_TABLE[non_terminal] = {}
        for p in PRODUCTION_LIST:
            if non_terminal == p.left:
                for symbol in p.select:
                    PARSING_TABLE[non_terminal][symbol] = p
        # Calculate SYNC
        for symbol in symbol_for_str(non_terminal).follow_set:
            if is_terminal(symbol):
                try:
                    p = PARSING_TABLE[non_terminal][symbol]
                except KeyError:
                    PARSING_TABLE[non_terminal][symbol] = 'SYNC'

        for symbol in symbol_for_str(non_terminal).first_set:
            if is_terminal(symbol):
                try:
                    p = PARSING_TABLE[non_terminal][symbol]
                except KeyError:
                    PARSING_TABLE[non_terminal][symbol] = 'SYNC'

    # prettyprint_parsing_table()


def prettyprint_parsing_table():
    for non_terminal in PARSING_TABLE.keys():
        symbol_to_production_list = []
        for symbol in PARSING_TABLE[non_terminal]:
            p = PARSING_TABLE[non_terminal][symbol]
            symbol_to_production = str(symbol) + ':' + str(p)
            symbol_to_production_list.append(symbol_to_production)

        print(non_terminal)
        print(symbol_to_production_list)


def print_symbol_table():
    for t in SYMBOL_TABLE:
        print(t)


def next_token():
    def _convert_to_tuple(r):
        """
        dict(token=op, code=get_token_code(op), value='-', address='-')
        (token,value,code,address)
        """
        if not r:
            return r
        else:
            return (r["token"], r["value"], r["code"], r["address"],)

    def _convert_to_dict(r):
        """
        dict(token=op, code=get_token_code(op), value='-', address='-')
        (token,value,code,address)
        """
        if not r:
            return r
        else:
            return dict(token=r[0], code=r[2], value=r[1], address='-')

    r = lexer2.scanner()
    while r is None:
        r = lexer2.scanner()
    print("next_token: ", _convert_to_dict(r), "\n")
    return r


def prepare_grammar():
    prepare_symbols_and_productions()
    get_nullable()
    get_first()
    get_follow()
    get_select()
    get_parsing_table()
    # prettyprint_parsing_table()


def do_parsing():
    SYMBOL_STACK.append('#')
    SYMBOL_STACK.append('<s>')
    # 语法树
    node_rank_list = []
    current_node = None
    start_node = None
    # 报错信息
    error_lines = []

    token_tuple = next_token()
    productions = open('productions.txt', 'w')
    stack = open('stack.txt', 'w')
    while len(SYMBOL_STACK) > 0:
        stack_top_symbol = SYMBOL_STACK[-1]
        current_token = token_tuple[0]
        if current_token == 'OP' or current_token == 'SEP':
            current_token = token_tuple[1]

        if current_token == 'SCANEOF':
            current_token = '#'

        if stack_top_symbol == 'null':
            # 语法树
            print("current_node--> ", current_node, "\n")
            r = create_node(node=current_node, value=stack_top_symbol, sons=[])
            current_node = node_rank_list.pop(0) if len(node_rank_list) > 0 else None

            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            continue

        if stack_top_symbol == '#':
            break

        if not is_terminal(stack_top_symbol):
            try:

                p = PARSING_TABLE[stack_top_symbol][current_token]

                print("current_node--> ", current_node)
                print("node_rank_list--> ", node_rank_list)
                print("stack_top_symbol--> ", stack_top_symbol, "|| current_token--> ", current_token, )
                print("production--> ", p, "\n")
                r = create_node(node=current_node, value=stack_top_symbol, sons=p.right)
                # print(r['node'].convert_to_dict(),"\n")

                if stack_top_symbol == "<s>":
                    start_node = r['node']
                node_rank_list = r['sons'] + node_rank_list
                current_node = node_rank_list.pop(0)


            except KeyError:
                # Stack top symbol unmatched, ignore it
                error_msg = syntax_error('unmatched')
                error_lines.append(error_msg)
                try:
                    token_tuple = next_token()
                except:
                    break
                continue

            if p == 'SYNC':
                # SYNC recognized, pop Stack
                syntax_error("sync symbol, recovering")
                LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
                stack.write(str(SYMBOL_STACK) + '\n')
                productions.write(str(p) + '\n')
                continue

            stack.write(str(SYMBOL_STACK) + '\n')
            productions.write(str(p) + '\n')
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            SYMBOL_STACK.extend(reversed(p.right))

        else:
            # 语法树
            print("current_node--> ", current_node, "完成终结符规约")
            print("node_rank_list--> ", node_rank_list)
            print("stack_top_symbol--> ", stack_top_symbol, "|| current_token--> ", current_token, "\n")
            if stack_top_symbol in ["ID", "VOID", "INT", "CHAR", "FLOAT", "LONG", "DOUBLE", "SHORT", "STRING_LITERAL"]:
                value = str(token_tuple[0]) + ":" + str(token_tuple[1])
            else:
                value = stack_top_symbol
            r = create_node(node=current_node, value=value, sons=[])
            # print(r['node'].convert_to_dict(),"\n")
            current_node = node_rank_list.pop(0)

            SYMBOL_STACK.pop()
            token_tuple = next_token()
    # print(start_node.convert_to_dict())
    create_plot(start_node.convert_to_dict())
    productions.close()
    stack.close()

    return error_lines


def main():
    prepare_grammar()
    lexer2.read_source_file('input2.c')
    do_parsing()


def server_main_parser(input_str):
    global TERMINAL_SET, NON_TERMINAL_SET, SYMBOL_DICT, PRODUCTION_LIST, PARSING_TABLE, SYMBOL_STACK, SYMBOL_TABLE, LAST_STACK_TOP_SYMBOL
    TERMINAL_SET = set()

    NON_TERMINAL_SET = set()

    SYMBOL_DICT = {}

    PRODUCTION_LIST = []

    PARSING_TABLE = {}

    SYMBOL_STACK = []

    SYMBOL_TABLE = {}

    LAST_STACK_TOP_SYMBOL = None
    prepare_grammar()
    output_lines = ["======语法分析输出======"]
    lexer2.read_source_str(input_str)
    output_lines += do_parsing()
    with open("tree.png", "rb") as f:
        base64_data = base64.b64encode(f.read())
        print(str(base64_data))

    return (output_lines, str(base64_data, encoding = "utf-8"))


if __name__ == '__main__':
    print(server_main_parser(input_str="int main(){int a}"))
    # main()
