#coding=utf-8

# 源码文件模型
class FileUnit:
    
    def __init__(self) -> None:
        self.functions = {}
        self.cur_fun_name = ''
        self.cur_fun_complexity = 0

    # 访问函数进入
    # 每一个节点都有两个动作，节点访问进入、节点访问退出
    def function_enter(self, fun_name, start_line, start_col, end_line, end_col):
        self.cur_fun_name = F'''{fun_name}-{start_line}-{start_col}-{end_line}-{end_col}'''
        self.cur_fun_complexity = 1

    # 访问函数退出
    def function_exit(self):
        self.functions[self.cur_fun_name] = self.cur_fun_complexity

    # 访问And运算符节点
    def and_enter(self):
        pass
    def and_exit(self):
        pass
    # 访问or运算符节点
    def or_enter(self):
        pass
    def or_exit(self):
        pass
    # 访问catch节点
    def catch_enter(self):
        self.cur_fun_complexity += 1
    def catch_exit(self):
        pass
    # 访问Do节点
    def do_enter(self):
        self.cur_fun_complexity += 1
    def do_exit(self):
        pass
    # 访问for节点
    def for_enter(self):
        self.cur_fun_complexity += 1
    def for_exit(self):
        pass
    # 访问if节点
    def if_enter(self):
        self.cur_fun_complexity += 1
    def if_exit(self):
        pass
    # 访问三元表达式
    def ternary_enter(self):
        self.cur_fun_complexity += 1
    def ternary_exit(self):
        pass
    # 访问while节点
    def while_enter(self):
        self.cur_fun_complexity += 1
    def while_exit(self):
        pass
    # 访问switch节点
    def switch_enter(self):
        pass
    def switch_exit(self):
        pass
    # 访问case节点
    def case_enter(self):
        self.cur_fun_complexity += 1
    def case_exit(self):
        pass

    # 获取文件度量结果
    # 度量结果以字典形式返回，字典包含Avg,Max,Sum,Functions四个Key，分别代表文件平均圈复杂度、文件最大圈复杂度、文件累积圈复杂度、函数复杂度信息
    # 函数复杂度又是一个字典，key为函数名与位置信息组成的唯一Key，值为圈复杂度值。
    def result(self):
        avg = 0
        sum = 0
        max = 0
        for fun in self.functions:
            if self.functions[fun] > max:
                max = self.functions[fun]
            sum += self.functions[fun]
            avg += 1
        if avg > 0:
            avg = sum / avg
        
        result = {'Avg':avg, 'Max':max, 'Sum':sum, 'functions':self.functions}
        return result

