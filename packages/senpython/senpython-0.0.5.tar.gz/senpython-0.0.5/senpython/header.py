# # # # # # # # # # # # # # # # #
# This file was generated from  #
# Code written in the Senpai    #
# Programming language          #
# # # # # # # # # # # # # # # # # 


import sys as _sys
# # # # # # # # #
# C L A S S E S #
# # # # # # # # #
from collections import deque as _deque

_use_custom_except = True


class Stack(_deque):
    _range = range

    def rot2(self):
        self[0], self[1] = self[1], self[0]

    def rot3(self):
        self[0], self[1], self[2] = self[2], self[0], self[1]

    def call_func(self, num_args):
        func = self.popleft()
        args = [self.popleft() for _ in self._range(num_args)]
        res = func(*args)
        if res is not None:
            self.appendleft(res)


class StackHolder(dict):
    def __init__(self, current_stack, **kwargs):
        super().__init__(kwargs)
        self.current_stack_name = current_stack
        self.current_stack = self[self.current_stack_name]

    def switch_stack(self, name):
        self.current_stack_name = name
        if name in self:
            self.current_stack = self[name]
        else:
            self[name] = Stack()
            self.current_stack = self[name]


stacks = StackHolder('bedroom', **{'bedroom': Stack()})

love = print
reason = input
crash = exit


def custom_except_hook(_type, value, tb):
    print("Sorry senpai, you messed up somewhere UmU", file=_sys.stderr)

    print(f"{_type.__name__}: {value}", file=_sys.stderr, end='\n\n')
    print("The status of stacks before the error occurred was:\n", file=_sys.stderr)

    for name in stacks:
        print(f'\t{name}: ', file=_sys.stderr, end='\n')
        for i, item in enumerate([repr(item) for item in stacks[name]]):
            print('\t\t', i, item, file=_sys.stderr, sep='\t', end='\n')
        print(file=_sys.stderr)
    print('\b \b', file=_sys.stderr)


if _use_custom_except:
    _sys.excepthook = custom_except_hook

# # # # # # # # # # # # #
# The next section was  #  
# generated from the    #
# source code           #
# # # # # # # # # # # # #
