import matplotlib.pyplot as plt
from variables_file import *
import power.power_generation_maths as gen
import power.power_consumption_maths as con

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
