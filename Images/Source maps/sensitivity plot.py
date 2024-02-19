import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import power_generation_maths

from variables_file import latitude, longitude, year, pitch, yaw, roll


total_power = []
day_of_year = []

def sense_plot_time_year(year, pitch, yaw, roll):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year_track = 1
    if is_leap_year(year):
        days_in_month[1] = 29  # Update February days to 29 for leap year
    
    for month in range(1, 13):
        for day in range(1, days_in_month[month - 1] + 1):

            print(f"{month:02d}-{day:02d}")

            power_of_day = 0

            for hour in range(24):
                for minute in range(60):
                    for second in range(60):
                       sun_values = power_generation_maths.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
                       power_of_day += sun_values.output_power
                       
            total_power.append(power_of_day)
            day_of_year.append(day_of_year_track)
            day_of_year_track += 1

    plt.plot(day_of_year, total_power)
    plt.xlabel("Day of Year")
    plt.ylabel("Total Power Generated")
    plt.title(f"Total Power Generated in {year}")
    plt.grid(True)
    plt.show()


def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

sense_plot_time_year(year, pitch, yaw, roll)