#coding=utf-8

import unittest

from . import File_visit as f_v


class VisiteFileTest(unittest.TestCase):
    # 测试并行圈复杂度计算的正确性
    def test_VisitFile(self):
        files = f_v.visit_files('./test')
        self.assertEqual(len(files), 2)
    

unittest.main()