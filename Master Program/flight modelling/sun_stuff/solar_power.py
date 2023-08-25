import math

def calculate_solar_power(incidence_angle, maximum_power, efficiency):
    # Calculate the effective power factor based on the sine of the incidence angle
    effective_power_factor = math.cos(math.radians(incidence_angle))

    # Calculate the power on the solar panel
    power = maximum_power * efficiency * effective_power_factor

    """ print("effective_power_factor: ", effective_power_factor)
    print("efficiency: ", efficiency)
    print("Max Power: ", maximum_power) """

    return power


