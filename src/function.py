# 环境：python3.6
# 词法分析器-getToken
import re

# 运算符表
y_list = {"+", "-", "*", "/", "<", "<=", ">", ">=", "=", "==", "!=", "^", ",", "&", "&&", "|", "||", "%", "~", "<<",
          ">>", "!"}
# 分隔符表
f_list = {";", "(", ")", "[", "]", "{", "}", ".", ":", "\"", "#", "\'", "\\", "?"}
# 关键字表
k_list = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern",
    "float", "for", "goto", "if", "else", "int", "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "printf"
}  ###新增else 关键字
# 比较关键字
Cmp = ["<", ">", "==", "!=", "<=", ">="]


# 正则表达式判断是否为数字
def if_num(int_word):
    if re.match("^([0-9]{1,}[.][0-9]*)$", int_word) or re.match("^([0-9]{1,})$", int_word) == None:
        return False
    else:
        return True


# 判断是否为为变量名
def if_name(int_word):
    if re.match("[a-zA-Z_][a-zA-Z0-9_]*", int_word) == None:
        return False
    else:
        return True


# 判断变量名是否已存在
def have_name(name_list, name):
    for n in name_list:
        if name == n['name']:
            return True
    return False


# list的换行输出
def printf(lists):
    for l in lists:
        print(l)


# 提取参数
def extract_args(literal):
    # 以左括号进行分割
    literal = literal.lstrip('(')
    # 以右括号进行分割
    literal = literal.rstrip(')')
    # 去掉空格
    literal = literal.replace(' ', '')
    # 此处用到了 正则表达式的预断言功能
    # <= 表示从左往右扫描 所以 (?<=,)?(\w+) 表示 从该位置向左看是否与逗号匹配且匹配0/1个括号表达式
    # = 表示从右往左扫描【默认方式】 所以(\w+)(?=,)?表示 从该位置向右看是否与逗号匹配且匹配0/1个括号表达式
    # 该句工作的具体流程是先整体进行匹配 即把满足(?<=,)?(\w+)(?=,)? 格式的str 匹配出来
    # 然后将符合括号表达式要求的匹配出来 (\w+)代表要提取得参数
    args_pattern = re.compile(r'(?<=,)?(\w+)(?=,)?')
    args_list = re.findall(args_pattern, literal)
    return args_list


# 宏定义预处理
# 处理格式 #define macro_name macro_string
def macros(filename):
    f = open(filename, 'r+', encoding='UTF-8')
    # 先逐行读取
    lines = f.readlines()
    # print("lines",lines)
    # 记录访问过的行，防止在词法分析时再次分析
    line_num = 1
    # 定义文本 用于后续的宏定义替换 并初始化
    original_str = ""
    # 是否遇到#define
    flag = 0
    for line in lines:
        # 按行进行分词 用于判断#define 关键字
        words = list(line.split())
        # print(words)
        # 去除空行的影响 即words[0] 不存在的问题
        if len(words) and re.match(r'#define', words[0]):
            # 再将词合并 用空格隔开
            literals = ' '.join(words)
            # print("literals:",literals)
            # 去除 #define 对提取macro_name 的影响
            literals = literals.replace("define", "").replace("#", "").strip()
            # print("literals:",literals)
            # macro_name 的正则表达式 \b表示单词开头 可以将括号表达式的前面匹配出来 如：add(x,y) 匹配add
            marco_name_pattern = re.compile(r'\b\w+(?=[(\s])')
            # 提取macro_name
            result = re.search(marco_name_pattern, literals)
            if result is None:
                return None
            # 若result有结果则为list格式
            # 获得macros name
            macro_name = result.group(0)
            # print("macro_name:",macro_name)
            # 获取匹配剩余的字符串
            rest_literals = literals[len(macro_name):]
            # print("rest_literals:",rest_literals)
            # 判断macro_name 后面是否有括号表达式 有则说明为函数替换 需要进行单独处理
            if rest_literals[0] == '(':
                # 匹配macro_string 括号表达式
                defns_pattern = re.compile(r'(?<=[)]).+')
                result = re.search(defns_pattern, rest_literals)
                if result is None:
                    # 为空说明 有误
                    return None
                defns = result.group(0)
            else:
                # 无括号表达式 为正常的字符替换
                defns = rest_literals
            # print("defns:",defns)
            # 获取匹配剩余的字符串
            rest_literals = rest_literals[:len(rest_literals) - len(defns)]
            args_list = None
            if not rest_literals == '':
                # 剩余字符串不为空 则进行参数提取
                args_list = extract_args(rest_literals)
            
            # 进行匹配pattern构造
            
            arg_str = macro_name
            if args_list is not None:
                # 补上括号
                arg_str += '\('
                for i in range(len(args_list)):
                    if i < len(args_list) - 1:
                        # 补上参数匹配符
                        arg_str += '\w+,[\s]*'
                    else:
                        arg_str += '\w+'
                arg_str += '\)'
            
            # 在文本中进行对符合patern 的串进行匹配
            
            # 为构造pattern 补上边界
            macro_pattern = r'\b%s[^\w]' % arg_str
            # 文本拼接
            if not flag:
                original_str = ''.join(lines)
            # print("original_str:",original_str)
            # 匹配
            result = re.findall(macro_pattern, original_str)
            # print("result:",result)
            if len(result) > 0:
                for node in result:
                    macro_defns = defns
                    node_str = node[len(macro_name) + 1:len(node) - 1]
                    # 被替换串的参数提取
                    parms_list = extract_args(node_str)
                    for k in range(len(parms_list)):
                        macro_defs_parm_pattern = re.compile(r'\b%s\b' % args_list[k])
                        # 对应参数替换
                        macro_defns = re.sub(macro_defs_parm_pattern, '%s' % parms_list[k], macro_defns)
                    # 格式化
                    replaces_str = ' {}{}'.format(macro_defns, node[-1])
                    result = re.sub(macro_pattern, replaces_str, original_str, 1)
                    # 增量更新文本
                    original_str = result
                flag = 1
            line_num += 1
        elif len(words) and not re.match(r"#define", words[0]):
            break
        elif not len(words):
            line_num += 1
    # 若出现#define 则origin str 不为空 则对文本惊醒list 化 便于词法分析
    if original_str is not "":
        # print(original_str)
        lines = list(original_str.split('\n'))
    # print("lines:", lines)
    return lines, line_num


# 分割并获取文本单词
# 返回值为列表out_words
# 列表元素{'word':ws, 'line':line_num}分别对应单词与所在行号
def get_word(filename):
    # print("预处理开始")
    lines, line_num_in = macros(filename)  # 预处理
    # print(lines, line_num_in)
    global f_list
    out_words = []
    # 先逐行读取，并记录行号
    line_num = 1
    # 判断是否含有注释块的标识
    pass_block = False
    for line in lines:
        if line_num >= line_num_in:
            words = list(line.split())  # python自带分词 默认以空格、换行和字表符分割
            # print("word:", words)
            for w in words:
                # 去除注释
                if '*/' in w:
                    pass_block = False  # 碰到注释块结尾，继续分析
                    continue
                if '//' in w or pass_block:
                    break  # 碰到单条注释开始，终止分析
                if '/*' in w:
                    pass_block = True
                    break  # 碰到注释块开始，终止分析
                # 分析单词
                if w in Cmp:
                    out_words.append({'word': w, 'line': line_num})  # 如果属于比较关键词，记录该单词和单词所在行号
                    continue
                
                ws = w  # 做一份拷贝
                for a in w:
                    if a in f_list or a in y_list:
                        # index为分隔符的位置，将被分隔符或运算符隔开的单词提取 如int main() 中的main()
                        index = ws.find(a)
                        if index != 0:
                            # 存储单词与该单词的所在行号，方便报错定位
                            out_words.append({'word': ws[0:index], 'line': line_num})  # 储存分隔符前的所有字符并记录行号
                        ws = ws[index + 1:]  # 获取分隔符后面的字符
                        out_words.append({'word': a, 'line': line_num})  # 记录该分割符
                if ws != '':
                    out_words.append({'word': ws, 'line': line_num})  # 不为空则记录
        line_num += 1
    return out_words