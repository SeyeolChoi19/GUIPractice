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
            def json_loader(filename: str, encoding: str = "utf-8"):
                with open(filename, "r", encoding = encoding) as f:
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

                self.loaded_data = load_dict[self.filename.lower().split(".")[-1]](self.filename, encoding = "latin-1")
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
                
        def save_file(filler_func = None):
            try:
                output_variables = [i.strip() for i in self.final_variable_selection.get("1.0", "end").split(",")]
                output_data      = self.merged_data.copy()
                
                output_data.columns = [col.lower() for col in output_data.columns] 
                output_data         = output_data[output_variables]

                save_data_object = output_data if type(output_data) == dict else json.loads(output_data.to_json())
                save_data_name   = fd.asksaveasfilename(initialfile = "Untitled.json", defaultextension = ".json", filetypes = [("JSON file", "*.json")])

                with open(save_data_name, "w") as f:
                    json.dump(save_data_object, f, indent = 4)

                self.status_label.config(text = "File Saved", fg = "blue")

            except KeyError:
                self.status_label.config(text = "Variable name error detected, please make sure variable names were entered correctly", fg = "red")

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
                self.select_filter_variable["values"]     = ["Select a variable", "All"] + list(self.merged_data.columns)
                self.select_filter_operation["values"]    = ["Select an operation"] + ["Greater than or equal", "Greater than", "Lesser than", "Lesser than or equal", "Equals", "Does not equal", "Drop null values"]
                self.select_numerical_variables["values"] = ["Select a variable"] + [i for i in self.merged_data.select_dtypes(include = ["int64", "float64"]).columns]
                self.filter_value_text_box.insert("1.0", 0)
                self.select_filter_variable.current(0)
                self.select_filter_operation.current(0)
                self.select_numerical_variables.current(0)
                                
            except AttributeError:
                self.status_label.config(text = "Inputs required for merge operation are missing, please ensure that datasets are loaded and the options for the merge operation are specified correctly", fg = "red")

        def apply_transformation(event):
            try:
                filter_value = self.filter_value_text_box.get("1.0", "end") if (self.combobox_dict["filter_variable"] in self.merged_data.select_dtypes(include = "object").columns) else float(self.filter_value_text_box.get("1.0", "end"))

                temporary_data = {
                    "Greater than or equal" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] >= filter_value],
                        "message" : f"Values lesser than {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Greater than" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] >  filter_value],
                        "message" : f"Values lesser than or equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Lesser than or equal" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] <= filter_value],
                        "message" : f"Values greater than {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Lesser than" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] <  filter_value],
                        "message" : f"Values greater than or equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Equals" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] == filter_value],
                        "message" : f"Values not equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Does not equal" : {
                        "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] != filter_value],
                        "message" : f"Values equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                    },
                    "Drop null values" : {
                        "data"    : self.merged_data.dropna(subset = [self.combobox_dict["filter_variable"]]),
                        "message" : f"Rows with null values in {self.combobox_dict['filter_variable']} removed"
                    }
                }

                self.merged_data = temporary_data[self.combobox_dict["filter_operation"]]["data"]
                self.status_label.config(text = temporary_data[self.combobox_dict["filter_operation"]]["message"])                
            except KeyError:
                self.status_label.config(text = "Please select a variable for data transformation operations")

        def generate_stats():
            mode_value  = self.merged_data[self.combobox_dict["descriptive_stats_box"]].mode()
            output_mode = mode_value[0] if (len(mode_value) == 1) else f"{self.combobox_dict['descriptive_stats_box']} does not have a mode"

            self.mean_text_bar.insert("1.0", self.merged_data[self.combobox_dict["descriptive_stats_box"]].mean())
            self.median_text_bar.insert("1.0", self.merged_data[self.combobox_dict["descriptive_stats_box"]].median())
            self.mode_text_bar.insert("1.0", output_mode)
                                       
        self.window = tk.Tk()
        self.window.title(self.window_message)
        self.window.geometry(self.window_geometry)
        self.window.resizable(0, 0)

        self.filename_bar    = create_text_bar(1, 0, 0, 0.05, 0.0970, state = "normal")
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
        
        create_label("4. Enter variables to save, separate variables with commas", 0.05, 0.45)
        self.final_variable_selection = create_text_bar(1, 0, 0, 0.05, 0.5, 408, state = "normal")
        create_button("Save Dataset", save_file, 0.05, 0.55, button_width = 57)
        
        create_label("5. Descriptive Statistics (for numeric columns)", 0.05, 0.6)
        create_label("Select variables", 0.05, 0.65)
        create_label("Mean", 0.155, 0.65)
        create_label("Median", 0.155, 0.75)
        create_label("Mode", 0.155, 0.85)
        create_button("Generate stats", generate_stats, 0.05, 0.75, button_width = 14)
        self.select_numerical_variables = create_combobox(0.05, 0.7, "descriptive_stats_box")
        self.mean_text_bar              = create_text_bar(1, 0, 0, 0.155, 0.7, 243)
        self.median_text_bar            = create_text_bar(1, 0, 0, 0.155, 0.8, 243)
        self.mode_text_bar              = create_text_bar(1, 0, 0, 0.155, 0.9, 243)

        create_label("6. Data Preview", 0.35, 0.15)
        create_label("7. Variable Chart", 0.65, 0.15)
        
        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:\Users\82102\Python_Projects\GUIPractice\config\GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    gp = GUIPractice(**config_dict["GUIPractice"]["constructor"])
    gp.settings_method(**config_dict["GUIPractice"]["settings_method"])
    gp.create_initial_state()
