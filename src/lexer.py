# 词法分析
from src.function import if_num, if_name, have_name, printf, get_word
# 一些判断函数和字符分割函数放在同级文件function.py中
import sys
import os

sys.path.append(os.pardir)  # 为了导入父目录的文件而进行的设定

# 运算符表
y_list = {
    "+",
    "-",
    "*",
    "/",
    "<",
    "<=",
    ">",
    ">=",
    "=",
    "==",
    "!=",
    "^",
    ",",
    "&",
    "&&",
    "|",
    "||",
    "%",
    "~",
    "<<",
    ">>",
    "!"}
# 分隔符表
f_list = {";", "(", ")", "[", "]", "{", "}", ".",
          ":", "\"", "#", "\'", "\\", "?"}
# 关键字表
k_list = {
    "auto",
    "break",
    "case",
    "const",
    "continue",
    "default",
    "do",
    "else",
    "enum",
    "extern",
    "for",
    "goto",
    "if",
    "register",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "volatile",
    "while",
    "printf"}

Cmp = ["<", ">", "==", "!=", ">=", "<="]

Type = {"int", "float", "char", "double", "void", "long", "unsigned", "string"}
type_flag = ""
# 括号配对判断
brackets_cp = {'{': '}', '[': ']', '(': ')'}


# 词法分析器输出对象
# 成员变量：输出的单词表，源代码中的分隔符表,运算符表,变量表,关键字表
# 一个方法，将源代码字符切割并存入对应表中
# 对象创建实例需要传入filename参数，默认为test.c
class word_list():
    def __init__(self, filename='test.c'):
        self.word_list = []  # 输出单词列表
        self.separator_list = []  # 分隔符
        self.operator_list = []  # 运算符
        self.name_list = []  # 变量
        self.key_word_table = []  # 关键字
        self.string_list = []
        self.flag = True  # 源代码是否正确标识
        self.error = ''

        # get_word函数将源代码切割
        self.create_table(get_word(filename))

    # 创建各个表
    def create_table(self, in_words):
        name_id = 0
        brackets_list = []  # 存储括号并判断是否完整匹配
        char_flag = False
        str_flag = False
        string_list = []
        strings = ""
        chars = ""
        for word in in_words:
            w = word['word']
            line = word['line']
            if w == '"':
                # 被双引号包裹的即为字符串，若str_flag为False，则置为True，进行字符串分析
                if not str_flag:
                    str_flag = True
                else:
                    str_flag = False
                    self.word_list.append(
                        {'line': line, 'type': 'TEXT', 'word': strings})
                    self.string_list.append(strings)
                    strings = ""
                # self.word_list.append({'line':line, 'type':w, 'word':w})
                continue
            # 判断是否为字符串
            if str_flag:
                strings += w
                continue
            # 被单引号包裹即为字符，进行字符分析
            if w == "'":
                if not char_flag:
                    char_flag = True
                else:
                    char_flag = False
                    self.word_list.append(
                        {'line': line, 'type': 'CHAR', 'word': chars})
                    chars = ""
                continue
            if char_flag:
                chars += w
                continue
            # 识别关键字
            if w in k_list:
                self.key_word_table.append(
                    {'line': line, 'type': 'keyword', 'word': w})
                self.word_list.append({'line': line, 'type': w, 'word': w})
            elif w in Cmp:
                self.word_list.append({'line': line, 'type': "Cmp", 'word': w})
            # 识别类型
            elif w in Type:
                type_flag = w
                self.key_word_table.append(
                    {'line': line, 'type': 'type', 'word': w})
                self.word_list.append(
                    {'line': line, 'type': 'type', 'word': w})
            # 识别运算符
            elif w in y_list:
                self.operator_list.append(
                    {'line': line, 'type': 'operator', 'word': w})
                self.word_list.append({'line': line, 'type': w, 'word': w})
            # 识别分隔符
            elif w in f_list:
                if w in brackets_cp.values() or w in brackets_cp.keys():
                    # 左括号入栈
                    if w in brackets_cp.keys():
                        brackets_list.append({'brackets': w, 'line': line})
                    # 右括号判断是否匹配并出栈
                    elif w == brackets_cp[brackets_list[-1]['brackets']]:
                        brackets_list.pop()
                    # 识别错误则返回错误位置并退出
                    else:
                        # print("第" + str(line) + "行的' " + w + " '无法匹配，无法通过编译，请检查代码正确性！")
                        self.flag = False
                        self.error = "第" + \
                            str(line) + "行的' " + w + " '无法匹配，无法通过编译，请检查代码正确性！"
                        return
                self.separator_list.append(
                    {'line': line, 'type': 'separator', 'word': w})
                self.word_list.append({'line': line, 'type': w, 'word': w})
            # 其他字符处理
            else:
                # 调用正则表达式判断是否是数字
                if if_num(w):
                    self.word_list.append(
                        {'line': line, 'type': 'number', 'word': w})
                # 如果是变量名要判断是否已经存在
                elif if_name(w):
                    if have_name(self.name_list, w):
                        self.word_list.append(
                            {'line': line, 'type': 'name', 'word': w, 'id': name_id})
                    else:
                        self.name_list.append(
                            {'line': line, 'id': name_id, 'word': 0.0, 'name': w, 'flag': type_flag})
                        self.word_list.append(
                            {'line': line, 'type': 'name', 'word': w, 'id': name_id})
                        name_id += 1
                else:
                    # print("第" + str(line) + "行的变量名' " + w + " '不可识别，无法通过编译，请检查代码正确性！")
                    self.flag = False
                    self.error = "第" + \
                        str(line) + "行的变量名' " + w + " '不可识别，无法通过编译，请检查代码正确性！"
                    return
        if brackets_list:
            # print("第" + str(brackets_list[0]['line']) + "行的' " + brackets_list[0]['brackets'] + " '无法匹配，无法通过编译，请检查代码正确性！")
            self.flag = False
            self.error = "第" + \
                str(brackets_list[0]['line']) + "行的' " + brackets_list[0]['brackets'] + " '无法匹配，无法通过编译，请检查代码正确性！"
            return


def get_lexer():
    try:
        filename = 'code/upload.c'
        w_list = word_list(filename)
        result = ''
        # sys.stdout = result
        if w_list.flag:
            # print("\n输出字符串如下")
            # print(w_list.word_list)
            # print("\n\n输出变量表如下\n")
            # print(w_list.name_list)
            #
            result += "字符串:\n"
            for word in w_list.word_list:
                result += '{'
                for key, value in word.items():
                    result += key + ': ' + str(value) + '  '
                result += '}\n'
            result += "====================\n变量表:\n"
            for name in w_list.name_list:
                result += '{'
                for key, value in name.items():
                    result += key + ': ' + str(value) + '  '
                result += '}\n'
        else:
            result = w_list.error
        return result
    except BaseException:
        return "程序错误，请检查代码"


if __name__ == '__main__':
    filename = input("请输入要编译的.c文件:")
    if filename == '':
        filename = '../code/upload.c'
    w_list = word_list(filename)
    if w_list.flag:
        print("\n输出字符串如下")
        printf(w_list.word_list)
        print("\n\n输出变量表如下\n")
        printf(w_list.name_list)
