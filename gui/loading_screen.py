# Loading screen for when .exe file starts up
import customtkinter
import tkinter as tk
from tkinter import ttk

class LoadingScreen:

    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        
        self.label = customtkinter.CTkLabel(master=self.frame, text="Loading...")
        self.label.pack(pady=12, padx=10)
        
        self.progressbar = ttk.Progressbar(master=self.frame, orient="horizontal", length=200, mode="indeterminate")
        self.progressbar.pack(pady=12, padx=10)
        self.progressbar.start()
    
    
    def show(self):
        self.root.update()
        self.root.deiconify()
        
    
    def destroy(self):
        self.progressbar.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    loading_screen = LoadingScreen(root)
    loading_screen.show()
    loading_screen.root.after(3000, loading_screen.destroy)
    loading_screen.root.mainloop()
