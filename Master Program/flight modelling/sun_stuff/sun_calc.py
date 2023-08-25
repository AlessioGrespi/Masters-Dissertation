""" 
Accurately calculate zenith and azimuth of the sun

https://www.pveducation.org/pvcdrom/properties-of-sunlight/suns-position-to-high-accuracy
http://www.psa.es/sdg/archive/SunPos.cpp
http://www.psa.es/sdg/archive/SunPos.h 
TODO:
- Add timezone adjustment
- Declare sunrise sunset
"""

import matplotlib.pyplot as plt
import math

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


from datetime import datetime, timedelta

def plot_sun_position(latitude, longitude, year, month, day):
    hours = []
    zenith_angles = []
    elevation_angles = []
    azimuths = []

    for hour in range(24):
        for minute in range(60):
            time = datetime(year, month, day, hour, minute, 0)
            sun_coords = calculate_sun_position(latitude, longitude, year, month, day, hour, minute, 0)
            hours.append(hour + minute / 60)  # Calculate hour with minute fraction
            zenith_angles.append(sun_coords.dZenithAngle)
            elevation_angles.append(sun_coords.dElevationAngle)
            azimuths.append(sun_coords.dAzimuth)

    # Plot the graph
    plt.figure(figsize=(12, 6))
    plt.plot(hours, zenith_angles, label="Zenith Angle")
    plt.plot(hours, elevation_angles, label="Elevation Angle")
    plt.plot(hours, azimuths, label="Azimuth")
    plt.xlabel("Hour of the day")
    plt.ylabel("Angle (degrees)")
    plt.title("Sun Position Throughout the Day")
    plt.legend()
    plt.xlim(0, 24)  # Set x-axis limits
    plt.xticks(range(0, 25, 4))  # Set x-axis tick marks every 4 units
    plt.grid(True)
    plt.show()