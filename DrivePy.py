#!/usr/bin/env python
import argparse
import sys
from map_utils import parse_csv, create_map
from gui_utils import create_gui
import pyfiglet


def parse_args():
    custom_usage = '''%(prog)s [options] [CSV_FILE]'''
    parser = argparse.ArgumentParser(description=
    '''    
    Create a map from wardriving data in a CSV file.
    The CSV file should contain at least the following columns:
    
    MAC, SSID, Latitude, Longitude, Signal Strength.
    
    Made for Flipper Zero using Marauder.
    '''
    , 
    formatter_class=argparse.RawTextHelpFormatter,
    usage=custom_usage,
    )                
    parser.add_argument('csv_file', nargs='?', default=None, help='Path to the CSV file containing wardriving data')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    return parser.parse_args()


def main_cli():
    args = parse_args()
    csv_file_path = args.csv_file

    # Parse CSV and create map
    access_points_data = parse_csv(csv_file_path)
    create_map(access_points_data)
    
    
def main_gui():
    root = create_gui()
    
    root.mainloop()   


if __name__ == "__main__":
    # Check if script is run as CLI or GUI
    if len(sys.argv) > 1:
        main_cli()
    else: 
        main_gui()