import sun_stuff.solar_power as sp
from variables_file import maximum_power, panel_efficiency, weight, wing_area, lift_co, drag_co, cross_section_area
import matplotlib.pyplot as plt
import power.power_consumption_maths
from matplotlib.ticker import MultipleLocator
import matplotlib.cm as cm
import numpy as np

def power_incidence_angle(): #Incidence Angle on Panel (x), Power output (y)
    powers = []
    angles = []
    for angle in range (37):
        angle *= 5
        angle -= 90
        power = sp.calculate_solar_power(angle, maximum_power, panel_efficiency)
        powers.append(power)
        angles.append(angle)

    plt.plot(angles, powers)
    plt.xlabel('Incidence Angle (degrees)')
    plt.ylabel('Solar Power (W)')
    plt.title('Solar Power vs. Incidence Angle')
    plt.xlim(-90, 90)
        # Set ticks at every 15 degrees on the x-axis
    """     x_major_locator = MultipleLocator(15)
    plt.gca().xaxis.set_major_locator(x_major_locator) """

    plt.grid(True)
    plt.show()


def min_speed_payload():
    min_speeds = []
    lifts = []
    drags = []
    thrusts = []
    weights = []
    ratio_weights = []
    ratio_ld = []
    wings = []

    for wing_area in range(20):
        wing_area += 1
        wing_area *= 0.2
        

        for payload_weight in range(20):
            payload_weight *= 100
            payload_weight /= 1000
            v_min, lift, drag, thrust = power.power_consumption_maths.min_for_flight(weight + payload_weight, wing_area, lift_co, drag_co, cross_section_area)
        
            ratio = payload_weight / (weight + payload_weight)
            wings.append(wing_area)  # Moved outside the inner loop
            weights.append(weight + payload_weight)
            min_speeds.append(v_min)
            lifts.append(lift)
            drags.append(drag)
            thrusts.append(thrust * 1000)
            ratio_weights.append(ratio)
            ratio_ld.append(lift / drag)

    # Create a color map for the wing area values
    cmap = cm.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(wings)))

    # Plot the data points with the color scale representing wing area values
    plt.scatter(weights, min_speeds, c=wings, cmap='viridis', edgecolors='k', alpha=0.7)
    plt.xlabel('Overall Weight (kg)')
    plt.ylabel('Minimum Speeds (m/s)')
    plt.title('Minimum thrust required')
    plt.colorbar(label='Wing Area (m^2)')

    plt.grid(True)
    plt.show()
#power_incidence_angle()

min_speed_payload()