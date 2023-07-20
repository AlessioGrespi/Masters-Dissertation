import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from variables_file import atmo_density, lift_co, drag_co, cross_section_area, wing_area


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
