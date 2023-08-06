
import os
from tree_sitter import Language, Parser

from . import Cyclomatic



Language.build_library(
	'build/my-languages.so',
	[
		os.path.split(os.path.realpath(__file__))[0]+'/vendor/tree-sitter-c',
		os.path.split(os.path.realpath(__file__))[0]+'/vendor/tree-sitter-java'
	]
)


Java_LANGUAGE = Language('build/my-languages.so', 'java')


parser = Parser()
parser.set_language(Java_LANGUAGE)


# 判定是否为Java源码语言有效的文件
def is_valid_file(f_file):
    # 目前只支持小写java后缀源码文件
    if f_file.split('.')[-1] == 'java':
        return True
    return False

# Java源码语言解析函数
# 执行成功，返回tree-sitter根节点
# 执行失败，返回None
def parse_c(c_file_content):
    tree = parser.parse(c_file_content)
    return tree


# Java源码语言函数获取名称
def get_fun_name(node, c_file_content):
    for c in node.children:
        if c.type == 'identifier':
            return c_file_content[c.start_byte:c.end_byte].decode('utf-8')
    return None

# Java源码语言遍历函数
def visit_node(node, file_u, c_file_content):
    # 获取node类型
    # 对支持的node类型进行file_u的回调处理
    if node.type == "method_declaration":
        fun_name = get_fun_name(node, c_file_content)
        file_u.function_enter(fun_name, node.start_point[0], node.start_point[1], node.end_point[0], node.end_point[1])
    elif node.type == "if_statement":
        file_u.if_enter()
    elif node.type == "while_statement":
        file_u.while_enter()
    elif node.type == "for_statement":
        file_u.for_enter()
    elif node.type == "do_statement":
        file_u.do_enter()
    elif node.type == "ternary_expression":
        file_u.ternary_enter()
    elif node.type == "switch_expression":
        file_u.switch_enter()
    elif node.type == "switch_label" and node.children[0].type == 'case':
        file_u.case_enter()
    elif node.type == 'catch_clause':
        file_u.catch_enter()

    for child in node.children:
        visit_node(child, file_u, c_file_content)


    if node.type == "method_declaration":
        file_u.function_exit()
    elif node.type == "if_statement":
        file_u.if_exit()
    elif node.type == "while_statement":
        file_u.while_exit()
    elif node.type == "for_statement":
        file_u.for_exit()
    elif node.type == "do_statement":
        file_u.do_exit()
    elif node.type == "ternary_expression":
        file_u.ternary_exit()
    elif node.type == "switch_expression":
        file_u.switch_exit()
    elif node.type == "switch_label" and node.children[0].type == 'case':
        file_u.case_exit()
    elif node.type == 'catch_clause':
        file_u.catch_exit()


# C源码文件加载转换函数
def load_as_utf8(c_file):
    with open(c_file, 'rb') as f:
        data = f.read()
        return data
    return None

# C语言圈复杂度计算函数
def cyclomatic_analysis(c_file):
    # 加载源码内容
    # 为了后续计算函数名称方便
    content = load_as_utf8(c_file)
    if content is None:
        return None
    
    # 解析源码
    tree = parse_c(content)
    if tree is None:
        return None
    
    # 遍历语法树
    file_u = Cyclomatic.FileUnit()
    visit_node(tree.root_node, file_u, content)

    return file_u.result()