import itertools

def tsp_brute_force(graph):
    # Generate all possible permutations of the cities
    cities = list(graph.keys())
    permutations = itertools.permutations(cities)

    # Initialize variables
    min_distance = float('inf')
    best_path = None

    # Iterate over all permutations and calculate the total distance
    for path in permutations:
        distance = 0
        prev_city = path[0]

        for city in path[1:]:
            distance += graph[prev_city][city]
            prev_city = city

        # Update the best path if a shorter distance is found
        if distance < min_distance:
            min_distance = distance
            best_path = path

    return best_path, min_distance


# Example usage
graph = {
    'A': {'B': 10, 'C': 15, 'D': 20},
    'B': {'A': 10, 'C': 35, 'D': 25},
    'C': {'A': 15, 'B': 35, 'D': 30},
    'D': {'A': 20, 'B': 25, 'C': 30}
}

best_path, min_distance = tsp_brute_force(graph)
print("Best path:", best_path)
print("Minimum distance:", min_distance)

import matplotlib.pyplot as plt

def plot_tsp_path(graph, path):
    # Extract the coordinates of the cities from the graph
    cities = list(graph.keys())
    x_coords = [graph[city]['x'] for city in cities]
    y_coords = [graph[city]['y'] for city in cities]

    # Plot the cities
    plt.scatter(x_coords, y_coords, color='red', zorder=2)

    # Plot the TSP path
    path_coords = [(graph[city]['x'], graph[city]['y']) for city in path]
    path_coords.append(path_coords[0])  # Connect the last city to the first city
    path_x = [coord[0] for coord in path_coords]
    path_y = [coord[1] for coord in path_coords]
    plt.plot(path_x, path_y, color='blue', zorder=1)

    # Set the axis labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TSP Path')

    # Display the plot
    plt.show()


# Example usage
graph = {
    'A': {'x': 0, 'y': 0},
    'B': {'x': 10, 'y': 5},
    'C': {'x': 5, 'y': 15},
    'D': {'x': -5, 'y': 10}
}

path = ['A', 'B', 'C', 'D']

plot_tsp_path(graph, path)
