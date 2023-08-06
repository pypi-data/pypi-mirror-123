
import sys

import File_visit as f_v
import Parallel_cyclomatic as p_c

# 圈复杂度计算模块对外接口
# 输入： 文件或目录
# 输出： 圈复杂度计算结果
def CyclomaticAnalysis(file_s):
    # 对文件、目录进行有效源码遍历
    files = f_v.visit_files(file_s)
    if len(files) == 0:
        print("没有发现有效的源码文件！")
        return None
    
    # 对文件列表进行并行化圈复杂度计算
    results = p_c.para_cyclomatic(files)
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python PyCyclomatic.py file_or_dir or python -m XX file_or_dir ")
        exit(-1)
    
    file_s = sys.argv[1]
    result = CyclomaticAnalysis(file_s)
    print(result)