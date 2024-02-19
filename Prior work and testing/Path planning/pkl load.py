import pickle
import matplotlib.pyplot as plt

# Load the quadtree object from the .pkl file
with open('quadtree.pkl', 'rb') as file:
    quadtree = pickle.load(file)

# Visualize the quadtree
def visualize_quadtree(node, ax):
    if node.is_leaf:
        # Plot leaf node as a rectangle
        x, y, w, h = node.boundary
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, color='blue', linewidth=0.5))
    else:
        # Plot internal node as a rectangle with dashed lines
        x, y, w, h = node.boundary
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, color='red', linewidth=0.5, linestyle='dashed'))
        
        # Recursively visualize child nodes
        for child in node.children:
            visualize_quadtree(child, ax)

# Create a figure and axis
fig, ax = plt.subplots()

# Visualize the quadtree starting from the root node
visualize_quadtree(quadtree.get_root(), ax)  # Replace 'get_root()' with the correct method to get the root node

# Set axis limits
ax.set_xlim(0, quadtree.width)
ax.set_ylim(0, quadtree.height)

# Show the plot
plt.show()
