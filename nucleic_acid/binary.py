'''
    This is the Binary Module
        purpose:
            represenating of binary datatypes as graph elements 
        contains: 
            Bit
            Bits
'''

import multiprocessing
from .graph import Node, Graph
from .parser import SubGraph

class Boolean(Node):
    def __init__(self, _len): #len: (in_len, out_len)
        super().__init__(directed=True, ordered=True, len=_len)

    def incompat_err(self, name, other=None):
        if isinstance(other, int):
            raise TypeError(f'\'{name}\' accepts inputs of len({self.len[0]}),\
            but input has len({other}')
        elif other != None:
            raise TypeError(f'\'{name}\' accepts inputs of len({self.len[1]}),\
            but {self=} has len({self.len[1]}) and {other=} has len({other.len[1]}')

    def add_gate(self, gate, other=None, mult=1):
        if mult > 1: 
            id = self.g.add_node(LogicList(gate, mult=mult))
        else:
            id = self.g.add_node(gate())

        self.g.add_edge(self.id, id)
        if other != None:
            self.g.add_edge(other.id, id)
        return id

    #not very useful, TODO: delete

    def __call__(self):
        self.eval()

    def __rshift__(self, other): # we have to use the '>>' operator to overload the equal sign
        if self.len[1] == other.len[0]:
            self.g.add_edge(self.id, id)

    #these apply to all boolean logic

    def __add__(self, other):  
        if self.len[1] + other.len[1] >= 2:
            if self.len[1] == other.len[1]:
                id = self.add_gate(OR, other)
        self.incompat_err(other, 'or', 2)
        return self.g.get_node(id)

    def __mul__(self, other):
        if self.len[1] + other.len[1] >= 2:
            if self.len[1] == other.len[1]:
                id = self.add_gate(AND, other)
        self.incompat_err(other, 'and', 2)
        return self.g.get_node(id)
    
    def __invert__(self):
        self.add_gate(NOT)

class Bits(Boolean):
    def __init__(self, _len=1):
        super().__init__((_len, _len))
        self.bits = []
    
    def eval(self):
        return self.bits
    
    def eq(self):
        bits = []
        for i in self.get_adj(direction='out'):
            bits += i()
        
        if len(bits) != self.len[0]:
            self.incompat_err('reg', len(bits))
        else:
            self.bits = bits
            return self.bits

class LogicList(SubGraph, Boolean):
    def __init__(self, gate, mult=2):
        super().__init__()
        super(Boolean, self).__init__(_len = (i * mult for i in gate.length))

        self.mult = mult
        self.gate = gate
        self.add_io()

    def build(self):
        dictation = {type(self.gate): (0, 1)}
        for i in range(self.mult):
            id = self.add_node(self.gate())
            self.add_edge('in', id)
            self.add_edge(id, 'out')
        

class OR(Boolean):
    length = (2, 1)

    def __init__(self):
        super().__init__(self.length)

    def eval(self):
        in_adj = self.get_adj(direction = 'in')
        return self.g.node[in_adj[0]()] | self.g.node[in_adj[1]]

class AND(Boolean):
    def __init__(self):
        super().__init__((2, 1))
    
    def eval(self):
        in_adj = self.get_adj(direction = 'in')
        return in_adj[0]() & in_adj[1]()

class NOT(Boolean):
    def __init__(self):
        super().__init__((1, 1))

    def eval(self):
        self.get_adj(direction = 'in')

