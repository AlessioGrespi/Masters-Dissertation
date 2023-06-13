import time

batt_mAH = 30000
mAH_remaining = 12000

mA_idle = 0.5  # drain per second
mA_motor = 5  # drain per second
cruise_speed = 15  # m/s
safety_factor = 20  # percent
current_altitude = 1000  # metres
landing_altitude = 100 #metres
glide_ratio = 45  # horizontal distance per metre of altitude
# drag =
# thrust =
# thrust_curve =
motor_efficiency_factor = 80

glide_dist_left = ((current_altitude-landing_altitude)*glide_ratio)/1000

print("Unpowered distance left: %.2f km" % glide_dist_left)

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
