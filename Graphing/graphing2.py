import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('power_data.csv')

# Extract the data for the x, y, and z axes from the DataFrame
z = data['Outputted Power (kWh)']
y = data['Day of Year']
x = data['Latitude']

# Create a 3D plot
fig = plt.figure()
ax3d = fig.add_subplot(111, projection='3d')

# Define the colormap
cmap = cm.get_cmap('viridis')

# Plot the 3D data points with colors based on latitude
ax3d.scatter(x, y, z, c=x, cmap=cmap)

# Add lines across x-axis readings for each latitude
for lat in set(x):
    lat_data = data[data['Latitude'] == lat]
    ax3d.plot(lat_data['Latitude'], lat_data['Day of Year'], lat_data['Outputted Power (kWh)'], color='gray', alpha=0.5)

# Customize the 3D plot (optional)
ax3d.set_title('Your Title')
ax3d.set_zlabel('Outputted Power (kWh)')
ax3d.set_ylabel('Day of Year')
ax3d.set_xlabel('Latitude')

# Create a twin axes for the 2D graph
ax2d = fig.add_subplot(111, frame_on=False)
ax2d.plot(y, z, color='red')

# Customize the 2D plot (optional)
ax2d.yaxis.tick_right()
ax2d.yaxis.set_label_position("right")
ax2d.set_ylabel('Outputted Power (kWh)', color='red')

# Adjust the spacing between the plot and the colorbar
plt.subplots_adjust(right=0.85)

# Add a colorbar
cbar = plt.colorbar(ax3d.collections[0])
cbar.set_label('Latitude')

# Display the plot
plt.show()
