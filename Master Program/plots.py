import sun_stuff.solar_power as sp
from variables_file import *
import matplotlib.pyplot as plt
import power.power_consumption_maths
from matplotlib.ticker import MultipleLocator
import matplotlib.cm as cm
import numpy as np
import math

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

def lift_co_wingspan():
    speeds = []
    min_speeds = []
    drags = []
    lift_co_values = []

    weight = mass * 9.81

    for lift_co in range(10):
        lift_co += 1
        lift_co /= 10

        v_min = math.sqrt((2 * weight) / (atmo_density * wing_area * lift_co))

        for velocity in range(25):
            drag = 0.5 * atmo_density * pow(velocity, 2) * cross_section_area * drag_co
            drag *= 1000
            drags.append(drag)
            min_speeds.append(v_min)
            speeds.append(velocity)
            lift_co_values.append(lift_co)

    # Convert the lists to numpy arrays for better handling
    speeds = np.array(speeds)
    drags = np.array(drags)
    lift_co_values = np.array(lift_co_values)

    plt.scatter(speeds, drags, c=lift_co_values, cmap='viridis', label='Lift Co')
    plt.xlabel('Speed')
    plt.ylabel('Drag (g)')
    plt.title('Scatter Plot with Lift Co Values')
    plt.colorbar(label='Lift Co')
    
    plt.grid(True)
    plt.legend()
    plt.show()


def sense_plot_time_year(year, pitch, yaw, roll):
    total_power = []
    day_of_year = []

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year_track = 1
    if is_leap_year(year):
        days_in_month[1] = 29  # Update February days to 29 for leap year
    
    for month in range(1, 13):
        for day in range(1, days_in_month[month - 1] + 1):

            print(f"{month:02d}-{day:02d}")

            power_of_day = 0

            for hour in range(24):
                for minute in range(60):
                    for second in range(60):
                       sun_values = power.power_generation_maths.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
                       power_of_day += sun_values.output_power
                       
            total_power.append(power_of_day)
            day_of_year.append(day_of_year_track)
            day_of_year_track += 1

    plt.plot(day_of_year, total_power)
    plt.xlabel("Day of Year")
    plt.ylabel("Total Power Generated")
    plt.title(f"Total Power Generated in {year}")
    plt.grid(True)
    plt.show()


def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

sense_plot_time_year(year, pitch, yaw, roll)

#power_incidence_angle()

#min_speed_payload()

lift_co_wingspan()


def solar_energy_per_unit_mass():
    w_m_squared = pow(0.125, 2) * 3.5

    areas = []
    weights = []
    velocities = []
    max_powers = []

    for velocity in range(10):
        velocity += 1
        velocity *= 5
        print(velocity)
        for mass in range(25):
            mass += 1
            lift = mass * 9.81
            velocities.append(velocity)
            weights.append(lift)
            wing_area_out = (2*lift)/(pow(velocity, 2) * atmo_density * lift_co)
            areas.append(wing_area_out)
            powers =  wing_area_out * w_m_squared
            max_powers.append(powers)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(weights, velocities, max_powers)
    ax.set_xlabel('Weight N')
    ax.set_zlabel('Power W')
    ax.set_ylabel('Velocity m/s')
    plt.show()

def lift_to_drag(): # idk this is wrong
    lifts = []
    drags = []
    velocities = []
    ratios = []

    for velocity in range(10):
        velocity += 1
        velocity *= 5

        lift = 0.5 * atmo_density * pow(velocity, 2) * wing_area * lift_co
        drag = 0.5 * atmo_density * pow(velocity, 2) * cross_section_area * drag_co

        lifts.append(lift)
        drags.append(drag)
        ratios.append(lift / drag)
        velocities.append(velocity)

    plt.plot(velocities, ratios)
    plt.xlabel('Velocity')
    plt.ylabel('Ratio (Lift / Drag)')
    plt.title('Ratio of Lift to Drag vs. Velocity')
    plt.show()

def airspeed_to_drag_dragco():
    drag_cos = []

    for drag_co in range(10):
        drag_co += 1
        drag_co /= 10

        drags = []
        velocities = []

        for velocity in range(10):
            velocity += 1
            velocity *= 5

            drag = 0.5 * atmo_density * pow(velocity, 2) * cross_section_area * drag_co

            drags.append(drag)
            velocities.append(velocity)

        plt.plot(velocities, drags, label=f"Drag Coeff: {drag_co:.1f}")

        drag_cos.append(drag_co)

    plt.xlabel('Velocity')
    plt.ylabel('Drag')
    plt.title('Drag vs. Velocity')
    plt.legend()
    plt.show()

def airspeed_to_drag_dragco():
    drag_cos = []

    for drag_co in range(10):
        drag_co += 1
        drag_co /= 10

        drags = []
        velocities = []

        for velocity in range(10):
            velocity += 1
            velocity *= 5

            drag = 0.5 * atmo_density * pow(velocity, 2) * cross_section_area * drag_co

            drags.append(drag)
            velocities.append(velocity)

        plt.plot(velocities, drags, label=f"Drag Coeff: {drag_co:.1f}")

        drag_cos.append(drag_co)

    plt.xlabel('Velocity')
    plt.ylabel('Drag')
    plt.title('Drag vs. Velocity')
    plt.legend()
    plt.show()

airspeed_to_drag_dragco()

lift_to_drag()

solar_energy_per_unit_mass()


def power_0_24():
    batt_WattHours_Remaining = batt_WattHours
    batt_WattSeconds_Remaining = batt_WattHours_Remaining * 3600

    for hour in range(24):
        for minute in range(60):
            for second in range(60):
                sun_values = gen.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
                power_consumption = con.consumption_rate(motor_power)
                resultant_power = sun_values.output_power - power_consumption
                batt_WattSeconds_Remaining = batt_WattSeconds_Remaining + resultant_power 
                batt_WattHours_Remaining = batt_WattSeconds_Remaining / 3600
                if batt_WattHours_Remaining <= 0:
                    batt_WattHours_Remaining = 0
                #print(power_consumption)
                print("Power Gen: %f W | Power Consumption: %f W | Resultant Power %f W | Ws Remaining: %f Wh" %(sun_values.output_power, power_consumption, resultant_power, batt_WattHours_Remaining))

                hours.append(hour + ((minute*60) + second)/3600)
                power_in.append(sun_values.output_power)
                power_out.append(power_consumption)
                power_day.append(resultant_power)
                Wh_remaining.append(batt_WattHours_Remaining)

    graph(0, 24)

def graph(start_x, end_x):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax1.plot(hours, Wh_remaining, label="Wh Remaining", color='blue')
    ax2.plot(hours, power_day, label="Resultant Power", color='purple')
    ax2.plot(hours, power_in, label="Power Generation", color='green')
    ax2.plot(hours, power_out, label="Power Consumtion", color='red')

    ax1.set_xlabel("Hours")
    ax1.set_ylabel("Wh Remaining", color='blue')
    ax2.set_ylabel("Power Flow", color='red')

    ax1.tick_params(axis='y', colors='blue')
    ax2.tick_params(axis='y', colors='red')

    #Set x-axis limits and gridlines
    ax1.set_xlim(start_x, end_x)
    ax1.set_xticks(range(start_x, end_x, 4))
    ax1.grid(True, linestyle='--')

    # Set y-axis limits
    ax1.set_ylim(0, max(Wh_remaining))

    # Add legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Add dotted line at y=0 for y-axis 2
    ax2.axhline(0, color='black', linestyle='dotted')

    plt.show()

def power_start_end(start_hour, end_hour):
    batt_WattHours_Remaining = batt_WattHours
    batt_WattSeconds_Remaining = batt_WattHours_Remaining * 3600

    for hour in range(start_hour, end_hour + 1):  # Loop from the start hour to the end hour (inclusive)
        for minute in range(60):
            for second in range(60):
                sun_values = gen.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
                power_consumption = con.consumption_rate(motor_power)
                resultant_power = sun_values.output_power - power_consumption
                batt_WattSeconds_Remaining = batt_WattSeconds_Remaining + resultant_power 
                batt_WattHours_Remaining = batt_WattSeconds_Remaining / 3600
                if batt_WattHours_Remaining <= 0:
                    batt_WattHours_Remaining = 0
                #print(power_consumption)
                print("Power Gen: %f W | Power Consumption: %f W | Resultant Power %f W | Ws Remaining: %f Wh" %(sun_values.output_power, power_consumption, resultant_power, batt_WattHours_Remaining))

                hours.append(hour + ((minute*60) + second)/3600)
                power_in.append(sun_values.output_power)
                power_out.append(power_consumption)
                power_day.append(resultant_power)
                Wh_remaining.append(batt_WattHours_Remaining)

    graph(start_hour, end_hour)


def power_start_depleted(start_hour):
    batt_WattHours_Remaining = batt_WattHours
    batt_WattSeconds_Remaining = batt_WattHours_Remaining * 3600

    hour = start_hour
    minute = 0
    second = 0

    while batt_WattHours_Remaining > 0:
        sun_values = gen.power_on_wing(latitude, longitude, year, month, day, hour, minute, second, pitch, yaw, roll)
        power_consumption = con.consumption_rate(motor_power)
        resultant_power = sun_values.output_power - power_consumption
        batt_WattSeconds_Remaining = batt_WattSeconds_Remaining + resultant_power
        batt_WattHours_Remaining = batt_WattSeconds_Remaining / 3600
        if batt_WattHours_Remaining <= 0:
            batt_WattHours_Remaining = 0
        #print(power_consumption)
        print("Power Gen: %f W | Power Consumption: %f W | Resultant Power %f W | Ws Remaining: %f Wh" %(sun_values.output_power, power_consumption, resultant_power, batt_WattHours_Remaining))

        hours.append(hour + ((minute*60) + second)/3600)
        power_in.append(sun_values.output_power)
        power_out.append(power_consumption)
        power_day.append(resultant_power)
        Wh_remaining.append(batt_WattHours_Remaining)

        # Increment time
        second += 1
        if second == 60:
            second = 0
            minute += 1
            if minute == 60:
                minute = 0
                hour += 1

    graph(start_hour, hour + 1)

