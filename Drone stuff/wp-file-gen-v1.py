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
            "points": [],
            "version": 2
        },
        "version": 1
    }
    return data

def generate_items():
    # Generate and return the items dynamically
    items = []
    coordinates = [
        (51.42371552, -2.6699811),
        (51.42347705, -2.66936391),
        (51.42307697, -2.6697086),
        (51.42278793, -2.67116731),
        (51.42293951, -2.67192164),
        (51.42334326, -2.67174357),
        (51.42352416208575, -2.6710625386167237)
    ]
    for index, (latitude, longitude) in enumerate(coordinates, start=1):
        item = {
            "AMSLAltAboveTerrain": None,
            "Altitude": 50,
            "AltitudeMode": 1,
            "autoContinue": True,
            "command": 16,
            "doJumpId": index,
            "frame": 3,
            "params": [0, 0, 0, None, latitude, longitude, 50],
            "type": "SimpleItem"
        }
        items.append(item)
    return items

def generate_home_position():
    # Generate and return the planned home position dynamically
    home_position = [51.42346581, -2.67132013, 47.27555199998217]
    return home_position

# Specify the file path
file_path = "output.json"

# Generate data
data = generate_data()

# Write data to JSON file
with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file created successfully.")
