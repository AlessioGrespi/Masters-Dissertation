# Sun Azimuth and Elevation
#
# This code is used to calculate the elevation and azimuth of the Sun at any posiiton on the earth. 
# Elevation is the angle above the horizon and azimuth is the angle of the sun from North. 
# Axial tilt and time of year is accounted for in the following calculations.
#
# Calculations based on information found here:
# https://www.pveducation.org/pvcdrom/properties-of-sunlight/the-suns-position 
# https://www.pveducation.org/pvcdrom/properties-of-sunlight/elevation-angle
#
# TODO:
# - Check accuracy of model against multiple sources
# - Make model function without need for timezone information.
# - Clean up code 
#
# Contact: alessiogrespi@gmail.com
# Last Edit: 8/6/23 - Commenting and clarity of code. 

# Import necessary libraries
import math

# Set Constants/Variables
latitude = 89       # Latitude 
longitude = 10      # Longitude
day = 80           # Day of the year
LT = 10              # (Local Clock) Time in hours
timezone = 1        # Timezone in which the drone is operating in

# Other variable names:
phi = latitude

# Calculate the current axial tilt of the earth (declination). Max tilt is 23.45˚, equation is essentially: 
# max tilt * sin((360/365)*(difference between current day and spring equinox ~20th March))
declination = 23.45 * math.sin(math.radians(((360 / 365) * (day - 81)))) 
delta = declination

# LSTM = Local Solar Time Meridian: Longitude of the current timezone
LSTM = 15 * (0+timezone) 

# EoT = Equation of time, accounts for the earth's wobble when spinning on its axis
B = math.radians((360/365) * (day-81))
EoT = (9.87*math.sin(2*B))+(-7.53*math.cos(B))+(-1.5*math.sin(B)) 

# TC = Time Correction factor, accounts for LST variation due to longitudinal variations within a timezone and the aforementioned EoT above.
TC = 4*(longitude - LSTM) + EoT

# LST = Local Solar Time: The time of day with respect to the sun, ignoring time zone based adjustments. 
LST = LT + (TC / 60)

# HRA = Hour Angle: Converts local solar time into the number of degrees transited through the sky by the sun. 
# There is 15˚ per hour. Noon is zero degrees, morning is negative, afternoon is positive.
HRA = 15 * (LST - 12)
gamma = HRA

# Elevation is the angle at which the sun is above the horizon, shown as alpha in some examples.
elevation = math.degrees(math.asin((math.sin(math.radians(declination)) * math.sin(math.radians(latitude))) + (math.cos(math.radians(declination)) * math.cos(math.radians(latitude)) * math.cos(math.radians(HRA)))))
alpha = elevation

print("Declination =", declination)
print("Hour Angle: ", HRA)
print("Elevation: ", elevation)
print("EoT: ", EoT)
print("LST: ", LST)
print("LSTM: ",LSTM)

# Azimuth is the angle the sun is with respect to north.
azimuth = math.degrees(math.acos(((math.sin(math.radians(declination)) * math.cos(math.radians(latitude))) - (math.cos(math.radians(declination)) * math.sin(math.radians(latitude)) * math.cos(math.radians(HRA)))) / math.cos(math.radians(elevation))))
print("azimuth =", azimuth)

# # Sunrise and senset calculations
# sunrise = 12 - ((1 / pow(15,0)) * math.acos(-math.tan(math.radians(phi))*math.tan(math.radians(delta))))-(TC/60)
# sunset = 12 + ((1 / pow(15,0)) * math.degrees(math.acos(-(math.tan(math.radians(phi))*math.tan(math.radians(delta))))))-(TC/60)

# print("Sunrise: ", sunrise)
# print("Sunset: ", sunset)