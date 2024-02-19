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

def plot_sun_position(year):
    latitudes = list(range(-90, 91, 10))
    hours = []
    zenith_angles = []
    elevation_angles = []
    azimuths = []
    latitude_values = []

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 8), subplot_kw={'projection': '3d'})

    days_of_year = [79, 172, 264, 355]  # Equinoxes and Solstices
    date_labels = ["Spring Equinox", "Summer Solstice", "Fall Equinox", "Winter Solstice"]

    for j, day_of_year in enumerate(days_of_year):
        for i, latitude in enumerate(latitudes):
            for hour in range(24):
                for minute in range(60):
                    time = datetime(year, 1, 1, hour, minute, 0) + timedelta(days=day_of_year - 1)
                    sun_coords = calculate_sun_position(latitude, 0, year, time.month, time.day, hour, minute, 0)
                    hours.append(hour + minute / 60)  # Calculate hour with minute fraction
                    zenith_angles.append(sun_coords.dZenithAngle)
                    elevation_angles.append(sun_coords.dElevationAngle)
                    azimuths.append(sun_coords.dAzimuth)
                    latitude_values.append(latitude)

                    # Add NaN to create a gap between 24 and 0 hours for each latitude
                    if hour == 23 and minute == 59 and i < len(latitudes) - 1:
                        hours.extend([np.nan, np.nan])
                        zenith_angles.extend([np.nan, np.nan])
                        elevation_angles.extend([np.nan, np.nan])
                        azimuths.extend([np.nan, np.nan])
                        latitude_values.extend([latitude, latitude_values[-1]])

        # Plot the lines, skipping NaN values
        ax1.plot(latitude_values, hours, zenith_angles, label=f'{date_labels[j]} - Zenith', linestyle='-')
        ax2.plot(latitude_values, hours, elevation_angles, label=f'{date_labels[j]} - Elevation', linestyle='-')
        ax3.plot(latitude_values, hours, azimuths, label=f'{date_labels[j]} - Azimuth', linestyle='-')

        # Reset lists for the next iteration
        hours, zenith_angles, elevation_angles, azimuths, latitude_values = [], [], [], [], []

    ax1.set_title("Zenith Angle Throughout the Year")
    ax1.set_xlabel("Latitude")
    ax1.set_ylabel("Hour of the day")
    ax1.set_zlabel("Angle (degrees)")
    ax1.set_xticks(range(-90, 91, 10))
    ax1.set_yticks(range(0, 25, 4))
    ax1.legend()
    ax1.grid(True)

    ax2.set_title("Elevation Angle Throughout the Year")
    ax2.set_xlabel("Latitude")
    ax2.set_ylabel("Hour of the day")
    ax2.set_zlabel("Angle (degrees)")
    ax2.set_xticks(range(-90, 91, 10))
    ax2.set_yticks(range(0, 25, 4))
    ax2.legend()
    ax2.grid(True)

    ax3.set_title("Azimuth Angle Throughout the Year")
    ax3.set_xlabel("Latitude")
    ax3.set_ylabel("Hour of the day")
    ax3.set_zlabel("Angle (degrees)")
    ax3.set_xticks(range(-90, 91, 10))
    ax3.set_yticks(range(0, 25, 4))
    ax3.legend()
    ax3.grid(True)

    plt.show()

# Example usage for the year 2023
plot_sun_position(2023)


