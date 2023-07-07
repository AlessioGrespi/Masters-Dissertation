from variables_file import *
import power_consumption_maths
import power_generation_maths
import time


def basic_range():
    power_consumption = power_consumption_maths.consumption_rate(motor_power)

    n = (batt_WattHours * 60) / power_consumption

    time_rem = time.strftime("%H:%M:%S", time.gmtime(n))
    print("%.2f W" % (power_consumption))
    print("Battery Capacity: %.2f Wh" % (batt_WattHours))
    print(time_rem)

def glider_range(current_altitude, landing_altitude):
    glide_dist_left = ((current_altitude-landing_altitude)*glide_ratio)/1000


def range_left(batt_mAH, mAH_remaining, motor_power, cruise_speed):

    power_drain_sec = power_consumption_maths.consumption_rate(motor_power)
    power_gen_sec = 0  # config later

    n = (mAH_remaining + power_gen_sec) / power_drain_sec  # seconds

    reserve = (batt_mAH * (safety_factor / 100)) / power_drain_sec

    safe_n = n - reserve

    dist_left = (safe_n * cruise_speed) / 1000
    dist_reserve = (reserve * cruise_speed) / 1000

    if (dist_left <= 0):
        dist_reserve = (n * cruise_speed) / 1000
        dist_left = 0

    if (safe_n <= 0):
        reserve_time = time.strftime("%H:%M:%S", time.gmtime(n))
        safe_n = 0
    else:
        reserve_time = time.strftime("%H:%M:%S", time.gmtime(reserve))

    absolute_time = time.strftime("%H:%M:%S", time.gmtime(n))
    safe_time = time.strftime("%H:%M:%S", time.gmtime(safe_n))


"""     print()
    print("Time remaining: ", safe_time)
    print("Reserve time remaining: ", reserve_time)
    print("Absolute time remaining: ", absolute_time)
    print()
    print("Range left: %.2f km" % dist_left)
    print("Reserve Range: %.2f km" % dist_reserve)
    print()
    print("mAH remaining: ", mAH_remaining) """
