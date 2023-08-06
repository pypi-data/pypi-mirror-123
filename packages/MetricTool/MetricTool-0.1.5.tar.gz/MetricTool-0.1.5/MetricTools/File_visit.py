

import sys
import os

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

import C_visitor as c_v
import Java_visitor as j_v


# 判定源码文件是否为有效源码文件
def is_valid_file(f_file):
    return c_v.is_valid_file(f_file) or j_v.is_valid_file(f_file)

# 对输入文件、目录进行统一遍历
# 返回有效的源码文件列表
def visit_files(file_s):
    # 记录有效源码文件
    result_files = []
    # 判定输入是否为文件
    if os.path.isfile(file_s):
        if is_valid_file(file_s):
            result_files.append(file_s)
        return result_files
    
    # 对目录进行遍历
    for root, dirs, files in os.walk(file_s):
        # 对目录下文件进行遍历
        for file in files:
            f_path = os.path.join(root, file)
            if is_valid_file(f_path):
                result_files.append(f_path)
    
    return result_files