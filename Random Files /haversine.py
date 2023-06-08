import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, radians, sqrt, atan2

def cartesian_to_latlong(x):
    lat = x[0]
    lon = x[1]
    lat_rad = lat / 6371  # Earth's radius in km
    lon_rad = lon / (6371 * cos(radians(lat)))
    return np.array([lat_rad, lon_rad])

def latlong_to_cartesian(x):
    lat_rad = x[0]
    lon_rad = x[1]
    lat = lat_rad * 6371  # Earth's radius in km
    lon = lon_rad * (6371 * cos(radians(lat)))
    return np.array([lat, lon])

def haversine(lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth's radius in km

    return distance

def calculate_distance(lat1, lon1, lat2, lon2, use_haversine=True):
    if use_haversine:
        return haversine(lat1, lon1, lat2, lon2)
    else:
        # Alternative distance calculation method
        # ... Implement alternative method here ...
        pass

def generate_points_within_distance(radius_km):
    while True:
        # Generate random lat-long coordinates
        lat1 = np.random.uniform(-90, 90)
        lon1 = np.random.uniform(-180, 180)
        lat2 = np.random.uniform(-90, 90)
        lon2 = np.random.uniform(-180, 180)

        # Calculate the distance using the Haversine formula
        distance = calculate_distance(lat1, lon1, lat2, lon2)

        if distance <= radius_km:
            heading = np.random.uniform(0, 2*np.pi)  # Generate a random heading angle
            return np.array([latlong_to_cartesian(np.array([lat1, lon1])), heading]), np.array([latlong_to_cartesian(np.array([lat2, lon2])), heading])

x0, xG = generate_points_within_distance(5)  # Generate two points within 5 km of each other

def plot_pose(x, col):
    # small length just for plotting
    d = np.array([0, 0.2])
    # plot a dot with a pointing line
    plt.plot(x[0][0] + d * cos(x[0][1]), x[0][1] + d * sin(x[0][1]), col)
    plt.plot(x[0][0], x[0][1], col+'o')

plot_pose(x0, 'm')
plot_pose(xG, 'g')

plt.show()
