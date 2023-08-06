

#coding=utf-8

import unittest
import sys
import os

sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import C_visitor as cv


class CyclomaticTest(unittest.TestCase):
    # 测试test.c圈复杂度的正确性
    def test_Cyclomatic_and(self):
        result = cv.cyclomatic_analysis(os.path.split(os.path.realpath(__file__))[0] + '/test/test.c')

        # test1圈复杂度为9
        self.assertEqual(result['functions']['test1-2-0-33-1'], 9)
        # test2圈复杂度为3
        self.assertEqual(result['functions']['test2-36-0-47-1'], 3)
        # 文件平均圈复杂度为6
        self.assertEqual(result['Avg'], 6)
        # 文件最大圈复杂度为9
        self.assertEqual(result['Max'], 9)
        # 文件累积圈复杂度为12
        self.assertEqual(result['Sum'], 12)
    

unittest.main()