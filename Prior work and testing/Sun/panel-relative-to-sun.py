pitch = 0 #deg
roll = 0#deg
yaw = 0 #deg
heading = 0 #deg
altitude = 1000

azimuth = 30 #deg
elevation = 50 #deg

""" 
heading_diff = heading - azimuth

if (heading_diff < 0):
    heading_diff = 360 - abs(heading_diff)
if (heading_diff > 360):
    heading_diff = heading_diff - 360 
"""

import math

# Step 1: Convert azimuth and elevation to a 3D direction vector
def azimuth_elevation_to_vector(azimuth, elevation):
    x = math.cos(elevation) * math.cos(azimuth)
    y = math.cos(elevation) * math.sin(azimuth)
    z = math.sin(elevation)
    return [x, y, z]

# Step 2: Calculate the surface normal vector
def surface_normal_vector(pitch, yaw, roll):
    # Convert angles to radians
    alpha = math.radians(pitch)
    beta = math.radians(yaw)
    gamma = math.radians(roll)

    # Calculate rotation matrix
    Rx = [[1, 0, 0],
          [0, math.cos(alpha), -math.sin(alpha)],
          [0, math.sin(alpha), math.cos(alpha)]]

    Ry = [[math.cos(beta), 0, math.sin(beta)],
          [0, 1, 0],
          [-math.sin(beta), 0, math.cos(beta)]]

    Rz = [[math.cos(gamma), -math.sin(gamma), 0],
          [math.sin(gamma), math.cos(gamma), 0],
          [0, 0, 1]]

    # Multiply rotation matrices
    R = [[sum(a * b for a, b in zip(Rx_row, Ry_col)) for Ry_col in zip(*Ry)] for Rx_row in Rx]
    R = [[sum(a * b for a, b in zip(R_row, Rz_col)) for Rz_col in zip(*Rz)] for R_row in R]

    # Default normal vector [0, 0, 1]
    surface_normal = [0, 0, 1]

    # Multiply rotation matrix by the normal vector
    surface_normal = [sum(a * b for a, b in zip(R_row, surface_normal)) for R_row in R]

    return surface_normal

# Step 3: Calculate the dot product
def dot_product(ray_direction, surface_normal):
    dot_product = sum(a * b for a, b in zip(ray_direction, surface_normal))
    return dot_product

# Step 4: Calculate the incidence angle
def calculate_incidence_angle(ray_direction, surface_normal):
    dot_prod = dot_product(ray_direction, surface_normal)
    incidence_angle = math.acos(dot_prod)
    incidence_angle_degrees = math.degrees(incidence_angle)
    return incidence_angle_degrees

# Example usage
azimuth = math.radians(45)  # Example azimuth angle in radians
elevation = math.radians(30)  # Example elevation angle in radians
pitch = 10  # Example pitch angle in degrees
yaw = 20  # Example yaw angle in degrees
roll = 0  # Example roll angle in degrees

# Convert azimuth and elevation to direction vector
ray_direction = azimuth_elevation_to_vector(azimuth, elevation)

# Calculate surface normal vector
surface_normal = surface_normal_vector(pitch, yaw, roll)

# Calculate incidence angle
incidence_angle = calculate_incidence_angle(ray_direction, surface_normal)

print(f"Incidence Angle: {incidence_angle} degrees")
