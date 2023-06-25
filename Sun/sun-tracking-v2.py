""" 
https://www.pveducation.org/pvcdrom/properties-of-sunlight/suns-position-to-high-accuracy
http://www.psa.es/sdg/archive/SunPos.cpp
http://www.psa.es/sdg/archive/SunPos.h 
"""
import matplotlib.pyplot as plt
import math
import time

pi = math.pi
twopi = 2 * pi
rad = pi / 180
dEarthMeanRadius = 6371.01
dAstronomicalUnit = 149597890

latitude = 40.7128
longitude = -74.0060

year = 2023
month = 6
day = 20
hour = 6
minute = 0
second = 0


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

def sunpos(udtTime, udtLocation, udtSunCoordinates):
    # Calculate the Julian Day
    dDecimalHours = udtTime.dHours + (udtTime.dMinutes + udtTime.dSeconds / 60.0) / 60.0
    liAux1 = (udtTime.iMonth - 14) // 12
    liAux2 = (1461 * (udtTime.iYear + 4800 + liAux1)) // 4 + (367 * (udtTime.iMonth - 2 - 12 * liAux1)) // 12 - (3 * ((udtTime.iYear + 4900 + liAux1) // 100)) // 4 + udtTime.iDay - 32075
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
    dLocalMeanSiderealTime = (dGreenwichMeanSiderealTime * 15 + udtLocation.dLongitude) * rad
    dHourAngle = dLocalMeanSiderealTime - dRightAscension
    dLatitudeInRadians = udtLocation.dLatitude * rad
    dCos_Latitude = math.cos(dLatitudeInRadians)
    dSin_Latitude = math.sin(dLatitudeInRadians)
    dCos_HourAngle = math.cos(dHourAngle)
    udtSunCoordinates.dZenithAngle = math.acos(dCos_Latitude * dCos_HourAngle * math.cos(dDeclination) + math.sin(dDeclination) * dSin_Latitude)
    dY = -math.sin(dHourAngle)
    dX = math.tan(dDeclination) * dCos_Latitude - dSin_Latitude * dCos_HourAngle
    udtSunCoordinates.dAzimuth = math.atan2(dY, dX)
    if udtSunCoordinates.dAzimuth < 0.0:
        udtSunCoordinates.dAzimuth += twopi
    udtSunCoordinates.dAzimuth /= rad

    # Apply the parallax correction
    dParallax = (dEarthMeanRadius / dAstronomicalUnit) * math.sin(udtSunCoordinates.dZenithAngle)
    udtSunCoordinates.dZenithAngle = (udtSunCoordinates.dZenithAngle + dParallax) / rad

    # Print the outputs
    print("Coordinates: %.5f : %.5f" %(latitude, longitude))
    print("Time: %i:%.2i:%.2i:%.2i:%.2i:%.2i" %(year, month, day, hour, minute, second))
    print("Zenith Angle: ", udtSunCoordinates.dZenithAngle)
    print("Azimuth: ", udtSunCoordinates.dAzimuth)

    return udtSunCoordinates

# Example usage
time = cTime(year, month, day, hour, minute, second)  # Starting time
location = cLocation(longitude, latitude)  # Example location (New York City)

# Calculate zenith and azimuth for each hour of the day
hours = []
zenith_angles = []
azimuths = []

sun_coords = cSunCoordinates()
sunpos(time, location, sun_coords)

"""


for hour in range(24):
    time.dHours = hour
    sun_coords = cSunCoordinates()
    sunpos(time, location, sun_coords)
    hours.append(hour)
    zenith_angles.append(sun_coords.dZenithAngle)
    azimuths.append(sun_coords.dAzimuth)

# Plot the graph
plt.figure(figsize=(12, 6))
plt.plot(hours, zenith_angles, label="Zenith Angle")
plt.plot(hours, azimuths, label="Azimuth")
plt.xlabel("Hour of the day")
plt.ylabel("Angle (degrees)")
plt.title("Sun Position Throughout the Day")
plt.legend()
plt.grid(True)
plt.show()

"""