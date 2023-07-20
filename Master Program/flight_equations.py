import math
from variables_file import *

lift = weight * 9.81
#drag = thrust

lift_co = lift / (0.5 * atmo_density * pow(velocity, 2) * wing_area)
v_min = math.sqrt((2 * weight) / (atmo_density * wing_area * lift_co))

#drag_co = drag / (0.5 * atmo_density * pow(velocity, 2) * cross_section_area)

print(wing_area)
print(lift_co)
print(v_min)