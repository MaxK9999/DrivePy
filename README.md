# DrivePy

Simple Python script that parses Wardriving CSV files, and submits parsed data to a map.

## Usage

 -bash:
    simply run `./DrivePy.py <PATH_TO_YOUR_CSV_FILE>`, file will be displayed in HTML format.

 -CMD/Powershell:
    run `python DrivePy.py <PATH_TO_YOUR_CSV_FILE>`.

 -GUI:
    to run via GUI, simply omit any switches or paths.

 -.exe:
    to run as `.exe` file from desktop, follow PyInstaller instructions below.

### Requirements

run `pip install -r requirements.txt`

## Installation and Compilation

1. Clone the Repository:
`git clone https://github.com/maxk9999/DrivePy.git`
`cd DrivePy`

2. Install Dependencies:

`pip install -r requirements.txt`

!!! FOR .exe FILE !!! (skip these steps if you do not wish to make a .exe file)

3. Compile the Executable with PyInstaller:

`pyinstaller --onefile DrivePy.py`

This will create a standalone executable (DrivePy.exe on Windows) in the dist directory.

4. Run the Executable:

The GUI should pop up and guide you through the steps.

### Credits

inspired by CreepDetector.ipynb by "Alex Lynd" and "skickar"
