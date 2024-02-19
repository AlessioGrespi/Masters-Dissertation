import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the quadtree data from the saved JSON file
with open("quadtree.json", "r") as json_file:
    quadtree = json.load(json_file)

def create_navigation_graph(quadtree):
    # Create a directed graph
    G = nx.DiGraph()

    def add_edges(node_id, node_data):
        for child_id, child_data in enumerate(node_data.get("children", [])):
            G.add_edge(node_id, child_id)
            add_edges(child_id, child_data)

    # Start adding edges from the root node (use 0 as the root node ID)
    add_edges(0, quadtree)

    return G

# Create the navigation graph
navigation_graph = create_navigation_graph(quadtree)

# Draw the navigation graph
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(navigation_graph, seed=42)
nx.draw(navigation_graph, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", arrowsize=10, connectionstyle="arc3, rad = 0.1")

plt.title("Navigation Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig("navigation_graph.png")
plt.show()
