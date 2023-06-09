import json

def generate_data():
    # Generate and return the data structure dynamically
    data = {
        "fileType": "Plan",
        "geoFence": {
            "circles": [],
            "polygons": [],
            "version": 2
        },
        "groundStation": "QGroundControl",
        "mission": {
            "cruiseSpeed": 15,
            "firmwareType": 3,
            "globalPlanAltitudeMode": 1,
            "hoverSpeed": 5,
            "items": generate_items(),
            "plannedHomePosition": generate_home_position(),
            "vehicleType": 1,
            "version": 2
        },
        "rallyPoints": {
            "points": generate_rally_points(),
            "version": 2
        },
        "version": 1
    }
    return data

def generate_items():
    # Generate and return the items dynamically
    items = []

    # Takeoff
    takeoff_item = {
        "AMSLAltAboveTerrain": None,
        "Altitude": 50,
        "AltitudeMode": 1,
        "autoContinue": True,
        "command": 22,
        "doJumpId": 1,
        "frame": 3,
        "params": [15, 0, 0, 0, 51.54545844, -0.1282961, 50],
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
            "command": 16,
            "doJumpId": index,
            "frame": 3,
            "params": [0, 0, 0, None, waypoint[0], waypoint[1], 50],
            "type": "SimpleItem"
        }
        items.append(waypoint_item)

    # Landing Pattern
    landing_pattern_item = {
        "altitudesAreRelative": True,
        "complexItemType": "fwLandingPattern",
        "landCoordinate": [51.54531029572302, -0.1284484227229825, 0],
        "landingApproachCoordinate": [51.54435042078925, -0.1289297728550751, 40],
        "loiterClockwise": True,
        "loiterRadius": 50,
        "stopTakingPhotos": False,
        "stopVideoPhotos": False,
        "type": "ComplexItem",
        "useLoiterToAlt": True,
        "valueSetIsDistance": True,
        "version": 2
    }
    items.append(landing_pattern_item)

    return items

def generate_home_position():
    # Generate and return the planned home position dynamically
    home_position = [51.54572948637875, -0.12784319524200782, 50.10484157727525]
    return home_position

def generate_rally_points():
    # Generate and return the rally points dynamically
    rally_points = [
        [51.54207272, -0.13584547, 50],
        [51.55072584, -0.13076061, 50]
    ]
    return rally_points

# Specify the file path
file_path = "output.json"

# Generate data
data = generate_data()

# Write data to JSON file
with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file created successfully.")
