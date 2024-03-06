# map_utils.py
import folium
from folium.plugins import MarkerCluster
import csv
import webbrowser
import pandas as pd


def parse_csv(file_path):
    access_points = []
    
    # Fetches Marauder Wardriving data from CSV file
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                mac_address = row[0]
                signal_strength = int(row[5])
                ssid = row[1]
                lat = float(row[6])
                lon = float(row[7])
                access_points.append((mac_address, ssid, lat, lon, signal_strength))
            except (ValueError, IndexError):
                # Skip lines with invalid format or missing values
                pass
    return access_points


def create_map(access_points):
    # Sort the data based on signal strength
    access_points.sort(key=lambda x: x[-1])

    # Create a Leaflet map
    map_center = [access_points[0][2], access_points[0][3]]
    mymap = folium.Map(location=map_center, zoom_start=15)

    # Add a MarkerCluster layer for the markers
    marker_cluster = MarkerCluster().add_to(mymap)

    # Add markers for each access point to the MarkerCluster layer
    for ap in access_points:
        popup_text = f"MAC: {ap[0]}<br>SSID: {ap[1]}<br>Signal Strength: {ap[4]}"
        marker = folium.Marker(location=[ap[2], ap[3]], popup=popup_text)
        marker.add_to(marker_cluster)

    # Add LayerControl to switch between layers
    folium.LayerControl().add_to(mymap)

    # Save the map as an HTML file
    mymap.save("wardriving_map.html")
    
    # Open the generated HTML file in the default web browser
    webbrowser.open("wardriving_map.html")


def create_summary_csv(access_points):
    # Extract information after the pipe symbol and format MAC address
    formatted_data = [
        [str(item).split('|')[1].split(',')[0].strip() if len(str(item).split('|')) > 1 else str(item).strip() for item in ap]
        for ap in access_points
    ]

    # Sort DataFrame by the "MAC" column
    columns = ["MAC", "SSID", "Latitude", "Longitude", "Signal Strength"]
    df = pd.DataFrame(formatted_data, columns=columns)
    
    # Set the width for each column
    column_width = 25

    # Save DataFrame to a new formatted text file with fixed width
    formatted_content = df.to_string(index=False, justify='left', col_space=column_width)

    with open('wardriving_summary.txt', 'w') as text_file:
        text_file.write(formatted_content)

    print("Summary text file created successfully.")