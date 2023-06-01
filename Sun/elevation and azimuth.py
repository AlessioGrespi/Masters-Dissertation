import math

# Constants
phi = 14  # Latitude 
d = 260  # Day of the year
LT = 7  # Time in hours
long = 30 # longitude
timezone = 1

# Equation 1
delta = 23.45 * math.sin(math.radians(((360 / 365) * (d - 81))))

# Equation 2
""" 
if long > 0:
    long = long - 7.5
else:
    long = long + 7.5


LSTM = round((long) / 15)*15 """

LSTM = 15 * (0+timezone)


B = math.radians((360/365) * (d-81))
EoT = (9.87*math.sin(2*B))+(-7.53*math.cos(B))+(-1.5*math.sin(B))
TC = 4*(long - LSTM) + EoT
LST = LT + (TC / 60)

gamma = 15 * (LST - 12)

# Equation 3
alpha = math.degrees(math.asin((math.sin(math.radians(delta)) * math.sin(math.radians(phi))) + (math.cos(math.radians(delta)) * math.cos(math.radians(phi)) * math.cos(math.radians(gamma)))))

print("delta =", delta)
print("gamma =", gamma)
print("alpha/elevation =", alpha)
print("EoT =", EoT)
print("LST =", LST)
print("LSTM =",LSTM)


argument = ((math.sin(math.radians(delta)) * math.cos(math.radians(phi))) - (math.cos(math.radians(delta)) * math.sin(math.radians(phi)) * math.cos(math.radians(gamma)))) / math.cos(math.radians(alpha))

beta = math.degrees(math.acos(argument))
 

print("beta/azimuth =", beta)


# Convert angles to degrees
# delta = math.degrees(delta)
# gamma = math.degrees(gamma)
# alpha = math.degrees(alpha)
# beta = math.degrees(beta)

# Print the results


