# app_utils.py
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
                mac_address = str(row[0]).split('|')[1].split(',')[0].strip() if len(str(row[0]).split('|')) > 1 else str(row[0]).strip()
                signal_strength = int(row[5])
                ssid = row[1]
                lat = float(row[6])
                lon = float(row[7])
                date_time = row[3].strip()
                access_points.append((mac_address, ssid, lat, lon, signal_strength, date_time))
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


def create_summary_csv(access_points, sort_by_ssid=False):
    # Sort DataFrame by the "MAC" column
    columns = [
        "Name",
        "SSID",
        "Latitude (Y)",
        "Longitude (X)",
        "Signal Strength",
        "Date/Time",
        ]
    df = pd.DataFrame(access_points, columns=columns)
    df["Grid Accuracy"] = "Estimated"
    
    # If sort_by_ssid is True, sort the DataFrame by SSID column, else sort by Date/Time column
    if sort_by_ssid:
        df.sort_values(by="SSID", inplace=True)
    else:
        df["Date/Time"] = pd.to_datetime(df["Date/Time"])
        df.sort_values(by="Date/Time", inplace=True)
    
    # Define formatting for SSID column to left-align
    column_width = 25
    formatters = {'SSID': lambda x: f'{x:<{column_width}}'}

    # Save DataFrame to a new formatted text file with fixed width
    formatted_content = df.to_string(index=False, justify='left', col_space=column_width, formatters=formatters)

    with open('wardriving_summary.txt', 'w') as text_file:
        text_file.write(formatted_content)

    print("Summary text file created successfully.")


def check_vendors(access_points, vendors_file_path, specified_vendor):
    vendors = {}

    # Read MAC vendors file and create a dictionary
    with open(vendors_file_path, 'r', encoding='utf-8') as vendors_file:
        for line in vendors_file:
            mac, vendor = line.strip().split('\t', 1)
            vendors[mac] = vendor

    matched_vendors = [(ap[0], vendors.get(ap[0][:8], 'Unknown Vendor')) for ap in access_points if ap[0][:8] in vendors]
    
    # Filter the matched vendors for the specified vendor
    specified_vendor_matches = [(mac, vendor) for mac, vendor in matched_vendors if vendor == specified_vendor]
    
    return specified_vendor_matches