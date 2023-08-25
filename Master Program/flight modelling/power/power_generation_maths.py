import time
from variables_file import *
import matplotlib as plt
import sun_stuff.sun_calc as sun_calc
import sun_stuff.incidence as incidence
import sun_stuff.solar_power as solar_power

#####################################

class sun_solar_values:
    def __init__(self):
        self.azimuth = 0.0
        self.zenith = 0.0
        self.incidence_angle = 0.0
        self.output_power = 0.0

def power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll):
    output_power = 0
    sun_coords = sun_calc.calculate_sun_position(latitude, longitude, year, month, day, hour, minute, second)

    azimuth = sun_coords.dAzimuth
    zenith = sun_coords.dZenithAngle
    elevation = 90 - zenith

    if zenith > 90:
        #zenith = 90
        elevation = 0
        output_power = 0
    
    if panel_type != "planar":
        for panel_number in panel_segments:
            # some sort of translation thing
            incidence_angle = incidence.calculate_incidence_angle(sun_coords.dAzimuth, elevation, pitch, yaw, roll)
            output_power = solar_power.calculate_solar_power(incidence_angle, maximum_power, panel_efficiency)
        print("code not written yet")
    else:
        incidence_angle = incidence.calculate_incidence_angle(sun_coords.dAzimuth, elevation, pitch, yaw, roll)
        output_power = solar_power.calculate_solar_power(incidence_angle, maximum_power, panel_efficiency)

    #print("Azimuth: %f | Zenith: %f | Incidence: %f | Output Power: %f" %(azimuth, zenith, incidence_angle, output_power))
    
    sun_values = sun_solar_values()

    sun_values.azimuth = azimuth
    sun_values.zenith = zenith
    sun_values.incidence_angle = incidence_angle
    sun_values.output_power = output_power
    return sun_values

def power_through_day(latitude, longitude, year, month, day, pitch, yaw, roll):
    for hour in range(24):
        for minute in range(60):
            sun_values = power_on_wing(latitude, longitude, year, month, day, hour, minute, 0, pitch, yaw, roll)

            power_day.append(sun_values.output_power)
            hours.append(hour + minute / 60)  # Calculate hour with minute fraction
            zenith_angles.append(sun_values.zenith)
            azimuths.append(sun_values.azimuth)

""" 
def print_power_through_day():
    power_through_day(latitude, longitude, year, month, day, pitch, yaw, roll)
"""

    
