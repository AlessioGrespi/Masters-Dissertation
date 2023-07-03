"""
TODO:
- Timezone adjustment
- Comment and format code
- Add code header
"""
import matplotlib.pyplot as plt
import sun_calc
import incidence
import solar_power
import power_maths
import math
from variables_file import *
from datetime import datetime, timedelta

power_maths.power_on_wing(latitude, longitude, year, month, day, hour, minute, pitch, yaw, roll)
power_maths.power_through_day(latitude, longitude, year, month, day, pitch, yaw, roll)

plt.figure(figsize=(12, 6))
plt.plot(hours, zenith_angles, label="Zenith Angle")
#plt.plot(hours, elevation_angles, label="Elevation Angle")
plt.plot(hours, azimuths, label="Azimuth")
#plt.plot(hours, incidence_angles, label="Incidence")
plt.plot(hours, power_day, label="Power")
plt.xlabel("Hour of the day")
plt.ylabel("Angle (degrees)")
plt.title("Sun Position Throughout the Day")
plt.legend()
plt.xlim(0, 24)  # Set x-axis limits
plt.xticks(range(0, 25, 1))  # Set x-axis tick marks every 4 units
plt.grid(True)
plt.show() 
