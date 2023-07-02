import time

glide_ratio = 45  # horizontal distance per metre of altitude
safety_factor = 20  # percent
motor_efficiency_factor = 80

def range(batt_mAH, mAH_remaining, mA_idle, mA_motor, cruise_speed):
    mA_motor = mA_motor * (100/motor_efficiency_factor)

    power_drain_sec = (mA_idle + mA_motor)
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



    print()
    print("Time remaining: ", safe_time)
    print("Reserve time remaining: ", reserve_time)
    print("Absolute time remaining: ", absolute_time)
    print()
    print("Range left: %.2f km" % dist_left)
    print("Reserve Range: %.2f km" % dist_reserve)
    print()
    print("mAH remaining: ", mAH_remaining)




def current_range(current_altitude, landing_altitude, batt_mAH, mAH_remaining, mA_idle, mA_motor, cruise_speed):

    glide_dist_left = ((current_altitude-landing_altitude)*glide_ratio)/1000
    print("Unpowered distance left: %.2f km" % glide_dist_left)

    range(batt_mAH, mAH_remaining, mA_idle, mA_motor, cruise_speed)

    total_range = glide_dist_left + dist_left 

    print("Range Remaining: ", total_range)




#def initial_solar_range():