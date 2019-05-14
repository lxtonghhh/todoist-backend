import sys, json

KEYWORD_LIST = ["func", "int", "print", "return", "continue", "if", "then", "else", "fi", "while", "do", "done", ""]
SEPARATOR_LIST = ['(', ')', ',', ';', '{', '}']
OPERATOR_LIST = ['+', '-', '*', '%', '/', '>', '<', '>=', '<=', '=', '==', '!=', '!']
# 符号表:字面量-编码映射
TOKEN_DICT = {'func': 0, 'int': 1, 'print': 2, 'return': 3, 'continue': 4, 'if': 5, 'then': 6, 'else': 7, 'fi': 8,
              'while': 9, 'do': 10, 'done': 11, '': 12, '(': 13, ')': 14, ',': 15, ';': 16, '{': 17, '}': 18, '+': 19,
              '-': 20, '*': 21, '%': 22, '/': 23, '>': 24, '<': 25, '>=': 26, '<=': 27, '=': 28, '==': 29, '!=': 30,
              '!': 31, 'IDENTIFIER': 32, 'INTEGER': 33, 'FLOAT': 34, 'TEXT': 35}

# 标识符表:字面量-内存地址(类型)映射
IDENTIFIER_DICT = {}
# 常数表:字面量-内存地址(类型)映射
CONSTANT_DICT = {}
# 助记符-编码映射
IDENTIFIER = 'IDENTIFIER'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
TEXT = 'TEXT'
SIGH_TO_INT = {}

is_keyword = lambda s: s in KEYWORD_LIST
is_separator = lambda s: s in SEPARATOR_LIST
is_operator = lambda s: s in OPERATOR_LIST
get_token_code = lambda s: TOKEN_DICT.get(s, None)

char_now = -1
line_now = 0
input_lines = []


class LexicalError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '词法错误：{0}'.format(self.msg)


class ScanEndError(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return '词法分析结束'.format(self.msg)


def get_token_dict():
    """
    获得全局符号表
    :return:
    """
    global TOKEN_DICT
    TOKEN_DICT = {token_name: code for code, token_name in enumerate(KEYWORD_LIST + SEPARATOR_LIST + OPERATOR_LIST)}
    TOKEN_DICT["IDENTIFIER"] = len(TOKEN_DICT)
    TOKEN_DICT["INTEGER"] = len(TOKEN_DICT)
    TOKEN_DICT["FLOAT"] = len(TOKEN_DICT)
    TOKEN_DICT["TEXT"] = len(TOKEN_DICT)


def getchar() -> str:
    """
    光标前进1 返回当前字符
    :return:
    """

    global char_now
    global line_now
    char_now += 1

    if char_now == len(input_lines[line_now]):
        line_now += 1
        char_now = 0

    if line_now == len(input_lines):
        return 'SCANEOF'
    else:
        return input_lines[line_now][char_now]


def ungetchar() -> str:
    """
    光标后退1 返回当前字符
    :return:
    """
    global char_now
    global line_now
    char_now = char_now - 1
    if char_now < 0:
        # 回到上一行
        line_now = line_now - 1
        if line_now < 0:
            # todo 是否报错
            return 'SCANEOF'
        else:
            char_now = len(input_lines[line_now]) - 1
    else:
        pass
    return input_lines[line_now][char_now]


def read_file(filename: str):
    global input_lines
    with open(filename, 'r', encoding='utf-8') as f:
        input_lines = f.readlines()


def scanner():
    c = getchar()
    if c == 'SCANEOF':
        raise ScanEndError()
    if c.strip() == '':
        return None
    if c.isalpha() or c == '_':
        # 关键字
        # 标识符规则:只能以"_"或者字母开头 可包含数字
        string = ''
        while c.isalpha() or c.isdigit() or c == '_':
            string += c
            c = getchar()
            if c == 'SCANEOF':
                break
        ungetchar()
        if is_keyword(string):
            return dict(token=string, code=get_token_code(string), value='-', address='-')
        else:
            # 遇到重复标识符取第一次
            if IDENTIFIER_DICT.get(string, None):
                pass
            else:
                IDENTIFIER_DICT[string] = dict(type=IDENTIFIER, code=get_token_code(IDENTIFIER))
            # todo 返回内存地址
            return dict(token=IDENTIFIER, code=get_token_code(IDENTIFIER), value=string, address=hex(id(string)))

    if c.isdigit():
        # 整型常量
        int_value = 0
        while c.isdigit():
            int_value = int_value * 10 + int(c)
            c = getchar()

        if c != '.':
            ungetchar()

            CONSTANT_DICT[int_value] = dict(type=INTEGER, code=get_token_code(INTEGER))
            # todo 返回内存地址
            return dict(token=INTEGER, code=get_token_code(INTEGER), value=int_value, address=hex(id(int_value)))

        # 浮点数常量
        float_value = str(int_value) + '.'
        c = getchar()
        while c.isdigit():
            float_value += c
            c = getchar()
        ungetchar()
        float_value = float(float_value)

        CONSTANT_DICT[float_value] = dict(type=FLOAT, code=get_token_code(FLOAT))
        # todo 返回内存地址
        return dict(token=FLOAT, code=get_token_code(FLOAT), value=float_value, address=hex(id(float_value)))

    if c == '\"':
        # 字符串常量
        str_literal = ''
        text_start_line = line_now
        text_start_char = char_now

        current_char = getchar()
        while current_char != '\"':
            str_literal += current_char
            current_char = getchar()
            if current_char == 'SCANEOF':
                raise LexicalError(
                    msg='From Line{0} Char{1} missing terminating \"'.format(text_start_line, text_start_char))

        CONSTANT_DICT[str_literal] = dict(type=TEXT, code=get_token_code(TEXT))
        # todo 返回内存地址
        return dict(token=TEXT, code=get_token_code(TEXT), value=str_literal, address=hex(id(str_literal)))

    if is_separator(c):
        # 界符
        sep = c
        return dict(token=sep, code=get_token_code(sep), value='-', address='-')

    if is_operator(c):
        # 运算符
        op = c
        next_c = getchar()
        if is_operator(next_c):
            op += next_c
            if op not in OPERATOR_LIST:
                raise LexicalError(
                    msg='Wrong Combination: ' + (op) + ' in Line {0} Char {1}'.format(line_now + 1,
                                                                                      char_now + 1))
            else:
                pass
        else:
            ungetchar()

        return dict(token=op, code=get_token_code(op), value='-', address='-')

    raise LexicalError(msg='Unknown Character: ' + c + ' in Line {0} Char {1}'.format(line_now + 1, char_now + 1))


FORMAT_TOKEN_CODE_VALUE = "( token:{token},编码code: {code},值value:{value} ,地址address:{address})\n"
FORMAT_CODE_ADDRESS = "( 编码code: {code},地址address:{address} )\n"

FORMAT_TOKEN_ADDRESS = "( token:{token},地址address:{address} )\n"
FORMAT_VALUE_ADDRESS = "( 值value:{value},地址address:{address} )\n"


def main(mode, file_name):
    # file_name = sys.argv[1]

    read_file(file_name)
    output_lines = []
    output_lines.append("======词法分析输出======\n")
    try:
        while True:
            res = scanner()
            if not res:
                continue
            else:
                print(res)
                if mode == 'teacher':
                    output_lines.append(
                        FORMAT_CODE_ADDRESS.format(code=str(res['code']).ljust(3, " "), address=str(res['address'])))
                if mode == 'my':
                    print(res['address'])
                    output_lines.append(
                        FORMAT_TOKEN_CODE_VALUE.format(token=res['token'].ljust(10, " "),
                                                       code=str(res['code']).ljust(3, " "),
                                                       value=res['value']
                                                       , address=str(res['address'])))
    except (LexicalError, ScanEndError) as e:
        print(e.msg)
        output_lines.append(e.msg + "\n")

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

    table = {**TOKEN_DICT, **IDENTIFIER_DICT, **CONSTANT_DICT}
    with open('table_in_one.json', 'w', encoding='utf-8') as f:
        json.dump(table, f)
    """
    目前阶段只需要做到:
    输出每个符号的地址和值。
    标识符：地址、字面量(abc)
    整数：地址、值
    字符串：地址、字面量（"abc"）
    """

    table_lines = []
    table_lines.append("======标识符符号表======\n")
    for key, value in IDENTIFIER_DICT.items():
        table_lines.append(FORMAT_TOKEN_ADDRESS.format(token=key, address=hex(id(key))))
    table_lines.append("======整数符号表======\n")
    for key, value in CONSTANT_DICT.items():
        if isinstance(key, int):
            table_lines.append(FORMAT_VALUE_ADDRESS.format(value=key, address=hex(id(key))))
    table_lines.append("======字符串符号表======\n")
    for key, value in CONSTANT_DICT.items():
        if isinstance(key, str):
            table_lines.append(FORMAT_TOKEN_ADDRESS.format(token=key, address=hex(id(key))))
    with open('output.txt', 'a', encoding='utf-8') as f:
        f.writelines(table_lines)


def server_main(input_str, mode='my'):
    global input_lines
    input_lines = input_str.split("\n")
    output_lines = []
    output_lines.append("======词法分析输出======\n")
    try:
        while True:
            res = scanner()
            if not res:
                continue
            else:
                print(res)
                if mode == 'teacher':
                    output_lines.append(
                        FORMAT_CODE_ADDRESS.format(code=str(res['code']).ljust(3, " "), address=str(res['address'])))
                if mode == 'my':
                    print(res['address'])
                    output_lines.append(
                        FORMAT_TOKEN_CODE_VALUE.format(token=res['token'].ljust(10, " "),
                                                       code=str(res['code']).ljust(3, " "),
                                                       value=res['value']
                                                       , address=str(res['address'])))
    except (LexicalError, ScanEndError) as e:
        print(e.msg)
        output_lines.append(e.msg + "\n")

    """
    目前阶段只需要做到:
    输出每个符号的地址和值。
    标识符：地址、字面量(abc)
    整数：地址、值
    字符串：地址、字面量（"abc"）
    """

    output_lines.append("======标识符符号表======\n")
    for key, value in IDENTIFIER_DICT.items():
        output_lines.append(FORMAT_TOKEN_ADDRESS.format(token=key, address=hex(id(key))))
    output_lines.append("======整数符号表======\n")
    for key, value in CONSTANT_DICT.items():
        if isinstance(key, int):
            output_lines.append(FORMAT_VALUE_ADDRESS.format(value=key, address=hex(id(key))))
    output_lines.append("======字符串符号表======\n")
    for key, value in CONSTANT_DICT.items():
        if isinstance(key, str):
            output_lines.append(FORMAT_TOKEN_ADDRESS.format(token=key, address=hex(id(key))))
    return output_lines


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(mode='my', file_name="input.txt")
    else:
        if sys.argv[1] == 'teacher':
            main(mode='teacher', file_name="input.txt")
        elif sys.argv[1] == 'my':
            main(mode='my', file_name="input.txt")
        else:
            print("Wrong Command!")

if __name__ == '__main__':
    get_token_dict()
    print(TOKEN_DICT)
