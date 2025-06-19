# app_utils.py
import folium
from folium.plugins import MarkerCluster
import csv
import webbrowser
import pandas as pd


def parse_csv(file_path, skip_duplicates=False):
    access_points = []
    encountered_macs = set()  # Set to store encountered MAC addresses

    # Fetches Marauder Wardriving data from CSV file
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                mac_address = str(row[0]).split('|')[1].split(',')[0].strip() if len(str(row[0]).split('|')) > 1 else str(row[0]).strip()

                if skip_duplicates and mac_address in encountered_macs:
                    continue

                ssid = row[1]
                wifi_type = row[2].strip('[]')  # remove brackets like [WPA2_PSK]
                signal_strength = int(row[5])
                lat = float(row[6])
                lon = float(row[7])

                access_points.append((mac_address, ssid, lat, lon, signal_strength, wifi_type))
                encountered_macs.add(mac_address)

            except (ValueError, IndexError):
                pass

    return access_points


def create_map(access_points):
    access_points.sort(key=lambda x: x[4])  # sort by signal strength

    map_center = [access_points[0][2], access_points[0][3]]
    mymap = folium.Map(location=map_center, zoom_start=15)
    marker_cluster = MarkerCluster().add_to(mymap)

    for ap in access_points:
        popup_text = (
            f"MAC: {ap[0]}<br>"
            f"SSID: {ap[1]}<br>"
            f"Signal Strength: {ap[4]}<br>"
            f"Wi-Fi Type: {ap[5]}"
        )
        folium.Marker(location=[ap[2], ap[3]], popup=popup_text).add_to(marker_cluster)

    folium.LayerControl().add_to(mymap)
    mymap.save("wardriving_map.html")
    webbrowser.open("wardriving_map.html")


def create_summary_csv(access_points, sort_by_ssid=False):
    columns = [
        "MAC",
        "SSID",
        "Latitude (Y)",
        "Longitude (X)",
        "Signal Strength",
        "Wi-Fi Type"
    ]

    df = pd.DataFrame(access_points, columns=columns)
    df["Grid Accuracy"] = "Estimated"

    if sort_by_ssid:
        df.sort_values(by="SSID", inplace=True)

    column_width = 25
    formatters = {'SSID': lambda x: f'{x:<{column_width}}'}

    formatted_content = df.to_string(index=False, justify='left', col_space=column_width, formatters=formatters)

    with open('wardriving_summary.txt', 'w') as text_file:
        text_file.write(formatted_content)

    print("Summary text file created successfully.")


def check_vendors(access_points, vendors_file_path, specified_vendor):
    vendors = {}

    with open(vendors_file_path, 'r', encoding='utf-8') as vendors_file:
        for line in vendors_file:
            mac, vendor = line.strip().split('\t', 1)
            vendors[mac] = vendor

    matched_vendors = [(ap[0], vendors.get(ap[0][:8], 'Unknown Vendor')) for ap in access_points if ap[0][:8] in vendors]
    specified_vendor_matches = [(mac, vendor) for mac, vendor in matched_vendors if vendor == specified_vendor]

    return specified_vendor_matches
