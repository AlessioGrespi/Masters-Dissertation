import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import get_cmap

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('power_data.csv')

# Extract the data for the x, y, and z axes from the DataFrame
z = data['Outputted Power (kWh)']
y = data['Day of Year']
x = data['Latitude']

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the colormap
cmap = get_cmap('viridis')

# Plot the data points with colors based on latitude
ax.scatter(x, y, z, c=x, cmap=cmap)

# Add lines across x-axis readings for each latitude
for lat in set(x):
    lat_data = data[data['Latitude'] == lat]
    ax.plot(lat_data['Latitude'], lat_data['Day of Year'], lat_data['Outputted Power (kWh)'],  color='gray', alpha=0.5)

# Customize the plot (optional)
ax.set_title('Your Title')
ax.set_zlabel('Outputted Power (kWh)')
ax.set_ylabel('Day of Year')
ax.set_xlabel('Latitude')

# Add a colorbar
cbar = plt.colorbar(ax.collections[0])
cbar.set_label('Latitude')

# Adjust the spacing between the plot and the colorbar
plt.subplots_adjust(right=0.85)

# Display the plot
plt.show()
