### Aircraft Defined Properties
dry_weight = 1.5
wet_weight = 0.5
payload_weight = 0.2
mass = dry_weight + wet_weight + payload_weight
wing_span = 2.4 #metres
wing_chord = 0.3 #metres
wing_area = wing_span * wing_chord #metres squared
cross_section_area = 0.5 #metres squared
glide_ratio = 45  # horizontal distance per metre of altitude
cruise_speed = 15  # m/s

### Power Systems
batt_mAH = 50000
batt_Cells = 8
cell_Voltage = 4.2
batt_Voltage = batt_Cells * cell_Voltage
batt_WattHours = batt_mAH * batt_Voltage / 1000
motor_efficiency_factor = 80
A_idle = 0.5  # drain per second
A_motor = 5  # drain per second
motor_power = 150 # W Dummy value atm

### Solar Systems
maximum_power = 350  # Example maximum power rating of the solar panel in watts
panel_efficiency = 0.85  # Example efficiency of the solar panel
panel_type = "planar"
panel_number = []
panel_segments = 0

### Panel Variables Assuming Sunpower C60 http://eshop.terms.eu/_data/s_3386/files/1379942540-sunpower_c60_bin_ghi.pdf 
panel_efficiency = 1 # efficiency can be ignored as it is already factored in
wppanel = 3.38 # W
# each panel is 125 mm x 125mm
panel_x = 2
panel_y = 8
maximum_power = wppanel * panel_x * panel_y

### Mathematical Constants
atmo_density = 1.225
drag_co = 0.02
lift_co = 0.21750566893424042 #(0.3-0.5)

### Mission parameters
safety_factor = 20  # percent
velocity = 15 #assume ground speed not air speed as model does not account for wind
# take_off =
landing_altitude = 100 #metres

### Time:
year = 2023
month = 6
day = 25
hour = 19
minute = 43
second = 40
timezone = 1

hour = hour + timezone
#add check to ensure not outside 24 hour range

### Live Parameters
pitch = 0 
yaw = 0 
roll = 0

latitude = 51.509865
longitude = -0.118092

#mAH_remaining = 12000

current_altitude = 1000  # metres




### Other maths stuff

hours = []
zenith_angles = []
elevation_angles = []
azimuths = []
incidence_angles = []
power_day = []
Wh_remaining = []
power_out = []
power_in = []