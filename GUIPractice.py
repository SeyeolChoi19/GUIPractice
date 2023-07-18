import json

import tkinter as tk 
import pandas  as pd 

from tkinter import ttk 
from tkinter import filedialog as fd 

class GUIPractice:
    def __init__(self, window_message: str, font_type: str = "Calibri"):
        self.window_message = window_message 
        self.font_type      = font_type 

    def settings_method(self, file_types: dict, window_width: int = 1200, window_height: int = 800, font_size: int = 12):
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

        def create_label(label_text: str, relative_x: float, relative_y: float) -> tk.Label:
            label_object = tk.Label(text = label_text, font = (self.font_type, self.font_size, "bold"))
            label_object.place(relx = relative_x, rely = relative_y)

            return label_object
        
        def create_text_bar(text_bar_height: int, grid_column: int, grid_row: int, relative_x: float, relative_y: float, bar_width: float = None, state: str = "disabled") -> tk.Text:
            text_bar = tk.Text(self.window, height = text_bar_height, state = state)
            text_bar.grid(column = grid_column, row = grid_row, sticky = "nsew")
            text_bar.place(relx = relative_x, rely = relative_y)

            if (bar_width != None):
                text_bar.place(width = bar_width)

            return text_bar
        
        def reset_function():
            objects_list = [
                self.filename_bar, self.mean_text_bar, self.min_text_bar, 
                self.percentile_25, self.percentile_50, self.percentile_75, 
                self.max_text_bar, self.stdev_bar, self.count_bar, 
                self.chart_window, self.data_window
            ]

            self.status_label.config(text = " ")

            if (hasattr(self, "loaded_data")):
                del self.loaded_data

            for object in objects_list: 
                object.delete("1.0", "end")

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

        self.filename_bar    = create_text_bar(1, 0, 0, 0.05, 0.0970, state = "normal")
        self.mean_text_bar   = create_text_bar(1, 0, 0, 0.65, 0.25, 140)
        self.median_text_bar = create_text_bar(1, 0, 0, 0.65, 0.35, 140)
        self.mode_bar        = create_text_bar(1, 0, 0, 0.65, 0.45, 140)
        self.chart_window    = create_text_bar(40, 6, 6, 0.05, 0.25, 400)
        self.data_window     = create_text_bar(40, 6, 6, 0.35, 0.25, 400)

        self.status_label = create_label(" ", 0.15, 0.05)
        create_label("Load CSV file", 0.05, 0.05)
        create_label("Data Preview", 0.05, 0.15)
        create_label("Variable Chart", 0.35, 0.15)
        create_label("Descriptive Statistics (for numeric columns)", 0.65, 0.15)
        create_label("Median", 0.65, 0.2)
        create_label("Mode", 0.65, 0.3)
        create_label("Mode", 0.65, 0.4)
        create_button("Load File", load_file, 0.46, 0.09)
        create_button("Save File", save_file, 0.54, 0.09)
        create_button("Reset", reset_function, 0.62, 0.09)

        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:/Users/User/Desktop/GUIPractice/config/GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    gp = GUIPractice(**config_dict["GUIPractice"]["constructor"])
    gp.settings_method(**config_dict["GUIPractice"]["settings_method"])
    gp.create_initial_state()
