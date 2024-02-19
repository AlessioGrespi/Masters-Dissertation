import matplotlib.pyplot as plt
import math
from tikzplotlib import save as tikz_save
import csv
from datetime import datetime, timedelta
import numpy as np

pi = math.pi
twopi = 2 * pi
rad = pi / 180
dEarthMeanRadius = 6371.01
dAstronomicalUnit = 149597890

class cTime:
    def __init__(self, year, month, day, hours, minutes, seconds):
        self.iYear = year
        self.iMonth = month
        self.iDay = day
        self.dHours = hours
        self.dMinutes = minutes
        self.dSeconds = seconds

class cLocation:
    def __init__(self, longitude, latitude):
        self.dLongitude = longitude
        self.dLatitude = latitude

class cSunCoordinates:
    def __init__(self):
        self.dZenithAngle = 0.0
        self.dAzimuth = 0.0
        self.dElevation = 0.0

def calculate_sun_position(latitude, longitude, year, month, day, hour, minute, second):
    time = cTime(year, month, day, hour, minute, second)
    location = cLocation(longitude, latitude)
    sun_coords = cSunCoordinates()

    # Calculate the Julian Day
    dDecimalHours = time.dHours + (time.dMinutes + time.dSeconds / 60.0) / 60.0
    liAux1 = (time.iMonth - 14) // 12
    liAux2 = (1461 * (time.iYear + 4800 + liAux1)) // 4 + (367 * (time.iMonth - 2 - 12 * liAux1)) // 12 - (3 * ((time.iYear + 4900 + liAux1) // 100)) // 4 + time.iDay - 32075
    dJulianDate = float(liAux2) - 0.5 + dDecimalHours / 24.0

    # Calculate the elapsed Julian Days
    dElapsedJulianDays = dJulianDate - 2451545.0

    # Calculate the ecliptic longitude and obliquity of the ecliptic
    dMeanLongitude = 4.8950630 + 0.017202791698 * dElapsedJulianDays
    dMeanAnomaly = 6.2400600 + 0.0172019699 * dElapsedJulianDays
    dEclipticLongitude = dMeanLongitude + 0.03341607 * math.sin(dMeanAnomaly) + 0.00034894 * math.sin(2 * dMeanAnomaly) - 0.0001134 - 0.0000203 * math.sin(2.1429 - 0.0010394594 * dElapsedJulianDays)
    dEclipticObliquity = 0.4090928 - 6.2140e-9 * dElapsedJulianDays + 0.0000396 * math.cos(2.1429 - 0.0010394594 * dElapsedJulianDays)

    # Calculate the celestial coordinates
    dSin_EclipticLongitude = math.sin(dEclipticLongitude)
    dY = math.cos(dEclipticObliquity) * dSin_EclipticLongitude
    dX = math.cos(dEclipticLongitude)
    dRightAscension = math.atan2(dY, dX)
    if dRightAscension < 0.0:
        dRightAscension += twopi
    dDeclination = math.asin(math.sin(dEclipticObliquity) * dSin_EclipticLongitude)

    # Calculate the local coordinates
    dGreenwichMeanSiderealTime = 6.6974243242 + 0.0657098283 * dElapsedJulianDays + dDecimalHours
    dLocalMeanSiderealTime = (dGreenwichMeanSiderealTime * 15 + location.dLongitude) * rad
    dHourAngle = dLocalMeanSiderealTime - dRightAscension
    dLatitudeInRadians = location.dLatitude * rad
    dCos_Latitude = math.cos(dLatitudeInRadians)
    dSin_Latitude = math.sin(dLatitudeInRadians)
    dCos_HourAngle = math.cos(dHourAngle)
    sun_coords.dZenithAngle = math.acos(dCos_Latitude * dCos_HourAngle * math.cos(dDeclination) + math.sin(dDeclination) * dSin_Latitude)
    dY = -math.sin(dHourAngle)
    dX = math.tan(dDeclination) * dCos_Latitude - dSin_Latitude * dCos_HourAngle
    sun_coords.dAzimuth = math.atan2(dY, dX)
    if sun_coords.dAzimuth < 0.0:
        sun_coords.dAzimuth += twopi
    sun_coords.dAzimuth /= rad

    # Apply the parallax correction
    dParallax = (dEarthMeanRadius / dAstronomicalUnit) * math.sin(sun_coords.dZenithAngle)
    sun_coords.dZenithAngle = (sun_coords.dZenithAngle + dParallax) / rad
    sun_coords.dElevationAngle = 90 - sun_coords.dZenithAngle 

    return sun_coords

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from datetime import datetime

def plot_sun_positions(year, summer_month, summer_day, winter_month, winter_day):
    latitudes = list(range(-90, 91, 10))
    summer_data = get_sun_data(year, summer_month, summer_day, latitudes)
    winter_data = get_sun_data(year, winter_month, winter_day, latitudes)

    # Create separate figures for each subplot
    fig1 = plt.figure(figsize=(6, 6))
    ax1 = fig1.add_subplot(111, projection='3d')

    fig2 = plt.figure(figsize=(6, 6))
    ax2 = fig2.add_subplot(111, projection='3d')

    fig3 = plt.figure(figsize=(6, 6))
    ax3 = fig3.add_subplot(111, projection='3d')

    # Plot for Summer Solstice
    plot_solstice_data(ax1, summer_data, 'zenith_angle', 'red', "Zenith Angle - Summer Solstice", "Summer Solstice")
    plot_solstice_data(ax2, summer_data, 'elevation_angle', 'red', "Elevation Angle - Summer Solstice", "Summer Solstice")
    plot_solstice_data(ax3, summer_data, 'azimuth', 'red', "Azimuth - Summer Solstice", "Summer Solstice")

    # Plot for Winter Solstice
    plot_solstice_data(ax1, winter_data, 'zenith_angle', 'blue', "Zenith Angle - Winter Solstice", "Winter Solstice")
    plot_solstice_data(ax2, winter_data, 'elevation_angle', 'blue', "Elevation Angle - Winter Solstice", "Winter Solstice")
    plot_solstice_data(ax3, winter_data, 'azimuth', 'blue', "Azimuth - Winter Solstice", "Winter Solstice")


    # Set common labels
    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel("Latitude")
        ax.set_ylabel("Hour of the day")
        ax.set_zlabel("Angle (degrees)")
        ax.set_xticks(range(-90, 91, 30))
        ax.set_yticks(range(0, 25, 4))
        ax.grid(True)

    ax1.set_title('Zenith Angle')
    ax2.set_title('Elevation Angle')
    ax3.set_title('Azimuth Angle')

    # Add legend to each subplot
    ax1.legend()
    ax2.legend()
    ax3.legend()

    plt.show()

def get_sun_data(year, month, day, latitudes):
    data = {'latitude': [], 'hour': [], 'zenith_angle': [], 'elevation_angle': [], 'azimuth': []}

    for i, latitude in enumerate(latitudes):
        for hour in range(24):
            for minute in range(60):
                time = datetime(year, month, day, hour, minute, 0)
                sun_coords = calculate_sun_position(latitude, 0, year, month, day, hour, minute, 0)
                data['latitude'].append(latitude)
                data['hour'].append(hour + minute / 60)  # Calculate hour with minute fraction
                data['zenith_angle'].append(sun_coords.dZenithAngle)
                data['elevation_angle'].append(sun_coords.dElevationAngle)
                data['azimuth'].append(sun_coords.dAzimuth)

                # Add NaN to create a gap between 24 and 0 hours for each latitude
                if hour == 23 and minute == 59 and i < len(latitudes) - 1:
                    for key in data.keys():
                        data[key].extend([np.nan, np.nan])

    return data

def plot_solstice_data(ax, season, data, color, title, label):
    ax.plot(season['latitude'], season['hour'], season[data], color=color, linewidth=1, label=label)
    #ax.set_title(title)

# Plot for both Summer and Winter Solstices
plot_sun_positions(2023, 6, 22, 12, 21)
