#!/usr/bin/env python
import argparse
import sys
from app_utils import parse_csv, create_map, create_summary_csv, check_vendors
from gui.gui_utils import create_gui
import pyfiglet
import random
import pandas as pd


def print_banner():
    banner_text = "DrivePy"

    # List of preferred fonts
    preferred_fonts = ['cricket', 'isometric2', 'banner3-D', 'larry3d', 'smslant', 'letters', 'poison', 'univers']

    # Choose a random font from the preferred list
    selected_font = random.choice(preferred_fonts)

    # Create Figlet instance with the selected font
    fig = pyfiglet.Figlet(font=selected_font)

    # Define ANSI escape codes for color (e.g., red text)
    color_start = '\033[94m'  # 91 corresponds to red
    color_end = '\033[0m'  # Reset color

    # Render and print the ASCII art with color
    ascii_banner = fig.renderText(banner_text)
    for line in ascii_banner.split('\n'):
        colored_line = f"{color_start}{line.center(10)}{color_end}"
        print(colored_line)
        

def parse_args():
    custom_usage = '''%(prog)s [options] [CSV_FILE]'''
    
    # Display the banner with a randomly selected font
    print_banner()

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
    parser.add_argument('-s', '--ssid', help='Filter by SSID, add double quotes to SSID if it contains spaces to prevent bugs.\nPut commas in between multiple SSIDs')
    parser.add_argument('-m', '--mac', help='Filter by MAC address, put commas in between multiple MAC addresses')
    parser.add_argument('-c', '--csv', help='Creates summary CSV file instead of creating map', action='store_true')
    parser.add_argument('-mV', '--vendors', help='Check access points by vendor')
    
    return parser.parse_args()


def main_cli():
    args = parse_args()
    csv_file_path = args.csv_file

    # Parse CSV and create map
    access_points_data = parse_csv(csv_file_path)
    
    # Add filters if provided
    if args.ssid:
        ssids = args.ssid.split(',')
        access_points_data = [ap for ap in access_points_data if any(ssid in ap[1] for ssid in ssids)]

    if args.mac:
        macs = args.mac.split(',')
        access_points_data = [ap for ap in access_points_data if any(mac in ap[0] for mac in macs)]
    
    if args.vendors:
        specified_vendor = args.vendors
        vendors_file_path = "mac-vendors.txt"
        matched_vendors = check_vendors(access_points_data, vendors_file_path, specified_vendor)
        if matched_vendors:
            for ap, vendor in matched_vendors:
                print(f"MAC: {ap}, SSID: {ap[1]}, Vendor: {vendor}")
        else:
            print(f"No matching vendors found for specified vendor: {specified_vendor}")
            sys.exit(1)
    
    if args.csv:
        create_summary_csv(access_points_data)    
    else:
        # Create map unless -c switch is provided (ommit else statement if you want to create a map regardless)
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