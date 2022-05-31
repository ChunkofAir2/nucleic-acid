'''
    The Analog Module: (avoided circuit for some reason)
        purpose: 
            representing analog devices in a graph sort of way
'''

from .graph import Node, Graph
from .parser import SubGraph

class CircuitElement(Node):
    def __init__(self, _len):
        super().__init__(directed=True, ordered=True, len=_len)
    
class NetList(SubGraph):
    def __init__(self):
        super().__init__()

    def __str__(self): #encodes the netlist
        pass

class Function(CircuitElement):
    pass