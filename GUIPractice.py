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
            vars_combobox  = ttk.Combobox(self.window, textvariable = keep_value, width = 12)

            vars_combobox["values"] = ["-"]
            vars_combobox["state"]  = "readonly"
            vars_combobox.current(0)
            vars_combobox.place(relx = relative_x, rely = relative_y)
            vars_combobox.bind("<<ComboboxSelected>>", combobox_trigger)

            return vars_combobox

        def create_button(button_text: str, button_function, relative_x: float, relative_y: float, button_number: int = None, button_width: int = None, button_height: int = None):
            def button_click():
                button_function(button_number)
            
            open_file_button = ttk.Button(self.window, text = button_text, command = button_click, width = button_width, height = button_height)
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

            # if (hasattr(self, "loaded_data")):
            #     del self.data_dictionary
            #     self.data_dictionary = {}

            #     for drop_box in [self.data_preview_box, self.variable_chart_box, self.descriptive_stats_box]:
            #         drop_box["values"] = ["-"]
            #         drop_box.current(0)

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

                descriptive_stats_list = ["-"]

                self.loaded_data = load_dict[self.filename.lower().split(".")[-1]](self.filename)
                self.data_dictionary[f"Data_{str(file_number).zfill(2)}"] = self.loaded_data
                self.status_label.config(text = f"File {file_number} Loaded", fg = "blue")
                
                if (("Data_01" in self.data_dictionary) and ("Data_02" in self.data_dictionary)):
                    self.join_type_box["values"]   = ["Select a join type"] + ["left", "right", "inner", "outer"]
                    self.join_column_box["values"] = ["Select primary key"] + [i for i in self.data_dictionary["Data_01"].columns if i in self.data_dictionary["Data_02"].columns]
                    self.join_type_box.current(0)
                    self.join_column_box.current(0)

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

        def merge_data(event):
            try:
                self.merged_data = pd.merge(
                    self.data_dictionary["Data_01"], 
                    self.data_dictionary["Data_02"], 
                    on  = self.combobox_dict["join_variable"], 
                    how = self.combobox_dict["join_type"]
                )

                self.status_label.config(text = "Datasets merged", fg = "blue")
                self.select_filter_variable["values"]  = ["Select a variable", "All"] + list(self.merged_data.columns)
                self.select_filter_operation["values"] = ["Select an operation"] + ["Greater than or equal", "Greater than", "Lesser than", "Lesser than or equal", "Equals", "Does not equal"]
                self.filter_value_text_box.insert("1.0", "Input filter values")
                self.select_filter_variable.current(0)
                self.select_filter_operation.current(0)
                                
            except AttributeError:
                self.status_label.config(text = "Inputs required for merge operation are missing, please ensure that datasets are loaded and the options for the merge operation are specified correctly", fg = "red")

        def apply_transformation(event):
            filter_value = float(self.filter_value_text_box.get()) if (self.combobox_dict["filter_variable"] in self.merged_data.select_dtypes(include = "object").columns) else self.filter_value_text_box.get()

            temporary_data = {
                "Greater than or equal" : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] >= filter_value],
                "Greater than"          : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] >  filter_value],
                "Lesser than or equal"  : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] <= filter_value],
                "Lesser than"           : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] <  filter_value],
                "Equals"                : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] == filter_value],
                "Does not equal"        : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] != filter_value]
            }

            self.merged_data = temporary_data[self.combobox_dict["filter_operation"]]
            self.status_label.config(text = "Filters applied")                
                                       
        self.window = tk.Tk()
        self.window.title(self.window_message)
        self.window.geometry(self.window_geometry)
        self.window.resizable(0, 0)

        self.filename_bar    = create_text_bar(1, 0, 0, 0.05, 0.0970, state = "normal")
        self.mean_text_bar   = create_text_bar(1, 0, 0, 0.05, 0.7, 408)
        self.median_text_bar = create_text_bar(1, 0, 0, 0.05, 0.8, 408)
        self.mode_bar        = create_text_bar(1, 0, 0, 0.05, 0.9, 408)
        self.chart_window    = create_text_bar(40, 6, 6, 0.35, 0.25, 400)
        self.data_window     = create_text_bar(40, 6, 6, 0.65, 0.25, 400)

        self.status_label = create_label(" ", 0.15, 0.05)
        create_label("1. Load CSV file", 0.05, 0.05)
        create_button("Load File 1", load_file, 0.46, 0.09, 1)
        create_button("Load File 2", load_file, 0.54, 0.09, 2)
        create_button("Reset", reset_function, 0.62, 0.09)
        
        create_label("2. Merge Datasets", 0.05, 0.15)
        create_button("Merge Datasets", merge_data, 0.05, 0.25, button_width = 57)
        self.join_type_box         = create_combobox(0.05, 0.2, "join_type")
        self.join_column_box       = create_combobox(0.15, 0.2, "join_variable")
        
        create_label("3. Data Transformation", 0.05, 0.30)    
        create_button("Apply Transformation", apply_transformation, 0.05, 0.4, button_width = 57)
        self.select_filter_variable  = create_combobox(0.05, 0.35, "filter_variable")
        self.select_filter_operation = create_combobox(0.15, 0.35, "filter_operation")
        self.filter_value_text_box   = create_text_bar(1, 0, 0, 0.25, 0.35, 106, state = "normal")
        
        # create_label("4. Save Data", 0.05, 0.45)
        # self.final_variable_selection = create_text_bar(1, 0, 0, 0.05, 0.5, 408, state = "normal")
        # create_button("Save Dataset", save_file, 0.05, 0.55, button_width = 57)
        
        # create_label("5. Descriptive Statistics (for numeric columns)", 0.05, 0.6)
        # create_label("Mean", 0.05, 0.65)
        # create_label("Median", 0.05, 0.75)
        # create_label("Mode", 0.05, 0.85)

        # create_label("6. Data Preview", 0.35, 0.15)
        # create_label("7. Variable Chart", 0.65, 0.15)
        
        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:/Users/User/Desktop/GUIPractice/config/GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    gp = GUIPractice(**config_dict["GUIPractice"]["constructor"])
    gp.settings_method(**config_dict["GUIPractice"]["settings_method"])
    gp.create_initial_state()
