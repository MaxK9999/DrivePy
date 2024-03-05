# GUI helper file for DrivePy to run from desktop
import customtkinter
from tkinter import filedialog, StringVar
from map_utils import parse_csv, create_map


def choose_file(entry_var):
    file_path = filedialog.askopenfilename(title="Select CSV File")
    entry_var.set(file_path)


def load_and_create_map(entry_var):
    csv_file_path = entry_var.get()
    try:
        access_points_data = parse_csv(csv_file_path)
        create_map(access_points_data)
    except Exception as e:
        print(f"Error: {e}")
        

def create_gui():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.geometry("500x500")
    root.title("DrivePy")	

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="DrivePy", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    entry_var = StringVar()
    entry = customtkinter.CTkEntry(master=frame, textvariable=entry_var, placeholder_text="Enter CSV file")
    entry.pack(pady=12, padx=10)

    choose_button = customtkinter.CTkButton(master=frame, text="Choose File", command=lambda: choose_file(entry_var))
    choose_button.pack(pady=12, padx=10)

    create_button = customtkinter.CTkButton(master=frame, text="Create Map", command=lambda: load_and_create_map(entry_var))
    create_button.pack(pady=12, padx=10)

    return root