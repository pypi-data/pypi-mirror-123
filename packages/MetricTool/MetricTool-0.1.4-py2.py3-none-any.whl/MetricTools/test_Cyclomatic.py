#coding=utf-8

import unittest

import sys
import os

sys.path.append(os.path.split(os.path.realpath(__file__))[0])
import Cyclomatic


class CyclomaticTest(unittest.TestCase):
    # 测试圈复杂度AND节点的正确性
    def test_Cyclomatic_and(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.and_enter()
        obj.and_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 1)
    # 测试圈复杂度OR节点的正确性
    def test_Cyclomatic_or(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.or_enter()
        obj.or_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 1)
    # 测试圈复杂度catch节点的正确性
    def test_Cyclomatic_catch(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.catch_enter()
        obj.catch_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度do节点的正确性
    def test_Cyclomatic_do(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.do_enter()
        obj.do_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度for节点的正确性
    def test_Cyclomatic_for(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.for_enter()
        obj.for_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度if节点的正确性
    def test_Cyclomatic_if(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.if_enter()
        obj.if_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度三元表达式节点的正确性
    def test_Cyclomatic_ternary(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度while节点的正确性
    def test_Cyclomatic_while(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.while_enter()
        obj.while_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试圈复杂度switch节点的正确性
    def test_Cyclomatic_switch(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.switch_enter()
        obj.switch_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 1)
    # 测试圈复杂度case节点的正确性
    def test_Cyclomatic_case(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.case_enter()
        obj.case_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['functions']['aa-10-1-15-1'], 2)
    # 测试文件平均圈复杂度的正确性
    def test_Cyclomatic_Avg(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.function_exit()

        obj.function_enter("bb", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.if_enter()
        obj.if_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['Avg'], 2.5)
    # 测试文件最大圈复杂度的正确性
    def test_Cyclomatic_Max(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.function_exit()

        obj.function_enter("bb", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.if_enter()
        obj.if_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['Max'], 3)
    # 测试文件累积圈复杂度的正确性
    def test_Cyclomatic_Sum(self):
        obj = Cyclomatic.FileUnit()
        obj.function_enter("aa", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.function_exit()

        obj.function_enter("bb", 10, 1, 15, 1)
        obj.ternary_enter()
        obj.ternary_exit()
        obj.if_enter()
        obj.if_exit()
        obj.function_exit()

        result = obj.result()
        self.assertEqual(result['Sum'], 5)

unittest.main()