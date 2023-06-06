import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def calculate_angle(x1, y1, x2, y2):
    # Calculate the angle between two points
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def plot_tsp_path(graph, path, turn_radius):
    # Extract the coordinates of the cities from the graph
    cities = list(graph.keys())
    x_coords = [graph[city]['x'] for city in cities]
    y_coords = [graph[city]['y'] for city in cities]

    # Plot the cities
    plt.scatter(x_coords, y_coords, color='red', zorder=2)

    # Plot the TSP path
    for i in range(len(path)):
        current_city = path[i]
        next_city = path[(i + 1) % len(path)]  # Wrap around to connect the last city to the first city

        # Calculate the center of the Dubins path arc
        x_center = (graph[current_city]['x'] + graph[next_city]['x']) / 2
        y_center = (graph[current_city]['y'] + graph[next_city]['y']) / 2

        # Calculate the start and end angles of the Dubins path arc
        start_angle = graph[current_city]['angle']
        end_angle = graph[next_city]['angle']

        # Calculate the radius of the Dubins path arc
        radius = turn_radius

        # Create and plot the Dubins path arc
        arc = Arc((x_center, y_center), radius * 2, radius * 2, 0, start_angle, end_angle)
        plt.gca().add_patch(arc)

    # Set the axis labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TSP Path')

    # Set equal aspect ratio for a more accurate plot
    plt.gca().set_aspect('equal')

    # Display the plot
    plt.show()


# Example usage
graph = {
    'A': {'x': 0, 'y': 0, 'angle': 45},
    'B': {'x': 10, 'y': 5, 'angle': 180},
    'C': {'x': 5, 'y': 15, 'angle': -90},
    'D': {'x': -5, 'y': 10, 'angle': 0}
}

path = ['A', 'B', 'C', 'D']

turn_radius = 2  # Set the minimum turn radius for the Dubins path

plot_tsp_path(graph, path, turn_radius)
