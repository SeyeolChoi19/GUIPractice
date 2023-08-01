import json

import tkinter           as tk 
import pandas            as pd 
import seaborn           as sns
import matplotlib.pyplot as plt 

from tkinter                           import ttk 
from tkinter                           import filedialog as fd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BasicMethods:
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
        self.data_dictionary   = {}
        self.combobox_dict     = {}
        self.text_bar_list     = []
        self.combobox_list     = []

        self.window = tk.Tk()
        self.window.title(self.window_message)
        self.window.geometry(self.window_geometry)
        self.window.resizable(0, 0)

    def create_label(self, label_text: str, relative_x: float, relative_y: float) -> tk.Label:
        label_object = tk.Label(text = label_text, font = (self.font_type, self.font_size, "bold"))
        label_object.place(relx = relative_x, rely = relative_y)

        return label_object
    
    def create_button(self, button_text: str, button_function, relative_x: float, relative_y: float, button_number: int = None, button_width: int = None, button_height: int = None):
        def button_click():
            button_function(button_number)

        button_object = ttk.Button(self.window, text = button_text, command = button_click, width = button_width, height = button_height)
        button_object.grid(column = 0, row = 1, sticky = "w", padx = 10, pady = 10)
        button_object.place(relx = relative_x, rely = relative_y)

    def create_text_bar(self, text_bar_height: int, grid_column: int, grid_row: int, relative_x: float, relative_y: float, bar_width: float = None, state: str = "disabled") -> tk.Text:
        text_bar = tk.Text(self.window, height = text_bar_height, state = state)
        text_bar.grid(column = grid_column, row = grid_row, sticky = "nsew")
        text_bar.place(relx = relative_x, rely = relative_y)

        if (bar_width != None):
            text_bar.place(width = bar_width)

        return text_bar    
    
    def create_combobox(self, relative_x: float, relative_y: float, combobox_designator: str) -> ttk.Combobox:
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

class FileLoader(BasicMethods):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def load_file(self, file_number: int):
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
                "json" : json_loader
            }

            self.loaded_data = load_dict[self.filename.lower().split(".")[-1]](self.filename, encoding = "latin-1")
            self.data_dictionary[f"Data_{str(file_number).zfill(2)}"] = self.loaded_data
            self.status_label.config(text = f"File {file_number} Loaded", fg = "blue")

            if (("Data_01" in self.data_dictionary) and ("Data_02" in self.data_dictionary)):
                self.join_type_box["values"]    = ["Select a join"] + ["left", "right", "inner", "outer"]
                self.left_column_box["values"]  = ["Select first key column"] + list(self.data_dictionary["Data_01"].columns)
                self.right_column_box["values"] = ["Select second key column"] + list(self.data_dictionary["Data_02"].columns)
                self.join_type_box.current(0)
                self.left_column_box.current(0)
                self.right_column_box.current(0)

        except ImportError:
            self.status_label.config(text = "Dependency error detected, please make sure all dependencies were installed correctly", fg = 'red')
        except FileNotFoundError:
            self.status_label.config(text = "File not found, please make sure the correct file was selected", fg = "red")
        except KeyError:
            if (hasattr(self, "loaded_data")):
                pass
            else:
                self.status_label.config(text = "Only csv and json files allowed", fg = "red")
                self.filename_bar.delete("1.0", "end")

    def create_loader(self):
        self.status_label = self.create_label(" ", 0.15, 0.05)
        self.filename_bar = self.create_text_bar(1, 0, 0, 0.05, 0.097, state = "normal")
        self.text_bar_list.append(self.filename_bar)
        self.create_label("1. Load csv file", 0.05, 0.05)
        self.create_button("Load File 1", self.load_file, 0.46, 0.09, 1)
        self.create_button("Load File 2", self.load_file, 0.54, 0.09, 2)

        self.join_type_box    = self.create_combobox(0.05, 0.19, "join_type")
        self.left_column_box  = self.create_combobox(0.15, 0.19, "left_join_variable")
        self.right_column_box = self.create_combobox(0.25, 0.19, "right_join_variable")

        for text_box in [self.join_type_box, self.left_column_box, self.right_column_box]:
            self.combobox_list.append(text_box)

class MergeModule(FileLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def basic_methods_main(self, *args, **kwargs):
        self.settings_method(*args, **kwargs)
        self.create_loader()

    def merge_data(self, event):
        def parse_date(date_string: str):
            output_string = ""

            if (date_string != "0"):
                date_array    = str(date_string).split("/")
                output_string = f"{str(date_array[-1]).zfill(2)}"

            return output_string 
        
        try: 
            self.merged_data = pd.merge(self.data_dictionary["Data_01"], self.data_dictionary["Data_02"], how = self.combobox_dict["join_type"], left_on = self.combobox_dict["left_join_variable"], right_on = self.combobox_dict["right_join_variable"])
            
            self.merged_data["Date"]             = self.merged_data["Date"].fillna("0")
            self.merged_data["Date"]             = self.merged_data.apply(lambda x: parse_date(x["Date"]), axis = 1)
            self.merged_data["In-Use ERP Total"] = self.merged_data["In-Use ERP Total"].str.replace(".", "").str.replace(",", "").astype(float) / 1000

            self.select_filter_variable["values"]     = ["Select a variable"] + list(self.merged_data.columns)
            self.select_filter_operation["values"]    = ["Select an operation"] + ["Greater than or equal", "Greater than", "Lesser than or equal", "Lesser than", "Equals", "Does not equal", "Contains", "Does not contain", "Drop null values"]
            self.select_numerical_variables["values"] = ["Select a variable"] + [i for i in self.merged_data.select_dtypes(include = "number").columns]

            for text_box in [self.select_filter_variable, self.select_filter_operation, self.select_numerical_variables]:
                text_box.current(0)

            self.status_label.config(text = "Datasets merged", fg = "blue")
        except AttributeError:
            self.status_label.config(text = "Inputs required for merge operation are missing, please ensure that datasets are loaded and the options for the merge operations are specified correctly", fg = "red")

    def create_merge_module(self):
        self.create_label("2. Merge Datasets", 0.05, 0.15)
        self.create_button("Merge Datasets", self.merge_data, 0.05, 0.23, button_width = 57)

        self.select_filter_variable     = self.create_combobox(0.05, 0.33, "filter_variable")
        self.select_filter_operation    = self.create_combobox(0.15, 0.33, "filter_operation")
        self.select_numerical_variables = self.create_combobox(0.05, 0.83, "descriptive_stats_box")

        for text_box in [self.select_filter_variable, self.select_filter_operation, self.select_numerical_variables]:
            self.combobox_list.append(text_box)

class DataTransformationModule(MergeModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def merge_module_main(self, *args, **kwargs):
        self.basic_methods_main(*args, **kwargs)
        self.create_merge_module()

    def apply_transformation(self, event):
        try:
            filter_value = self.filter_value_text_box.get("1.0", "end") if (self.combobox_dict["filter_variable"] in self.merged_data.select_dtypes(include = "object").columns) else float(self.filter_value_text_box.get("1.0", "end"))

            temporary_data = {
                "Greater than or equal" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] >= filter_value],
                    "message" : f"Rows lesser than {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Greater than" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] > filter_value],
                    "message" : f"Rows lesser than or equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Lesser than or equal" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] <= filter_value],
                    "message" : f"Rows greater than {filter_value} for {self.combobox_dict['filter_variable']} removed",
                },
                "Lesser than" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] < filter_value],
                    "message" : f"Rows greater than or equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Equals" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] == filter_value],
                    "message" : f"Rows not equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Does not equal" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]] != filter_value],
                    "message" : f"Rows equal to {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Contains" : {
                    "data"    : self.merged_data[self.merged_data[self.combobox_dict["filter_variable"]].isin([i.strip() for i in str(filter_value).split(",")])],
                    "message" : f"Rows not in {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Does not contain" : {
                    "data"    : self.merged_data[~self.merged_data[self.combobox_dict["filter_variable"]].isin([i.strip() for i in str(filter_value).split(",")])],
                    "message" : f"Rows in {filter_value} for {self.combobox_dict['filter_variable']} removed"
                },
                "Drop null values" : {
                    "data"    : self.merged_data.dropna(subset = [self.combobox_dict["filter_variable"]]),
                    "message" : f"Rows with null values in {self.combobox_dict['filter_variable']} removed"
                },
            }

            self.merged_data = temporary_data[self.combobox_dict["filter_operation"]]["data"]
            self.status_label.config(text = temporary_data[self.combobox_dict["filter_operation"]]["message"])
            self.filter_value_text_box.delete("1.0", "end")
        except KeyError: 
            self.status_label.config(text = "Please select a variable for data transformation operations", fg = "red")
            self.filter_value_text_box.delete("1.0", "end")

    def create_data_transformation_module(self):
        self.filter_value_text_box = self.create_text_bar(1, 0, 0, 0.25, 0.33, 106, state = "normal")
        self.create_label("3. Data Transformation", 0.05, 0.29)
        self.create_button("Apply Transformation", self.apply_transformation, 0.05, 0.37, button_width = 57)

class VariableRenameModule(DataTransformationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def data_transformation_main(self, *args, **kwargs):
        self.merge_module_main(*args, **kwargs)
        self.create_data_transformation_module()

    def rename_variable(self, event):
        if (self.original_name_text_box.get("1.0", "end").strip() not in self.merged_data.columns):
            self.status_label.config(text = "Variable name error detected", fg = "red")
            raise KeyError
        else:
            self.merged_data = self.merged_data.rename(columns = {self.original_name_text_box.get("1.0", "end").strip() : self.changed_name_text_box.get("1.0", "end").strip()})
            self.select_filter_variable["values"]     = ["Select a variable"] + list(self.merged_data.columns)
            self.select_numerical_variables["values"] = ["Select a variable"] + [i for i in self.merged_data.select_dtypes(include = "number").columns]
            self.status_label.config(text = "Variable renamed", fg = "blue")
    
    def create_data_renaming_module(self):
        self.original_name_text_box = self.create_text_bar(1, 0, 0, 0.15, 0.47, 252, state = "normal")
        self.changed_name_text_box  = self.create_text_bar(1, 0, 0, 0.15, 0.51, 252, state = "normal")
        self.create_label("4. Rename Variables", 0.05, 0.43)
        self.create_label("Variable Name", 0.05, 0.47)
        self.create_label("New Name", 0.05, 0.51)
        self.create_button("Rename Variable", self.rename_variable, 0.05, 0.55, button_width = 57)

        for text_box in [self.original_name_text_box, self.changed_name_text_box]:
            self.text_bar_list.append(text_box)

class SaveDataModule(VariableRenameModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def variable_rename_main(self, *args, **kwargs):
        self.data_transformation_main(*args, **kwargs)
        self.create_data_renaming_module()

    def save_file(self, filler_func = None):
        try:
            output_variables    = [i.strip() for i in self.final_variable_selection.get("1.0", "end").lower().split(",")]
            output_data         = self.merged_data.copy()
            output_data.columns = [col.lower() for col in output_data.columns]
            output_data         = output_data[output_variables].to_json()
            save_data_name      = fd.asksaveasfilename(initialfile = "Untitled.json", defaultextension = ".json", filetypes = [("JSON file", "*.json")])

            with open(save_data_name, "w") as f:
                json.dump(output_data, f, indent = 4)

            self.status_label.config(text = "File saved", fg = "blue")           
        except KeyError: 
            self.status_label.config(text = "Variable name error detected, please make sure variable names were entered correctly", fg = "red")
        except AttributeError:
            self.status_label.config(text = "Data to be saved not found, please make sure data was loaded correctly", fg = "red")
        except FileNotFoundError:
            self.status_label.config(text = "Illegal directory, please check if the destination folder was selected correctly", fg = "red")
            
    def create_save_file_module(self):
        self.final_variable_selection = self.create_text_bar(1, 0, 0, 0.05, 0.65, 408, state = "normal")
        self.text_bar_list.append(self.final_variable_selection)
        self.create_label("5. Enter variables to save (separate with commas)", 0.05, 0.61)
        self.create_button("Save Dataset", self.save_file, 0.05, 0.69, button_width = 57)

class DescriptiveStatsModule(SaveDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_file_module_main(self, *args, **kwargs):
        self.variable_rename_main(*args, **kwargs)
        self.create_save_file_module()

    def generate_stats(self, event):
        mean_value   = round(self.merged_data[self.combobox_dict["descriptive_stats_box"]].mean(), 5)
        median_value = round(self.merged_data[self.combobox_dict["descriptive_stats_box"]].median(), 5)
        mode_value   = round(self.merged_data[self.combobox_dict["descriptive_stats_box"]].mode(), 5)
        output_mode  = mode_value.iloc[0] if (len(mode_value) == 1) else "Not applicable"
        
        for (text_bar, output_value) in zip([self.mean_text_bar, self.median_text_bar, self.mode_text_bar], [mean_value, median_value, output_mode]):
            text_bar.delete("1.0", "end")
            text_bar.insert("1.0", output_value)

        self.status_label.config(text = "Descriptive stats generated", fg = "blue")

    def create_descriptive_stats_module(self):
        self.mean_text_bar   = self.create_text_bar(1, 0, 0, 0.145, 0.83, 80, state = "normal")
        self.median_text_bar = self.create_text_bar(1, 0, 0, 0.205, 0.83, 80, state = "normal")
        self.mode_text_bar   = self.create_text_bar(1, 0, 0, 0.265, 0.83, 80, state = "normal")
        self.create_label("6. Descriptive Statistics (for numeric columns)", 0.05, 0.75)
        self.create_label("Select variables", 0.05, 0.79)
        self.create_label("Mean", 0.145, 0.79)
        self.create_label("Median", 0.205, 0.79)
        self.create_label("Mode", 0.265, 0.79)
        self.create_button("Generate Stats", self.generate_stats, 0.05, 0.87, button_width = 57)

        for text_box in [self.mean_text_bar, self.median_text_bar, self.mode_text_bar]:
            self.text_bar_list.append(text_box)

class DataVisualizationModule(DescriptiveStatsModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def descriptive_stats_main(self, *args, **kwargs):
        self.save_file_module_main(*args, **kwargs)
        self.create_descriptive_stats_module()

    def data_preview(self, event, relative_x: float = 0.001, relative_y: float = 0.001):
        try:
            variables_to_preview      = [i.strip() for i in self.preview_text_box.get("1.0", "end").lower().split(",")]
            preview_dataframe         = self.merged_data.copy()
            preview_dataframe.columns = [i.lower().strip() for i in preview_dataframe.columns]
            preview_dataframe         = preview_dataframe[variables_to_preview]
            
            preview_dataframe["Count"] = 1

            preview_dataframe = preview_dataframe.groupby(variables_to_preview + ["Count"], as_index = False).sum()

            fig, ax = plt.subplots(figsize = (9, 5))
            ax.axis("off")

            plotted_table = pd.plotting.table(ax, preview_dataframe.head(20), loc = ["upper center"], colWidths = [0.1] * (len(variables_to_preview) + 1))
            plotted_table.auto_set_font_size(False)
            plotted_table.set_fontsize(6)

            table_canvas = FigureCanvasTkAgg(fig, master = self.dataframe_viewer)
            table_canvas.draw()
            table_canvas.get_tk_widget().place(relx = relative_x, rely = relative_y, width = 900, height = 500)

            plt.close()
            self.preview_text_box.delete("1.0", "end")
            self.status_label.config(text = "Data preview generated", fg = "blue")
        except ValueError:
            self.status_label.config(text = "Empty dataframe detected, please reload the data or check if variables were entered correctly", fg = "red")
        except KeyError:
            self.status_label.config(text = "Variable not found, please check if variable names were entered correctly", fg = "red")
        except AttributeError:
            self.status_label.config(text = "Data not found, please reload data", fg = "red")

    def correlation_chart(self, event, relative_x: float = 0.001, relative_y: float = 0.001):
        def prepare_data():
            copied_data           = self.merged_data.copy()
            copied_data.columns   = [i.lower().strip() for i in self.merged_data.columns]
            correlation_variables = [i.lower().strip() for i in self.preview_text_box.get("1.0", "end").lower().split(",")]
            string_dataframe      = copied_data[[i for i in correlation_variables if (i in copied_data.select_dtypes(include = "object").columns)]]
            numerical_dataframe   = copied_data[[i for i in correlation_variables if (i in copied_data.select_dtypes(include = "number").columns)]]

            for column in string_dataframe.columns:
                for (number, value) in enumerate(string_dataframe[column].unique()):
                    string_dataframe.loc[string_dataframe[column] == value, column] = str(number)

                string_dataframe[column] = string_dataframe[column].astype(float)
            
            output_dataframe = pd.concat([numerical_dataframe, string_dataframe], axis = 1)

            return output_dataframe
        
        def create_heatmap_chart(input_data: pd.DataFrame):
            correlation_matrix = input_data.corr()
            sns.heatmap(correlation_matrix, annot = True, cmap = "coolwarm")

            figure_canvas = FigureCanvasTkAgg(plt.gcf(), master = self.dataframe_viewer)
            figure_canvas.draw()
            figure_canvas.get_tk_widget().place(relx = relative_x, rely = relative_y, width = 900, height = 500)
            plt.close()
            self.preview_text_box.delete("1.0", "end")

        try:
            input_data = prepare_data()
            create_heatmap_chart(input_data)
            self.status_label.config(text = "Correlation heatmap generated", fg = "blue")
        except ValueError:
            self.status_label.config(text = "Empty dataframe detected, please reload the data or check if variables were entered correctly", fg = "red")
        except KeyError:
            self.status_label.config(text = "Variable not found, please check if variable names were entered correctly", fg = "red")
        except AttributeError:
            self.status_label.config(text = "Data not found, please reload data", fg = "red")

    def create_data_visualization_module(self):
        self.preview_text_box = self.create_text_bar(1, 0, 0, 0.35, 0.194, 600, state = "normal")
        self.chart_window     = self.create_text_bar(39, 6, 6, 0.35, 0.23, 901)
        self.dataframe_viewer = ttk.Frame(self.chart_window)
        self.dataframe_viewer.place(width = 896, height = 505, relx = 0.001, rely = 0.001)
        self.create_label("7. Data Visualizer", 0.35, 0.15)
        self.create_button("Preview Data", self.data_preview, 0.775, 0.19, button_width = 15)
        self.create_button("Correlation Viewer", self.correlation_chart, 0.87, 0.19, button_width = 15)

        for text_box in [self.preview_text_box, self.chart_window]:
            self.text_bar_list.append(text_box)

class DataProcessingGUI(DataVisualizationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def data_visualization_module_main(self, *args, **kwargs):
        self.descriptive_stats_main(*args, **kwargs)
        self.create_data_visualization_module()

    def reset_function(self, event):
        def reset_comboboxes():
            for combobox in self.combobox_list:
                combobox["values"] = ["-"]
                combobox.current(0)

        def reset_text_bars():
            for text_bar in self.text_bar_list:
                text_bar.delete("1.0", "end")

        def reset_other_elements():
            self.data_dictionary  = {}
            self.dataframe_viewer = ttk.Frame(self.chart_window)
            self.dataframe_viewer.place(width = 896, height = 505, relx = 0.001, rely = 0.001)
            self.status_label.config(text = " ")

        reset_comboboxes()
        reset_text_bars()
        reset_other_elements()

    def create_data_processing_gui(self):
        self.create_button("Reset GUI", self.reset_function, 0.62, 0.09)
        self.window.mainloop()

if __name__ == "__main__":
    with open(r"C:\Users\User\Desktop\GUIPractice\config\GUIPractice_config.json", "r") as f:
        config_dict = json.load(f)

    dpg = DataProcessingGUI(**config_dict["GUIPractice"]["constructor"])
    dpg.data_visualization_module_main(**config_dict["GUIPractice"]["settings_method"])
    dpg.create_data_processing_gui()
