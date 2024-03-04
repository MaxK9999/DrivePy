# GUI helper file for DrivePy to run from desktop
import customtkinter


def create_gui():
    # Set up the customtkinter values
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")


    root = customtkinter.CTk()
    root.geometry("500x500")
    root.title("DrivePy")	


    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)


    label = customtkinter.CTkLabel(master=frame, text="DrivePy", font=("Roboto", 24))
    label.pack(pady=12, padx=10)

    return root