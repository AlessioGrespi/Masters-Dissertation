import power.power_consumption_maths as consumption
import power.power_generation_maths as generation

import sun_stuff.incidence as incidence
import sun_stuff.solar_power as power
import sun_stuff.sun_calc as calc

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

longitude = 0
year = 2023
""" 
solstice_dates = [(3, 20), (6, 21), (9, 23), (12, 22)]  # Equinox and solstice dates

def power_through_day(month, day):
    latitude_values = []
    power_values = []
    seconds = []
    minutes = []
    hours = []
    days = []
    months = []

    for latitude in range(10):
        latitude *= 10

        for hour in range(24):
            for minute in range(60):
                for second in range(60):
                    sun_values = generation.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch=0, yaw=0, roll=0)
                    
                    seconds.append(second)
                    minutes.append(minute)
                    hours.append(hour)
                    days.append(day)
                    months.append(month)
                    latitude_values.append(latitude)
                    power_values.append(sun_values.output_power)
 """

solstice_dates = [(6, 21), (12, 22)]  # Equinox and solstice dates
#solstice_dates = [ (6, 21), (12, 22)]  # Equinox and solstice dates

def power_through_day():
    latitude_values = []
    power_values = []
    #seconds = []
    #minutes = []
    hours = []
    days = []
    months = []

    for latitude in range(10):
        latitude *= 10
        for month, day in solstice_dates:
            for hour in range(24):
                for minute in range(4):
                    minute *= 15
                    #for second in range(60):

                    second = 0
                
                    sun_values = generation.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch=0, yaw=0, roll=0)
                
                    

                    #seconds.append(second)
                    #minutes.append(minute)
                    hours.append(hour +(minute/60))
                    days.append(day)
                    months.append(month)
                    latitude_values.append(latitude)
                    power_values.append(sun_values.output_power)

                    print(f"Month: {month}, Day: {day}, Latitude: {latitude}, hour: {hour +(minute/60)}")

    for latitude in range(9):
        latitude += 1
        latitude *= -10
        for month, day in solstice_dates:
            for hour in range(24):
                for minute in range(4):
                    minute *= 15
                    #for second in range(60):

                    second = 0

                
                    sun_values = generation.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch=0, yaw=0, roll=0)
                
                    

                    #seconds.append(second)
                    #minutes.append(minute)
                    hours.append(hour + (minute / 60))
                    days.append(day)
                    months.append(month)
                    latitude_values.append(latitude)
                    power_values.append(sun_values.output_power)

                    print(f"Month: {month}, Day: {day}, Latitude: {latitude}, hour: {hour + (minute / 60)}")            
    
    return latitude_values, power_values, hours, days, months
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Call the modified power_through_day function to get the data
latitude_values, power_values, hours, days, months = power_through_day()

# Define a color map for the solstice dates
date_colors = {(6, 21): 'g', (12, 22): 'c'}

# Map the date to a color for each data point
colors = [date_colors[(month, day)] for month, day in zip(months, days)]

# Define legend names individually
legend_names = ['Summer Solstice', 'Winter Solstice']

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set marker size (adjust the value as needed)
marker_size = 5

# Plot the data with date-based colors
scatter = ax.scatter(hours, latitude_values, power_values, c=colors, s=marker_size)

ax.set_xlabel('Time of Day (Hours)')
ax.set_ylabel('Latitude')
ax.set_zlabel('Power (W)')

# Create a legend with individually set names
legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=name, markersize=10, markerfacecolor=color) for name, color in zip(legend_names, date_colors.values())]
ax.legend(handles=legend_labels)

# Add grey lines for each latitude
unique_latitudes = sorted(set(latitude_values))

for lat in unique_latitudes:
    lat_indices = [i for i, val in enumerate(latitude_values) if val == lat]
    lat_hours = [hours[i] for i in lat_indices]
    lat_power = [power_values[i] for i in lat_indices]

    # Find segments where the latitude switches between dates
    lat_diff = np.diff(lat_hours)
    lat_switch_indices = np.where(lat_diff < 0)[0]

    # Plot separate line segments for each continuous segment of latitude values
    start_idx = 0
    for switch_idx in lat_switch_indices:
        ax.plot(lat_hours[start_idx : switch_idx + 1], [lat] * (switch_idx - start_idx + 1), lat_power[start_idx : switch_idx + 1], c='grey', linestyle='--', linewidth=0.5)
        start_idx = switch_idx + 1

    # Plot the remaining part of the latitude segment
    ax.plot(lat_hours[start_idx:], [lat] * (len(lat_hours) - start_idx), lat_power[start_idx:], c='grey', linestyle='--', linewidth=0.5)

plt.title('Power vs. Latitude vs. Time of Day')
plt.show()

""" 
def sense_generate_data(year, latitudes, solstice_dates):
    data = []

    for latitude in latitudes:
        print('Latitude: ', latitude)
        for date in solstice_dates:
            month, day = date
            print("Month: {}, Day: {}".format(month, day))

            if is_leap_year(year):
                days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            else:
                days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            day_of_year = sum(days_in_month[:month - 1]) + day

            power_per_hour = [0] * 24  # Initialize an array to store power for each hour

            for hour in range(24):
                for minute in range(60):
                    for second in range(60):
                        sun_values = generation.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch=0, yaw=0, roll=0)
                        power_per_hour[hour] += sun_values.output_power

            data.extend([(day_of_year, latitude, hour, power) for hour, power in enumerate(power_per_hour)])

    return data

def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

solstice_dates = [(3, 20), (6, 21), (9, 23), (12, 22)]  # Equinox and solstice dates
latitudes = list(range(0, 91, 10))
data = sense_generate_data(2023, latitudes, solstice_dates)

hour_of_day = [entry[2] for entry in data]
power_generated = [entry[3] for entry in data]
day_of_year = [entry[0] for entry in data]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Assign a color to each day based on day_of_year
colors = plt.cm.viridis((np.array(day_of_year) - min(day_of_year)) / (max(day_of_year) - min(day_of_year)))

for i in range(len(hour_of_day)):
    ax.scatter(hour_of_day[i], latitudes[i], power_generated[i], c=[colors[i]], marker='o')

ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Latitude')
ax.set_zlabel('Power Generated')
ax.set_title('Power Generated in 2023')

plt.show()
 """