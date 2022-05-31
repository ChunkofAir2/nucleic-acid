'''
    The Graph Module
        purpose: 
            backbone for the generation of netlists 
'''

import unittest

class Node:
    def __init__(self, directed=True, ordered=True, _len=(1, 1)):
        self.adj = ([], [])
        self.directed = directed 
        self.ordered = ordered
        self.len = _len

    def set_id(self, id):
        self.id = id 

    def add_edge(self, id1, id2):
        direction = 1 if id1 == self.id else 0
        to_id = id2 if id1 == self.id else id1

        if self.ordered:
            adj = [i[0] for i in self.adj[direction]]
        else: 
            adj = self.adj[direction]

        if (self.directed) or (to_id not in adj):
            if self.ordered:
                to_id = (to_id, len(self.adj[direction]))
            self.adj[direction].append(to_id)

    def replace_edge(self, map_id, direction='bi'): #id1 -> id2
        if direction == 'in' or direction == 'bi':
            for index, (id, order) in enumerate(self.adj[0]):
                if id in map_id:
                    self.adj[0][index] = (map_id[id], order)

        if direction == 'out' or direction == 'bi':
            for index, (id, order) in enumerate(self.adj[1]):
                if id in map_id:
                    self.adj[1][index] = (map_id[id], order)

    def remove_edge(self, id, direction='bi'):
        if direction == 'in' or direction == 'bi':
            for index, (in_id, _) in enumerate(self.adj[0]):
                if id == in_id:
                    self.adj[0].pop(index)

        if direction == 'out' or direction == 'bi':
            for index, (out_id, _) in enumerate(self.adj[1]):
                if id == out_id:
                    self.adj[1].pop(index)

    def add_graph(self, graph):
        self.g = graph

    def get_adj(self, direction='bi'):
        if self.ordered:
            if direction == 'bi': return set([i[0] for i in self.adj[0] + self.adj[1]])
            elif direction == 'in': return [i[0] for i in self.adj[0]]
            elif direction == 'out': return [i[0] for i in self.adj[1]]
        else :
            if direction == 'bi': return set(self.adj[0] + self.adj[1])
            elif direction == 'in': return self.adj[0]
            elif direction == 'out': return self.adj[1]

# this ensures that graphs can be included in other graphs 
class Graph: 
    def __init__(self):
        self.nodes = {}

    def get_node(self, id):
        if id in self.nodes:
            return self.nodes[id]
        else :
            return None 

    def add_node(self, node: Node, id=None):
        if id == None:
            id = len(self.nodes) + 1

        node.add_graph(self)
        node.set_id(id)
        self.nodes[id] = node
        return id
    
    def remove_node(self, id):
        for adj_id in self.nodes[id].get_adj():
            self.remove_edge(id, adj_id)
        return self.nodes.pop(id)

    def add_edge(self, id1, id2):
        self.nodes[id1].add_edge(id1, id2)
        self.nodes[id2].add_edge(id1, id2)
    
    def replace_edge(self, node, map_id, direction='bi'):
        self.nodes[node].replace_edge(map_id, direction=direction)

    def remove_edge(self, id1, id2, direction='bi'):
        self.nodes[id1].remove_edge(id2, direction=direction)
        self.nodes[id2].remove_edge(id1, direction=direction)

