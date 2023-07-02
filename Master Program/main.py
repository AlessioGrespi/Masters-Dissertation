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
import power_drain
import math

latitude = 51.509865
longitude = -0.118092

#time in UTC
year = 2023
month = 6
day = 25
hour = 19
minute = 43
second = 40
timezone = 1

hour = hour + timezone

pitch = 0 
yaw = 0 
roll = 0

maximum_power = 250  # Example maximum power rating of the solar panel in watts
panel_efficiency = 0.85  # Example efficiency of the solar panel

from datetime import datetime, timedelta



batt_mAH = 30000
mAH_remaining = 12000

mA_idle = 0.5  # drain per second
mA_motor = 5  # drain per second
cruise_speed = 15  # m/s

current_altitude = 1000  # metres
landing_altitude = 100 #metres



hours = []
zenith_angles = []
elevation_angles = []
azimuths = []
incidence_angles = []
power_day = []


for hour in range(24):
    for minute in range(60):
        time = datetime(year, month, day, hour, minute, 0)
        sun_coords = sun_calc.calculate_sun_position(latitude, longitude, year, month, day, hour, minute, 0)

        zenith = sun_coords.dZenithAngle
        elevation = 90 - zenith

        if zenith > 90:
            #zenith = 90
            elevation = 0

        incidence_angle = incidence.calculate_incidence_angle(sun_coords.dAzimuth, elevation, pitch, yaw, roll)
        incidence_angles.append(incidence_angle)

        power_day.append(solar_power.calculate_solar_power(incidence_angle, maximum_power, panel_efficiency))
        hours.append(hour + minute / 60)  # Calculate hour with minute fraction
        zenith_angles.append(zenith)
        elevation_angles.append(elevation)
        azimuths.append(sun_coords.dAzimuth)

# Plot the graph
plt.figure(figsize=(12, 6))
plt.plot(hours, zenith_angles, label="Zenith Angle")
plt.plot(hours, elevation_angles, label="Elevation Angle")
plt.plot(hours, azimuths, label="Azimuth")
plt.plot(hours, incidence_angles, label="Incidence")
plt.plot(hours, power_day, label="Power")
plt.xlabel("Hour of the day")
plt.ylabel("Angle (degrees)")
plt.title("Sun Position Throughout the Day")
plt.legend()
plt.xlim(0, 24)  # Set x-axis limits
plt.xticks(range(0, 25, 1))  # Set x-axis tick marks every 4 units
plt.grid(True)
plt.show() 


power_drain.range(batt_mAH, mAH_remaining, mA_idle, mA_motor, cruise_speed)