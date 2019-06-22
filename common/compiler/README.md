## 如何运行？

#### 执行环境 python3.6.5

将test目录下实例数据复制到文件根目录的input.txt中

执行 python lexer.py

会输出结果到 output.txt 和table_in_one,json

### 1.输出单词，以二元式形式

```
======词法分析输出======
( 编码code: 1  ,地址address:- )
( 编码code: 32 ,地址address:0x1d62900 )
( 编码code: 28 ,地址address:- )
```

(关键字的编码，-）
(标识符的编码，字面量的指针(指针的地址)）
(整形常数的编码,p)
(字符串型常数的编码,p)
(运算符的编码，-）
(界符的编码，-）

### 2.非法处理

```
From Line7 Char6 missing terminating "
```

非法字符报错
非法组合报错

### 3.符号表管理

```
======标识符符号表======
( token:a,地址address:0x1d62900 )
( token:myFunction,地址address:0x39b2f48 )
( token:b,地址address:0x1d68a00 )
( token:c,地址address:0x1d5b740 )
( token:d,地址address:0x1d5ba80 )
======整数符号表======
( 值value:1,地址address:0x5a71e310 )
( 值value:10,地址address:0x5a71e3a0 )
======字符串符号表======
( token:中文,地址address:0x39b6a10 )
```

输出每个符号的地址和值。
标识符：地址、字面量(abc)
整数：地址、值
字符串：地址、字面量（"abc"）

#### 符号表使用hash表实现



```
TOKEN_DICT = {'func': 0, 'int': 1, 'print': 2, 'return': 3, 'continue': 4, 'if': 5, 'then': 6, 'else': 7, 'fi': 8,
              'while': 9, 'do': 10, 'done': 11, '': 12, '(': 13, ')': 14, ',': 15, ';': 16, '{': 17, '}': 18, '+': 19,
              '-': 20, '*': 21, '%': 22, '/': 23, '>': 24, '<': 25, '>=': 26, '<=': 27, '=': 28, '==': 29, '!=': 30,
              '!': 31, 'IDENTIFIER': 32, 'INTEGER': 33, 'FLOAT': 34, 'TEXT': 35}

# 标识符表:字面量-内存地址(类型)映射
IDENTIFIER_DICT = {}
# 常数表:字面量-内存地址(类型)映射
CONSTANT_DICT = {}
```

### 4.现场3个问题
