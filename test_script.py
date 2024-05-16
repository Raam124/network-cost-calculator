import unittest
import networkx as nx
from script import calculate_cost
from rate_card import RATE_CARD_A,RATE_CARD_B


class TestCostCalculation(unittest.TestCase):
    

    def setUp(self):
        """ Create a sample graph with the values defiend in the challenge"""
        self.G = nx.Graph()
        self.G.add_node("A", type="Cabinet")
        self.G.add_node("B", type="Pot")
        self.G.add_node("C", type="Pot")
        self.G.add_node("D", type="Pot")
        self.G.add_node("E", type="Pot")
        self.G.add_node("F", type="Chamber")
        self.G.add_node("G", type="Chamber")
        self.G.add_node("H", type="Chamber")
        self.G.add_node("I", type="Chamber")
        self.G.add_edge("A", "F", material="verge", length=50)
        self.G.add_edge("B", "F", material="verge", length=20)
        self.G.add_edge("C", "G", material="road", length=50)
        self.G.add_edge("D", "H", material="road", length=100)
        self.G.add_edge("E", "H", material="verge", length=50)
        self.G.add_edge("F", "G", material="verge", length=100)
        self.G.add_edge("G", "I", material="road", length=40)
        self.G.add_edge("H", "G", material="road", length=100)

    def test_rate_card_a(self):
        """Test cost calculation with rate card A."""
        pot_costs_a, total_cost_a = calculate_cost(self.G, RATE_CARD_A)
        self.assertEqual(total_cost_a, 69700)
        self.assertEqual(pot_costs_a["B"], 4800)
        self.assertEqual(pot_costs_a["C"], 14000)
        self.assertEqual(pot_costs_a["D"], 29200)
        self.assertEqual(pot_costs_a["E"], 21700)

    def test_rate_card_b(self):
        """Test cost calculation with rate card B."""
        pot_costs_b, total_cost_b = calculate_cost(self.G, RATE_CARD_B)
        self.assertEqual(total_cost_b, 75800)
        self.assertEqual(pot_costs_b["B"], 5600)
        self.assertEqual(pot_costs_b["C"], 15600)
        self.assertEqual(pot_costs_b["D"], 30800)
        self.assertEqual(pot_costs_b["E"], 23800)


    """ below are some edge cases I thought of"""

    def test_rate_card_b_with_pot_cost(self):
        """Test cost calculation with rate card B and specific pot cost. (rate card A already have a fixed pot cost so this test is not required for A)"""
        rate_card_b_with_cost = RATE_CARD_B.copy()
        rate_card_b_with_cost["pot_cost"] = 1500
        pot_costs_b, total_cost_b = calculate_cost(self.G, rate_card_b_with_cost)
        self.assertEqual(total_cost_b, 63400)
        self.assertEqual(pot_costs_b["B"], 5700)
        self.assertEqual(pot_costs_b["C"], 13100)
        self.assertEqual(pot_costs_b["D"], 25300)
        self.assertEqual(pot_costs_b["E"], 19300)

    def test_empty_graph(self):
        """Test cost calculation with an empty graph."""
        empty_graph = nx.Graph()
        pot_costs, total_cost = calculate_cost(empty_graph, RATE_CARD_A)
        self.assertEqual(total_cost, 0)
        self.assertEqual(len(pot_costs), 0)

    def test_single_node_graph(self):
        """Test cost calculation with a single node graph.(Only Cabinet)"""
        single_node_graph = nx.Graph()
        single_node_graph.add_node("A", type="Cabinet")
        pot_costs, total_cost = calculate_cost(single_node_graph, RATE_CARD_A)
        self.assertEqual(total_cost, 0)
        self.assertEqual(len(pot_costs), 0)

if __name__ == '__main__':
    unittest.main()
