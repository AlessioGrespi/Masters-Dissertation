import power.power_consumption_maths as consumption
import power.power_generation_maths as generation

import sun_stuff.incidence as incidence
import sun_stuff.solar_power as power
import sun_stuff.sun_calc as calc

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

latitude_intervals = list(range(-90, 91, 10))
longitude = 0

def sense_generate_data(year, pitch, yaw, roll):
    data = []

    for latitude in latitude_intervals:
        print('latitude ', latitude)
        for month in range(1, 13):
            # Get data for the 15th day of each month
            day = 15

            print("month ", month)

            if is_leap_year(year):
                days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            else:
                days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            day_of_year = sum(days_in_month[:month - 1]) + day

            power_of_day = 0

            for hour in range(24):
                for minute in range(60):
                    for second in range(60):
                        sun_values = generation.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
                        power_of_day += sun_values.output_power

            print(f"Month: {month}, Day: {day}, Latitude: {latitude}, hour: {hour}")     

            data.append((day_of_year, latitude, power_of_day))

    return data

def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

# Generate data and save it to a file
data = sense_generate_data(2023, 0, 0, 0)

with open('solar_data.pkl', 'wb') as file:
    pickle.dump(data, file)

# Load the data from the file
with open('solar_data.pkl', 'rb') as file:
    data = pickle.load(file)

day_of_year = [entry[0] for entry in data]
latitude = [entry[1] for entry in data]
total_power = [entry[2] for entry in data]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(day_of_year, latitude, total_power, c='b', marker='o')

ax.set_xlabel('Day of Year')
ax.set_ylabel('Latitude')
ax.set_zlabel('Total Power Generated')
ax.set_title('Total Power Generated in 2023')

plt.show()
