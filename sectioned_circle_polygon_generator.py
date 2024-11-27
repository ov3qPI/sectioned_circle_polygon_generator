import sys
import math
import simplekml
import numpy as np

# Function to parse command-line arguments
def parse_arguments():
    if len(sys.argv) != 5:
        print("Usage: python3 sectioned_circle_polygon_generator.py <lat> <long> <radius> <divisions>")
        sys.exit(1)

    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    radius_str = sys.argv[3]
    divisions = int(sys.argv[4])

    # Extracting radius from radius string (assuming format is R<number>)
    if radius_str.startswith('R'):
        radius = float(radius_str[1:])
    else:
        raise ValueError("Invalid radius format. Use R<number> for radius.")

    return latitude, longitude, radius, divisions

# Function to generate points in a circle
def generate_circle_points(lat, lon, radius_km, num_points=360):
    points = []
    for i in range(num_points):
        angle_rad = math.radians(float(i))
        dlat = radius_km / 6371.0 * math.degrees(math.cos(angle_rad))
        dlon = radius_km / 6371.0 * math.degrees(math.sin(angle_rad)) / math.cos(math.radians(lat))
        points.append((lon + dlon, lat + dlat))
    return points

# Function to generate division lines
def generate_division_lines(lat, lon, radius_km, divisions):
    lines = []
    for i in range(divisions):
        angle_rad = math.radians(i * 360 / divisions)
        dlat = radius_km / 6371.0 * math.degrees(math.sin(angle_rad))
        dlon = radius_km / 6371.0 * math.degrees(math.cos(angle_rad)) / math.cos(math.radians(lat))
        lines.append([(lon, lat), (lon + dlon, lat + dlat)])
    return lines

if __name__ == '__main__':
    try:
        # Parse arguments
        latitude, longitude, radius, divisions = parse_arguments()

        # Validate divisions
        if divisions not in [4, 8, 16, 32, 64]:
            raise ValueError("Divisions must be one of the following: 4, 8, 16, 32, 64.")

        # Generate KML
        kml = simplekml.Kml()

        # Add circular polygon to KML
        circle_points = generate_circle_points(latitude, longitude, radius)
        pol = kml.newpolygon(name="Circular Polygon")
        pol.outerboundaryis = circle_points
        pol.style.polystyle.fill = 0  # No fill
        pol.style.linestyle.color = simplekml.Color.rgb(0, 255, 0)  # Fighter-jet-HUD green outline
        pol.style.linestyle.width = 2

        # Add division lines to KML
        lines = generate_division_lines(latitude, longitude, radius, divisions)
        for idx, line_points in enumerate(lines):
            lin = kml.newlinestring(name=f"Division Line {idx + 1}")
            lin.coords = line_points
            lin.style.linestyle.width = 2
            lin.style.linestyle.color = simplekml.Color.rgb(0, 255, 0)  # Fighter-jet-HUD green lines

        # Save KML file
        kml_filename = f"{latitude}_{longitude}_R{radius}_D{divisions}.kml"
        kml.save(kml_filename)
        print(f"KML file '{kml_filename}' has been successfully created.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
