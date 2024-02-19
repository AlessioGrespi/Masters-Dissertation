import numpy as np
import matplotlib.pyplot as plt

# Define the graph as an adjacency matrix
graph = np.array([  [255, 0, 0, -1, 0, 0],
                    [0, 0, 0, -1, 0, 0],
                    [0, 0, 0, -1, 0, 0],
                    [0, 0, 0, -1, 0, 0],
                    [0, 0, 0, -1, 0, 0],
                    [0, 0, 0, -1, 0, 0],
                    [0, 0, 0, 0, 0, 0]])


# Define the heuristic values for each node
heuristics = np.array([7, 4, 3, 2, 5, 0])

def a_star(graph, heuristics, start, goal):
    open_list = [start]
    closed_list = []

    g_score = {node: float('inf') for node in range(len(graph))}
    g_score[start] = 0

    f_score = {node: float('inf') for node in range(len(graph))}
    f_score[start] = heuristics[start]

    while open_list:
        current = min(open_list, key=lambda node: f_score[node])
        if current == goal:
            return reconstruct_path(came_from, goal)

        open_list.remove(current)
        closed_list.append(current)

        for neighbor in range(len(graph[current])):
            if graph[current][neighbor] == -1 or neighbor in closed_list:
                continue

            tentative_g_score = g_score[current] + graph[current][neighbor]

            if neighbor not in open_list:
                open_list.append(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristics[neighbor]

    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

# Define the start and goal nodes
start_node = 0
goal_node = 5

# Find the path using A* algorithm
came_from = {}
path = a_star(graph, heuristics, start_node, goal_node)

# Plot the graph and the path
plt.figure()
plt.imshow(graph, cmap='gray', interpolation='nearest', vmin=-1, vmax=10)
plt.title('Graph')
plt.xticks(range(len(graph)))
plt.yticks(range(len(graph)))
plt.scatter(start_node, start_node, color='g', marker='o', s=200, label='Start')
plt.scatter(goal_node, goal_node, color='r', marker='o', s=200, label='Goal')
plt.legend()

if path:
    for i in range(len(path) - 1):
        plt.plot([path[i], path[i + 1]], [path[i], path[i + 1]], 'b', linewidth=2)

plt.show()
