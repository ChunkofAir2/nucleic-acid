'''
    The Parser module :
        purpose: 
            parse the content of the classes and functions 
'''

from .graph import Graph, Node

class IOBlock(Node): #in/out block used on SubGraph

    # more explaination of dictated 
    # {type(gate name): (input/output selection, eg. 0, 1 for and/or)}
    def __init__(self, outside, dictation, direction=None, ordered=True): 
        super().__init__(directed=True, ordered=ordered)
        self.direction = direction
        self.dictation = dictation
        self.id = direction # for now this is for subgraphs
 
        if direction == 'in':
            self.adj = (outside, [])
            self.col = 0
        elif direction == 'out':
            self.adj = ([], outside)
            self.col = 1

    def sum_col(self, col):
        len = 0
        for i in self.adj[col]:
            len += i[0].len[1-col] # if column 0 then its the output (1), vice versa
        return len 
    
    def is_col_eq(self):
        input_len = self.sum_col(0)
        output_len = self.sum_col(1)
        if input_len != output_len:
            raise TypeError(f'IO: input length ({input_len}) does not match\
            the output length ({output_len})')
    
    def is_dir_eq(self):
        for i, id in enumerate(self.adj[self.col][1:]):
            if self.g.nodes[self.adj[self.col][i-1][0]].len[1-self.col] == self.g.nodes[id[0]].len[1-self.col]:
                raise TypeError(f'IO: {self.direction} lengths (at element {i} and {i-1})\
                does not match the requirement that they must be equal')
    
    def expand(self, map_id): #expands using the specified map
        self.is_col_eq() #asserts for debugging

        for i in self.adj[1-self.col]: #maps the adjcency list from the subgraph to the new one 
            i = (map_id[i[0]], i[1])

        for i in self.adj[1-self.col]: # for every element that is a part of the subgraph
            if self.direction == 'in': 
                for l in self.dictation[type(i)]: # order as in the dictation
                    self.g.g.add_edge(self.adj[0][l], i[0])
            if self.direction == 'out':
                for l in self.dictation[type(i)]:
                    self.g.g.add_edge(i[0], self.adj[0][l])
        
        # in the case that the IO isn't picky about which sides to choose 
        # self.is_col_eq() #assert, used for debugging

        # io_len = (0, 0)
        # col_len = self.sum_col(0) #using zero because of convieniance, really doesn't matter
        # current = (self.adj[0][0][0], self.adj[1][0][0])
        # prev = (None, None)
        # i, j = 0, 0

        # while io_len[0] != col_len or io_len[1] != col_len: # advances each side like a race
        #     self.g.add_io_edge(current[0].id, current[1].id)

        #     if prev[0] != current[0]: # changes the length if a new node was connected 
        #         io_len[0] = io_len[0] + current[0].len
        #     if prev[1] != current[1]:
        #         io_len[1] = io_len[1] + current[1].len

        #     prev = current

        #     if io_len[0] >= io_len[1]: # new node if one side is lagging
        #         current[1] = self.adj[1][i][0]
        #         i+=1
        #     if io_len[0] <= io_len[1]:
        #         current[0] = self.adj[0][j][0]
        #         j+=1

        # self.g.remove_node(self.id)


class SubGraph(Node, Graph):
    std_dict = {} #TODO: finish this 

    def __init__(self, directed=True):
        super().__init__(directed, ordered=True)
        super(Graph, self).__init__()

    def add_io(self, dictation=None):
        if dictation == None :
            dictation = self.std_dict
        self.add_node(IOBlock(self.adj[0], dictation, direction='in', ordered=True))
        self.add_node(IOBlock(self.adj[1], dictation, direction='out', ordered=True))

    # def replace(self): #TODO: Why is this function even here?
    #     i = self.nodes['in'].get_adj('in')
    #     o = self.nodes['out'].get_adj('out')

    #     self.g.remove_node(self.id)
    #     self.g.add_node(self)

    #     for in_id in i:
    #         self.g.add_edge(in_id, self.id)
    #     for out_id in o:
    #         self.g.add_edge(self.id, out_id)

    def expand(self, map_id=None):
        map_id = {}
        for id in self.nodes:
            prev_id = id
            map_id[prev_id] = self.g.add_node(self.nodes[id]) # generates new id

        for id in self.nodes:
            self.g.replace_edge(id, map_id)

        #2 io blocks that expand into the graph
        self.nodes[map_id['in']].expand(map_id)      
        self.nodes[map_id['out']].expand(map_id)

        self.g.remove_node(self.id)
    
    def eval(self):
        pass

class parse():
    def __init__(self, circuit):
        self._circuit = circuit
        
    def __call__(self, *args):
        self.circuit = self._circuit(*args)
        self.subg = SubGraph()

        ordered = self.circuit.input.ordered

        self.subg.add_node(IOBlock(*self.circuit.input, direction='in', ordered=ordered))
        outputs = self.circuit.build()
        self.subg.add_node(IOBlock(*outputs, direction='out', ordered=ordered))

        #have to think about loops 
        #self.circuit.__call__ = self.subg.__call__

        return self
    
'''
class CircuitTemplate(Node):
    def __init__(self):
        self.input = ...

    def build(self):
        build circuit 
        return output
'''

def eval_graph(nodes):
    pass

