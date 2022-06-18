'''
    The Parser module :
        purpose: 
            parse the content of the classes and functions 
'''

from re import M
from .graph import Graph, Node

class IOBlock(Node): #
    '''in/out block used on SubGraph'''

    available_methods = ['dictated', 'aligned']
    # more explaination of dictated 
    # {type(gate name): (input/output selection, eg. 0, 1 for and/or)}
    def __init__(self, outside, *args, direction=None, ordered=True, method='aligned'): 
        super().__init__(directed=True, ordered=ordered)
        self.direction = direction
        if method not in self.available_methods:
            available = ' ,'.join(self.available_methods)
            raise ValueError(f'IO(__init__): the correspondance method \'{method}\'\
                does not math the available options({available})')
        self.method = method

        if self.method == 'dictated': #can expanded to accomodate more methods
            self.dictation = args[0]
        
        self.id = direction # for now this is for subgraphs

        if direction == 'in':
            self.adj = (outside, [])
            self.col = 0
        elif direction == 'out':
            self.adj = ([], outside)
            self.col = 1
        else :
            raise TypeError(f'IO(__init__): the direction \'{direction}\' \
                does not match the available options (in, out)')

        self._internal_adj = ([], [])

    def sum_col(self, column):
        # for clarity columns are represented externally as a string
        if column not in {'in', 'out'}:
            raise TypeError(f'IO(sum_col): the column name {column}\
            does not match the available columns (in, out)') 
        col = 0 if column == 'in' else 1 # we only expect 'in' and 'out'

        #we loop over the column and collects the length of each node's in/output
        len = 0
        for i in self.adj[col]:
            len += self.g.g.node[i[0]].len[1-col] # if column 0 then its the output (1), vice versa
        return len 
    
    def is_col_eq(self):
        input_len = self.sum_col('in')
        output_len = self.sum_col('out')
        if input_len != output_len:
            raise ValueError(f'IO: input length ({input_len}) does not match\
            the output length ({output_len})')
    
    def is_dir_eq(self):
        for i, id in enumerate(self.adj[self.col][1:]):
            if self.g.nodes[self.adj[self.col][i-1][0]].len[1-self.col] == self.g.nodes[id[0]].len[1-self.col]:
                raise ValueError(f'IO: {self.direction} lengths (at element {i} and {i-1})\
                does not match the requirement that they must be equal')
    
    def expand(self, map_id): #expands using the specified map
        for i in self.adj[1-self.col]: #maps the adjcency list from the subgraph to the new one 
            i = (map_id[i[0]], i[1])

        if self.method == 'dictated':
            self.expand_dictated()
        elif self.method == 'aligned':
            self.expand_aligned()

        self.g.remove_node(self.id)

    def expand_dictated(self):
        self.is_dir_eq() #asserts for debugging

        for i in self.adj[1-self.col]: # for every element that is a part of the subgraph
            if self.direction == 'in': 
                for l in self.dictation[type(i)]: # order as in the dictation
                    self.g.g.add_edge(self.adj[0][l], i[0])
            if self.direction == 'out':
                for l in self.dictation[type(i)]:
                    self.g.g.add_edge(i[0], self.adj[0][l])
    
    def expand_aligned(self):
        # in the case that the IO isn't picky about which sides to choose 
        self.is_col_eq() #asserts for debugging

        io_len = (0, 0)
        col_len = self.sum_col(0) #using zero because of convieniance, really doesn't matter
        current = (self.adj[0][0][0], self.adj[1][0][0])
        prev = (None, None)
        i, j = 0, 0

        while io_len[0] != col_len or io_len[1] != col_len: #advances each lagging side
            self.g.add_io_edge(current[0].id, current[1].id)

            if prev[0] != current[0]: # changes the length if a new node was connected 
                io_len[0] = io_len[0] + self.g.g.nodes[current[0]].len
            if prev[1] != current[1]:
                io_len[1] = io_len[1] + self.g.g.nodes[current[1]].len

            prev = current

            if io_len[0] >= io_len[1]: # new node if one side is lagging
                current[1] = self.adj[1][i][0]
                i+=1
            if io_len[0] <= io_len[1]:
                current[0] = self.adj[0][j][0]
                j+=1


class SubGraph(Node, Graph):

    def __init__(self, directed=True):
        super().__init__(directed, ordered=True)
        super(Graph, self).__init__()

    def add_io(self, *args, method=None):
        self.add_node(IOBlock(self.adj[0], *args, direction='in', ordered=True, method=method))
        self.add_node(IOBlock(self.adj[1], *args, direction='out', ordered=True, method=method))

    def expand(self, map_id=None):
        map_id = {}
        for id in self.nodes:
            if id == 'in' or id == 'out': # we do not want to modify them
                continue
            prev_id = id
            map_id[prev_id] = self.g.add_node(self.nodes[id]) # generates new id

        for id in self.nodes:
            self.g.replace_edge(id, map_id)

        #2 io blocks that expand into the graph
        self.nodes[map_id['in']].expand(map_id)      
        self.nodes[map_id['out']].expand(map_id)

        self.g.remove_node(self.id)

class parse(SubGraph):
    def __init__(self, circuit):
        self._circuit = circuit

    def __call__(self, *args): 
        #the public facing part has way more try excepts for obvious reasons 

        self.circuit = self._circuit(*args)
        try:
            circuit_args = self.circuit.get_args()
        except NameError:
            circuit_args = ['dictated']

        if len(circuit_args) > 1:
            self.add_io(circuit_args[1:], method=circuit_args[0])
        elif len(circuit_args) == 1: 
            self.add_io(method=circuit_args[0])
        try:
            for i in self.circuit.inputs:
                self.add_edge('in', i.id)
            for o in self.circuit.outputs:
                self.add_edge('out', o.id)
        except NameError:
            raise TypeError('parse(__call__): the circuit does not have input[s]/output[s]')

        try:
            self.circuit.build()
        except NameError:
            raise TypeError('parse(__call__): the circuit does not contain build() function required')

        return self
    
'''
class CircuitTemplate(Node):
    def __init__(self):
        self.input = ...

    def build(self):
        build circuit 
        return output
'''

