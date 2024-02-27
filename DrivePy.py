import folium
from folium.plugins import Search, MarkerCluster
import csv
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Create a map from wardriving data in a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file containing wardriving data')
    return parser.parse_args()


def parse_csv(file_path):
    access_points = []
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

    # Add a new layer for the search control
    search_layer = folium.FeatureGroup(name='Search').add_to(mymap)

    # Add search control to the new layer
    search_control = Search(layer=search_layer, text='SSID: {name} MAC: {mac}').add_to(mymap)

    # Add LayerControl to switch between layers
    folium.LayerControl().add_to(mymap)

    # Save the map to an HTML file
    mymap.save('wardriving_map.html')


def main():
    args = parse_args()
    csv_file_path = args.csv_file

    # Parse CSV and create map
    access_points_data = parse_csv(csv_file_path)
    create_map(access_points_data)

if __name__ == "__main__":
    main()