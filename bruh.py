import networkx as nx
import heapq
import matplotlib.pyplot as plt

def generate_path(area_graph, rewards, start, goal):
    # Calculate the heuristic values based on rewards
    heuristic_values = {node: rewards[node] for node in area_graph.nodes()}

    # Modify edge weights based on the proximity to the direct path
    for edge in area_graph.edges():
        node1, node2 = edge
        distance_to_direct_path = abs(heuristic_values[node1] - heuristic_values[node2])
        area_graph.edges[node1, node2]['weight'] += distance_to_direct_path

    # Custom A* algorithm implementation
    open_list = [(0, start)]
    closed_list = set()
    parent = {}
    g_score = {node: float('inf') for node in area_graph.nodes()}
    g_score[start] = 0

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node != start:
                path.insert(0, current_node)
                current_node = parent[current_node]
            path.insert(0, start)
            return path

        closed_list.add(current_node)

        for neighbor, edge_data in area_graph[current_node].items():
            neighbor_cost = current_cost + edge_data['weight']
            if neighbor_cost < g_score[neighbor]:
                g_score[neighbor] = neighbor_cost
                priority = neighbor_cost + heuristic_values[neighbor]
                heapq.heappush(open_list, (priority, neighbor))
                parent[neighbor] = current_node

    return None

# Create the area graph
area_graph = nx.Graph()
area_graph.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
area_graph.add_edges_from([('A', 'B', {'weight': 0}), ('A', 'C', {'weight': 0}),
                           ('C', 'D', {'weight': 0}), ('D', 'B', {'weight': 0}),
                           ('B', 'E', {'weight': 0})])

# Assign rewards to each point
rewards = {'A': 10, 'B': 20, 'C': 5, 'D': 15, 'E': 5}

# Generate the path
path = generate_path(area_graph, rewards, 'A', 'B')

# Plot the area graph and the path
pos = nx.spring_layout(area_graph)

plt.figure(figsize=(8, 6))

# Draw the area graph
nx.draw_networkx(area_graph, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
# Draw the rewards as node labels
nx.draw_networkx_labels(area_graph, pos=pos, labels=rewards, font_color='black')

# Highlight the optimal path
if path:
    edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(area_graph, pos=pos, edgelist=edges, edge_color='red', width=2.0)

plt.title('Area Graph with Optimal Path')
plt.axis('off')
plt.show()

