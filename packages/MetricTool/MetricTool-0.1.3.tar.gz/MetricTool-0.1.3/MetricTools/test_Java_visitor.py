

#coding=utf-8

import unittest

from . import Java_visitor as cv


class CyclomaticTest(unittest.TestCase):
    # 测试test.java圈复杂度的正确性
    def test_Cyclomatic_and(self):
        result = cv.cyclomatic_analysis('./test/test.java')
        
        # test1圈复杂度为9
        self.assertEqual(result['functions']['test1-4-4-35-5'], 9)
        # test2圈复杂度为3
        self.assertEqual(result['functions']['test2-38-4-55-5'], 4)
        # 文件平均圈复杂度为6
        self.assertEqual(result['Avg'], 6.5)
        # 文件最大圈复杂度为9
        self.assertEqual(result['Max'], 9)
        # 文件累积圈复杂度为12
        self.assertEqual(result['Sum'], 13)
    

unittest.main()