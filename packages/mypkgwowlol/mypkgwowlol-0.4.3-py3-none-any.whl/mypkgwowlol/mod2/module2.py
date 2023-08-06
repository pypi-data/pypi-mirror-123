import sys, os
sys.path.append(os.path.realpath('..'))
from mod1 import module1

class module_2():

    def __init__(self):
        pass

    def module_print(self):
        modx = module1.module_1()
        x = 73
        y = 35
        z = modx.add_two(x,y)
        print(z)