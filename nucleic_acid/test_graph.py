'''
    Unit testing (for now) for graphs 
'''

from .graph import Node, Graph
import unittest

class Test_Node(unittest.TestCase):
    def test_node(self): #testing the 3 edge related functions
        node = Node(directed=True, ordered=True)
        node.set_id(0)

        node.add_edge(node.id, 12)
        node.add_edge(10, node.id)

        node.replace_edge({12: 10}, direction='bi')        
        self.assertEqual(node.get_adj('out'), [10])

        node.replace_edge({10: 12}, direction='bi')
        self.assertEqual(node.get_adj('in'), [12])

        node.remove_edge(12, direction='bi')
        self.assertEqual(node.get_adj('bi'), set())

class Test_Graph(unittest.TestCase):
    def test_graph(self):
        graph = Graph()
        node1 = graph.add_node(Node())
        node2 = graph.add_node(Node())

        graph.add_edge(node1, node2)
        graph.add_edge(node2, node1)

        self.assertEqual(graph.nodes[node1].get_adj('bi'), set([node2]))
        self.assertEqual(graph.nodes[node2].get_adj('bi'), set([node1]))
