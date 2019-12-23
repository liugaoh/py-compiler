# -*- coding: utf-8 -*-
"""
   File Name：     test
   Description :
   Author :       康康
   date：          2019/12/16
"""
import os

from src.to_asm import to_asm


to_asm('test.c')
os.system("gcc " + 'test.s ' + "-o " + 'test')
os.system("./test")
# result = "编译成功，执行结果：\n"
# result += os.popen("test").read()
# print(result)