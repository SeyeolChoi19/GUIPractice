import json

import tkinter as tk 
import pandas  as pd 

from tkinter import ttk 
from tkinter import filedialog as fd 

# https://www.geeksforgeeks.org/how-to-change-the-tkinter-label-font-size/
# https://www.geeksforgeeks.org/resizable-method-in-tkinter-python/
# https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/

class GUIPractice:
    def __init__(self, window_message: str, font_type: str = "Calibri"):
        self.window_message = window_message 
        self.font_type      = font_type 

    def settings_method(self, file_types: dict, window_width: int, window_height: int, font_size: int = 12):
        self.file_types_dict   = file_types 
        self.target_file_types = ((key, value) for (key, value) in self.file_types_dict.items())
        self.window_width      = window_width 
        self.window_height     = window_height 
        self.window_geometry   = f"{self.window_width}x{self.window_height}"
        self.font_size         = font_size 

    def create_initial_state(self):
        def create_button(button_text: str, button_function, relative_x: float, relative_y: float):
            open_file_button = ttk.Button(self.window, text = button_text, command = button_function)
            open_file_button.grid(column = 0, row = 1, sticky = "w", padx = 10, pady = 10)
            open_file_button.place(relx = relative_x, rely = relative_y)

        def load_file():
            def json_loader(filename: str):
                with open(filename, "r") as f:
                    json_datafile = pd.DataFrame(json.load(f))
                
                return json_datafile
            
            try:
                self.filename = fd.askopenfilename()
                self.filename_bar.delete("1.0", "end")
                self.filename_bar.insert("1.0", self.filename)
            
                load_dict = {
                    "csv"  : pd.read_csv,
                    "xlsx" : pd.read_excel,
                    "json" : json_loader
                }

                self.loaded_data = load_dict[self.filename.lower().split(".")[-1]](self.filename)
                self.status_label.config(text = "File Loaded", fg = "blue")

            except ImportError:
                self.status_label.config(text = "Dependency error detected, please make sure all dependencies were installed correctly", fg = "red")
            except: 
                if (hasattr(self, "loaded_data")):
                    pass                    
                else:
                    self.status_label.config(text = "File not found, please make sure the correct file was selected", fg = "red")
                    self.filename_bar.delete("1.0", "end")
                
        def save_file():
            try:
                save_data_object = self.loaded_data if type(self.loaded_data) == dict else json.loads(self.loaded_data.to_json())
                save_data_name   = fd.asksaveasfilename(initialfile = "Untitled.json", defaultextension = ".json", filetypes = [("JSON file", "*.json")])

                with open(save_data_name, "w") as f:
                    json.dump(save_data_object, f, indent = 4)

                self.status_label.config(text = "File Saved", fg = "blue")

            except AttributeError:
                self.status_label.config(text = "Data to be saved not found, please make sure data was loaded correctly", fg = "red")
            
            except FileNotFoundError:
                self.status_label.config(text = "Illegal directory, please check if the destination folder was selected correctly", fg = "red")
            
        self.window = tk.Tk()
        self.window.title(self.window_message)
        self.window.geometry(self.window_geometry)
        self.window.resizable(0, 0)

        self.label_object = tk.Label(text = "Load CSV file", font = (self.font_type, self.font_size, "bold"))
        self.status_label = tk.Label(text = " ", font = (self.font_type, self.font_size, "bold"))
        self.filename_bar = tk.Text(self.window, height = 1)
        
        self.label_object.place(relx = 0.05, rely = 0.05)
        self.status_label.place(relx = 0.15, rely = 0.05)
        self.filename_bar.grid(column = 0, row = 0, sticky = "nsew")
        self.filename_bar.place(relx = 0.05, rely = 0.0970)
        
        create_button("Load File", load_file, 0.63, 0.09)
        create_button("Save File", save_file, 0.73, 0.09)

        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:\Users\USER\Desktop\Python_Projects\Projects\TkinterGUIs\config\GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    gp = GUIPractice(**config_dict["GUIPractice"]["constructor"])
    gp.settings_method(**config_dict["GUIPractice"]["settings_method"])
    gp.create_initial_state()
