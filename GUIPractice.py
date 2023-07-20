import json

import tkinter as tk 
import pandas  as pd 

from tkinter import ttk 
from tkinter import filedialog as fd 

class GUIPractice:
    def __init__(self, window_message: str, font_type: str = "Calibri"):
        self.window_message  = window_message 
        self.font_type       = font_type 

    def settings_method(self, file_types: dict, window_width: int = 1200, window_height: int = 800, font_size: int = 12):
        self.file_types_dict   = file_types 
        self.target_file_types = ((key, value) for (key, value) in self.file_types_dict.items())
        self.window_width      = window_width 
        self.window_height     = window_height 
        self.window_geometry   = f"{self.window_width}x{self.window_height}"
        self.font_size         = font_size 
        self.data_dictionary   = {}
        self.combobox_dict     = {}

    def create_initial_state(self):
        def create_combobox(relative_x: float, relative_y: float, combobox_designator: str) -> ttk.Combobox:
            def combobox_trigger(event):
                self.combobox_dict[combobox_designator] = vars_combobox.get()

            selected_value = tk.StringVar()            
            keep_value     = selected_value.get()
            vars_combobox  = ttk.Combobox(self.window, textvariable = keep_value)

            vars_combobox["values"] = ["-"]
            vars_combobox["state"]  = "readonly"
            vars_combobox.current(0)
            vars_combobox.place(relx = relative_x, rely = relative_y)
            vars_combobox.bind("<<ComboboxSelected>>", combobox_trigger)

            return vars_combobox

        def create_button(button_text: str, button_function, relative_x: float, relative_y: float, button_number: int = None):
            def button_click():
                button_function(button_number)
            
            open_file_button = ttk.Button(self.window, text = button_text, command = button_click)
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
        
        def reset_function(filler: None):
            objects_list = [self.filename_bar, self.mean_text_bar, self.chart_window, self.data_window]
            self.status_label.config(text = " ")

            for object in objects_list: 
                object.delete("1.0", "end")

            if (hasattr(self, "loaded_data")):
                del self.data_dictionary
                self.data_dictionary = {}

                for drop_box in [self.data_preview_box, self.variable_chart_box, self.descriptive_stats_box]:
                    drop_box["values"] = ["-"]
                    drop_box.current(0)

        def load_file(file_number):
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

                self.data_dictionary[f"Data_{str(file_number).zfill(2)}"] = self.loaded_data
                self.status_label.config(text = f"File {file_number} Loaded", fg = "blue")
                self.data_preview_box["values"]   = ["Select a variable"] + list(self.loaded_data.columns)
                self.variable_chart_box["values"] = ["Select a variable"] + list(self.loaded_data.columns)
                self.data_preview_box.current(0)
                self.variable_chart_box.current(0)
                
                descriptive_stats_list = ["-"]

                if (self.loaded_data.select_dtypes(include = ["int64", "float64"]).shape[1] != 0):
                    descriptive_stats_list = ["Select a variable"] + [i for i in self.loaded_data.select_dtypes(include = ["float64", "int64"]).columns]

                self.descriptive_stats_box["values"] = descriptive_stats_list
                self.descriptive_stats_box.current(0)
                
            except ImportError:
                self.status_label.config(text = "Dependency error detected, please make sure all dependencies were installed correctly", fg = "red")
            except FileNotFoundError:
                self.status_label.config(text = "File not found, please make sure the correct file was selected", fg = "red")
            except KeyError: 
                if (hasattr(self, "loaded_data")):
                    pass                    
                else:
                    self.status_label.config(text = "Only csv, xlsx and json files allowed", fg = "red")
                    self.filename_bar.delete("1.0", "end")
                
        def save_file(filler_func: None):
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
        self.mean_text_bar   = create_text_bar(1, 0, 0, 0.65, 0.3, 140)
        self.median_text_bar = create_text_bar(1, 0, 0, 0.65, 0.4, 140)
        self.mode_bar        = create_text_bar(1, 0, 0, 0.65, 0.5, 140)
        self.chart_window    = create_text_bar(40, 6, 6, 0.05, 0.25, 400)
        self.data_window     = create_text_bar(40, 6, 6, 0.35, 0.25, 400)

        self.status_label = create_label(" ", 0.15, 0.05)
        create_label("Load CSV file", 0.05, 0.05)
        create_label("Data Preview", 0.05, 0.15)
        create_label("Variable Chart", 0.35, 0.15)
        create_label("Descriptive Statistics (for numeric columns)", 0.65, 0.15)
        create_label("Mean", 0.65, 0.25)
        create_label("Median", 0.65, 0.35)
        create_label("Mode", 0.65, 0.45)
        create_label("Variable Filters", 0.65, 0.6)

        create_button("Load File 1", load_file, 0.46, 0.09, 1)
        create_button("Load File 2", load_file, 0.54, 0.09, 2)
        create_button("Save File", save_file, 0.62, 0.09)
        create_button("Reset", reset_function, 0.70, 0.09)
        
        self.data_preview_box      = create_combobox(0.05, 0.2, "data_preview")
        self.variable_chart_box    = create_combobox(0.35, 0.2, "variable_chart")
        self.descriptive_stats_box = create_combobox(0.65, 0.2, "descriptive_stats")

        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:/Users/User/Desktop/GUIPractice/config/GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    gp = GUIPractice(**config_dict["GUIPractice"]["constructor"])
    gp.settings_method(**config_dict["GUIPractice"]["settings_method"])
    gp.create_initial_state()
