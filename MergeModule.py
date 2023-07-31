import json

import tkinter           as tk 
import pandas            as pd 
import seaborn           as sns
import matplotlib.pyplot as plt 

from FileLoader                        import FileLoader
from tkinter                           import ttk 
from tkinter                           import filedialog as fd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
            
            self.merged_data["Date"] = self.merged_data["Date"].fillna("0")
            self.merged_data["Date"] = self.merged_data.apply(lambda x: parse_date(x["Date"]), axis = 1)
            self.merged_data["In-Use ERP Total"] = self.merged_data["In-Use ERP Total"].str.replace(".", "").astype(float) / 1000

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
        self.select_numerical_variables = self.create_combobox(0.05, 0.93, "descriptive_stats_box")
