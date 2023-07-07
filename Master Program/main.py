"""
TODO:
- Timezone adjustment
- Comment and format code
- Add code header
"""
import matplotlib.pyplot as plt


from variables_file import *
from datetime import datetime, timedelta
import power_generation_maths
import power_consumption_maths
import graphs


graphs.power_start_depleted(2)



""" 
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
 """