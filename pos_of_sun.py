import math
import datetime

def calculate_sun_position(latitude, longitude, date, time):
    # Convert latitude and longitude to radians
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)

    # Get the number of days since January 1, 2000 (J2000 epoch)
    j2000 = datetime.datetime(2000, 1, 1)
    delta = date - j2000
    julian_date = 2451545.0 + delta.days + (time.hour - 12) / 24 + time.minute / 1440 + time.second / 86400

    # Calculate the number of Julian centuries since J2000
    t = (julian_date - 2451545.0) / 36525

    # Calculate the mean solar longitude
    l0 = math.radians(280.46645 + 36000.76983 * t + 0.0003032 * t**2)

    # Calculate the mean solar anomaly
    m = math.radians(357.52910 + 35999.05030 * t - 0.0001559 * t**2 - 0.00000048 * t**3)

    # Calculate the equation of the center
    c = (1.914600 - 0.004817 * t - 0.000014 * t**2) * math.sin(m) + (0.019993 - 0.000101 * t) * math.sin(2 * m) + 0.000290 * math.sin(3 * m)

    # Calculate the ecliptic longitude
    ecliptic_longitude = l0 + c

    # Calculate the obliquity of the ecliptic
    obliquity = math.radians(23.43999 - 0.013 * t)

    # Calculate the right ascension and declination of the sun
    y = math.cos(obliquity) * math.sin(ecliptic_longitude)
    x = math.cos(ecliptic_longitude)
    right_ascension = math.atan2(y, x)
    right_ascension = math.degrees(right_ascension)

    declination = math.asin(math.sin(obliquity) * math.sin(ecliptic_longitude))
    declination = math.degrees(declination)

    # Calculate the local hour angle
    hour_angle = math.radians(15 * (time.hour + time.minute / 60 + time.second / 3600 - 12))

    # Calculate the observer's zenith angle
    sin_latitude = math.sin(latitude)
    cos_latitude = math.cos(latitude)
    sin_declination = math.sin(math.radians(declination))
    cos_declination = math.cos(math.radians(declination))
    cos_hour_angle = math.cos(hour_angle)

    zenith_angle = math.acos(sin_latitude * sin_declination + cos_latitude * cos_declination * cos_hour_angle)
    zenith_angle = math.degrees(zenith_angle)

    # Calculate the azimuth angle
    sin_azimuth = cos_declination * math.sin(hour_angle)
    cos_azimuth = (sin_declination * cos_latitude - cos_declination * sin_latitude * cos_hour_angle)
    azimuth = math.atan2(sin_azimuth, cos_azimuth)
    azimuth = math.degrees(azimuth)

    # Adjust azimuth range from -180 to 180 degrees
    azimuth = (azimuth + 180) % 360 - 180

    # Calculate the altitude angle
    altitude = 90 - zenith_angle

    return altitude, azimuth

# Example usage
latitude = 37.7749  # San Francisco
longitude = -122.4194
date = datetime.date(2023, 5, 24)
time = datetime.time(12, 0, 0)

altitude, azimuth = calculate_sun_position(latitude, longitude, date, time)

print('Altitude:', altitude)
print('Azimuth:', azimuth)
