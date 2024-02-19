import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

# Load the data from the file
with open('solar_data.pkl', 'rb') as file:
    data = pickle.load(file)

day_of_year = [entry[0] for entry in data]
latitude = [entry[1] for entry in data]
total_power = [entry[2] / 1000 for entry in data]  # Divide by 1000 to convert to kWh

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define a color map (you can change the colormap as needed)
cmap = plt.get_cmap('viridis')

# Normalize total power for coloring
norm = plt.Normalize(min(total_power), max(total_power))

scatter = ax.scatter(latitude, day_of_year, total_power, c=total_power, cmap=cmap, marker='o', norm=norm)

ax.set_xlabel('Latitude')
ax.set_ylabel('Day of Year')
ax.set_zlabel('Power Generated (kWh) per day')  # Updated axis label
ax.set_title('Total Power Generated in 2023')

# Add a color bar
cbar = fig.colorbar(scatter, ax=ax, label='Power Generated (kWh)')  # Updated color bar label

# Set the axis limits
ax.set_xlim(-90, 90)  # Adjust the latitude limits
ax.set_ylim(0, 365)  # Adjust the day of year limits

# Add lines for each latitude (in grey)
for lat in set(latitude):
    lat_indices = [i for i, val in enumerate(latitude) if val == lat]
    lat_day_of_year = [day_of_year[i] for i in lat_indices]
    lat_total_power = [total_power[i] for i in lat_indices]

    ax.plot([lat] * len(lat_day_of_year), lat_day_of_year, lat_total_power, c='grey')

plt.show()
