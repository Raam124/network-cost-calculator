import networkx as nx
from rate_card import RATE_CARD_A, RATE_CARD_B

def calculate_cost(G, rate_card):
    """" print statements are added to debug the code easily (commented out)"""
    pot_costs = {} 
    
    # Find the shortest path from each pot to the cabinet
    for pot in G.nodes():
        if G.nodes[pot]["type"] == "Pot":
            try:
                path_to_cabinet = nx.shortest_path(G, source=pot, target="A", weight="length")
                # print(path_to_cabinet)
                total_cost = rate_card["cabinet_cost"]  # Cabinet cost is defaultly added for all pots
                
                # Calculate cost along the path from pot to cabinet
                for i in range(len(path_to_cabinet) - 1):
                    current_node = path_to_cabinet[i]
                    next_node = path_to_cabinet[i + 1]
                    # print(current_node,next_node)
                    
                    # Get the cost of trench and chamber
                    edge_data = G.edges[current_node, next_node]
                    length = edge_data["length"]
                    trench_material = edge_data["material"]
                    trench_cost = rate_card["verge_trench_cost"] if trench_material == "verge" else rate_card["road_trench_cost"]
                    chamber_cost = rate_card["chamber_cost"]
                    # print(length,trench_cost,chamber_cost)
                    
                    # Add Trench cost to total cost
                    total_cost += trench_cost * length

                    #  Add Chamber cost to total cost
                    if G.nodes[next_node]["type"] != "Cabinet":
                        total_cost += chamber_cost 
                    
                    # Calculating Pot cost for RATE CARD A
                    if rate_card == RATE_CARD_A:
                        if G.nodes[current_node]["type"] == "Pot":
                            pot_cost = rate_card["pot_cost"]
                            total_cost += pot_cost
                    
                    # Calculating Pot cost for RATE CARD B
                    if rate_card == RATE_CARD_B:
                        total_cost += 20 * length                
                
                pot_costs[pot] = total_cost
            except nx.NetworkXNoPath:
                return "Error: No path found from pot {} to cabinet.".format(pot)

    # Calculate the total cost
    total_cost = sum(pot_costs.values())
    
    return pot_costs, total_cost


if __name__ == "__main__":
    G = nx.read_graphml("problem.graphml")

    pot_costs_a, total_cost_a = calculate_cost(G, RATE_CARD_A)
    pot_costs_b, total_cost_b = calculate_cost(G, RATE_CARD_B)

    print("Costs for Rate Card A:")
    for pot, cost in pot_costs_a.items():
        print(f"Pot {pot}: £{cost}")
    print("Total Cost using Rate Card A: £", total_cost_a)

    print("\nCosts for Rate Card B:")
    for pot, cost in pot_costs_b.items():
        print(f"Pot {pot}: £{cost}")
    print("Total Cost using Rate Card B: £", total_cost_b)
