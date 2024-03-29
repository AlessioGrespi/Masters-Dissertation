from variables_file import *
import math

####################

def forces_of_flight(velocity, wing_area, lift_co, drag_co, cross_section_area, weight):

    lift = 0.5 * atmo_density * pow(velocity, 2) * wing_area * lift_co
    drag = 0.5 * atmo_density * pow(velocity, 2) * cross_section_area * drag_co
    thrust = drag

    return lift, drag, thrust
    """ 
    if acceleration == 0:
    else:
        thrust = (drag + weight * acceleration) / motor_efficiency_factor 
    """
    
def min_for_flight(weight, wing_area, lift_co, drag_co, cross_section_area):
    v_min = math.sqrt((2 * weight) / (atmo_density * wing_area * lift_co))
    lift, drag, thrust = forces_of_flight(v_min, wing_area, lift_co, drag_co, cross_section_area, weight)

    return v_min, lift, drag, thrust

def motor_LUT():
    # idk how to do this -> motor power is output
    forces_of_flight()

def consumption_rate(motor_power): # P = IV
    power_consumption = motor_power + (A_idle * 5)
    return power_consumption

print(consumption_rate(motor_power))