from re import S
from nucleic_acid import *
import unittest
'''
# usage
@parse
class BooleanAdder(): # generates a graph with a, b, c as inputs, outputing sum and carry
    def __init__(self):
        self.inputs = (*var.bits(3).type(var.boolean))
        self.outputs = (*var.bits(2).type(var.boolean))

    def build(self): # using logic gates and boolean logic
        a, b, c = self.input
        sum, carry = self.output

        xor_ab, carry = None

        a ** b >> xor_ab
        xor_ab ** c >> sum
        xor_ab * c + a * b >> carry
        
    
    def __call__(self, bin_input):
        bin_input >> self.input
        

@parse
class MOSAdder():
    def __init__(self):
        self.inputs = var.wire_list(3) # wires can carry analog information, as opposed to bits

        self.source = None
        self.drain = None
    
    def __call__(self): 
        v = self.source 
        a, b, c = tuple(self.inputs)
        d = self.drain
        w = var.wire_list(4)

        v @ (-a, -b) >> w[0] # '-' sign for nmos, @ to connect v to both elements, and | to combine them 
        ((w[0] - b) - a) & (w[0] - c) >> w[1] # w[1] is one of the outputs
        (w[1] + c) @ (+a, +b) >> d 
        (w[1] + a) + b >> d 

        v @ (-a, -b, -c) >> w[2]
        (((w[2] + a) + b) + c) & (w[2] - w[1]) >> w[3]
        (w[3] + w[1]) @ (+a, +b, +c) >> d
        ((w[3] + c) + a) + b >> d
        v - w[3] >> w[4] + w[3] >> d

        return (w[1], w[4])

@bench('digital', iter=2**3) # do full simulation
class DigitalAdder_Bench():
    def __init__(self, adder):
        self.counter = var.bits(3).type(var.integer.decimal) # this allows us to do easy integer addition
        self.adder = adder

    def __call__(self):
        self.counter += 1
        return self.adder(self.counter)

    def expected(self):
        s = self.counter[0] + self.counter[1] + self.counter[2]
        return tuple(s.type(var.integer.binary))

'''

class Test_DigitalAdder(unittest.TestCase):
    def test_increment(self):
        print("true")


if __name__ == '__main__':
    unittest.main()