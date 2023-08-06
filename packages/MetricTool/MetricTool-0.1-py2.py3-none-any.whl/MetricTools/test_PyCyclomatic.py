#coding=utf-8

import unittest

import PyCyclomatic


class CyclomaticTest(unittest.TestCase):
    # 测试顶层模块圈复杂度计算的正确性
    def test_Cyclomatic(self):
        file_s = '../test'
        results = PyCyclomatic.CyclomaticAnalysis(file_s)


        result = results['../test/test.java']
        
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


        result = results['../test/test.c']

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