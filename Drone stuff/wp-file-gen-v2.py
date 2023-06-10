# Print WP to JSON
#
# The script allows one to generate a complete wp path plan with rally points that can then be uploaded to a ArduPilot flight controller.
#
# Example file was generated with QGroundControl and then the raw text was analysed in order to then generate the code to write the script. 
# Waypoints can be generated dynamically from an array.
#
# Contact: alessiogrespi@gmail.com
# Last Edit: 10/6/23 - Commenting and clarity of code. 

import json

def generate_data():
    # Generate and return the data structure dynamically
    data = {
        "fileType": "Plan",  # Specifies the type of file being generated
        "geoFence": {
            "circles": [],  # List of circle geo-fence items
            "polygons": [],  # List of polygon geo-fence items
            "version": 2  # Geo-fence data structure version
        },
        "groundStation": "QGroundControl",  # Specifies the ground control station
        "mission": {
            "cruiseSpeed": 15,  # Speed at which the vehicle cruises between waypoints
            "firmwareType": 3,  # Type of firmware running on the vehicle
            "globalPlanAltitudeMode": 1,  # Altitude mode for the global plan
            "hoverSpeed": 5,  # Speed at which the vehicle hovers at waypoints
            "items": generate_items(),  # List of mission items
            "plannedHomePosition": generate_home_position(),  # Planned home position coordinates
            "vehicleType": 1,  # Type of vehicle
            "version": 2  # Mission data structure version
        },
        "rallyPoints": {
            "points": generate_rally_points(),  # List of rally point coordinates
            "version": 2  # Rally point data structure version
        },
        "version": 1  # Version of the generated file
    }
    return data

def generate_items():
    # Generate and return the items dynamically
    items = []

    # Takeoff type
    takeoff_item = {
        "AMSLAltAboveTerrain": None,
        "Altitude": 50,
        "AltitudeMode": 1,
        "autoContinue": True,
        "command": 22,  # Command for takeoff
        "doJumpId": 1,
        "frame": 3,
        "params": [15, 0, 0, 0, 51.54545844, -0.1282961, 50],  # Parameters for the takeoff command
        "type": "SimpleItem"
    }
    items.append(takeoff_item)

    # Waypoints
    waypoints = [
        [51.54603448, -0.12726251],
        [51.54594838, -0.12597681],
        [51.54501561, -0.1255026],
        [51.54455779, -0.12567218],
        [51.54409757, -0.12728103]
    ]

    for index, waypoint in enumerate(waypoints, start=2):
        waypoint_item = {
            "AMSLAltAboveTerrain": None,
            "Altitude": 50,
            "AltitudeMode": 1,
            "autoContinue": True,
            "command": 16,  # Command for waypoint
            "doJumpId": index,
            "frame": 3,
            "params": [0, 0, 0, None, waypoint[0], waypoint[1], 50],  # Parameters for the waypoint command
            "type": "SimpleItem"
        }
        items.append(waypoint_item)

    # Landing Pattern
    landing_pattern_item = {
        "altitudesAreRelative": True,
        "complexItemType": "fwLandingPattern",
        "landCoordinate": [51.54531029572302, -0.1284484227229825, 0],  # Landing coordinate
        "landingApproachCoordinate": [51.54435042078925, -0.1289297728550751, 40],  # Approach coordinate
        "loiterClockwise": True,  # Direction of loitering
        "loiterRadius": 50,  # Radius of loitering
        "stopTakingPhotos": False,  # Specifies whether to stop taking photos
        "stopVideoPhotos": False,  # Specifies whether to stop video photos
        "type": "ComplexItem",
        "useLoiterToAlt": True,  # Specifies whether to use loiter to altitude
        "valueSetIsDistance": True,  # Specifies whether the value set is distance
        "version": 2  # Landing pattern data structure version
    }
    items.append(landing_pattern_item)

    return items

def generate_home_position():
    # Generate and return the planned home position dynamically
    home_position = [51.54572948637875, -0.12784319524200782, 50.10484157727525]  # Home position coordinates
    return home_position

def generate_rally_points():
    # Generate and return the rally points dynamically
    rally_points = [
        [51.54207272, -0.13584547, 50],  # Rally point 1 coordinates
        [51.55072584, -0.13076061, 50]  # Rally point 2 coordinates
    ]
    return rally_points

# Specify the file path
file_path = "output.json"

# Generate data
data = generate_data()

# Write data to JSON file
with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)  # Dump data to JSON file with indentation

print("JSON file created successfully.")

# The initial comment block describes the purpose of the script, which is to generate a waypoint path plan with rally points for an ArduPilot flight controller. It mentions that the example file was generated using QGroundControl, and the script allows dynamic generation of waypoints from an array.
# The comment block with contact information and last edit date provides relevant details about the script's author and the last time it was modified.
# Comments within the generate_data() function explain the structure and purpose of each component in the data dictionary.
# Comments within the generate_items() function describe the different types of mission items being generated, such as takeoff, waypoints, and landing pattern. They also provide details about the parameters and properties of each item.
# Comments within the generate_home_position() and generate_rally_points() functions describe the purpose of these functions and the coordinates they generate.
# The comment above the file_path variable specifies the file path where the generated JSON file will be saved.
# The comment before the data = generate_data() line explains that the data is being generated dynamically using the generate_data() function.
# The comment before the JSON file writing section explains that the data will be written to a JSON file with indentation.
# The final comment indicates that the JSON file was created successfully.