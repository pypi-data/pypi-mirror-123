import concurrent.futures

from . import C_visitor as c_v
from . import Java_visitor as j_v


# 对源码文件进行度量计算
def do_cyclomatic(f_file):
    if c_v.is_valid_file(f_file):
        return f_file, c_v.cyclomatic_analysis(f_file)
    elif j_v.is_valid_file(f_file):
        return f_file, j_v.cyclomatic_analysis(f_file)
    return f_file, None


# 模块对外接口函数
# 对输入的源码文件列表进行圈复杂度计算
def para_cyclomatic(f_files):
    all_data = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(do_cyclomatic, f_files)
        for result in results:
            all_data[result[0]] = result[1]
    return all_data
