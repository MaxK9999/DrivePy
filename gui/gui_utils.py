# GUI helper file for DrivePy to run from desktop
import customtkinter
from tkinter import filedialog, StringVar, ttk
from map_utils import parse_csv, create_map


def choose_file(entry_var):
    file_path = filedialog.askopenfilename(title="Select CSV File")
    entry_var.set(file_path)


def load_and_create_map(entry_var, filter_var, filter_entry):
    csv_file_path = entry_var.get()
    try:
        access_points_data = parse_csv(csv_file_path)

        # Apply filters if provided
        filter_type = filter_var.get()
        filter_value = filter_entry.get()

        if filter_type and filter_value:
            if filter_type == "SSID":
                access_points_data = [ap for ap in access_points_data if get_ssid(ap) == filter_value]
            elif filter_type == "MAC":
                access_points_data = [ap for ap in access_points_data if filter_value.lower() in ap[0].lower()]

        create_map(access_points_data)
    except Exception as e:
        print(f"Error: {e}")

def get_ssid(ap):
    try:
        return ap[1]
    except IndexError:
        return None


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

    filter_frame = customtkinter.CTkFrame(master=frame)
    filter_frame.pack(pady=12, padx=10)

    filter_var = StringVar()
    
    # Set default filter
    filter_var.set("SSID")

    filter_label = customtkinter.CTkLabel(master=filter_frame, text="Filter by:")
    filter_label.grid(row=0, column=0, padx=5)

    filter_dropdown = ttk.Combobox(master=filter_frame, textvariable=filter_var, values=["SSID", "MAC"])
    filter_dropdown.grid(row=0, column=1, padx=5)

    filter_entry = customtkinter.CTkEntry(master=filter_frame, placeholder_text="Enter SSID or MAC")
    filter_entry.grid(row=0, column=2, padx=5)

    create_button = customtkinter.CTkButton(
        master=frame,
        text="Create Map",
        command=lambda: load_and_create_map(entry_var, filter_var, filter_entry)
    )
    create_button.pack(pady=12, padx=10)

    return root
