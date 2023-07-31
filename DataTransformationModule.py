import json

import tkinter           as tk 
import pandas            as pd 
import seaborn           as sns
import matplotlib.pyplot as plt 

from MergeModule                       import MergeModule
from FileLoader                        import FileLoader
from tkinter                           import ttk 
from tkinter                           import filedialog as fd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.create_label("3. Data Transformation", 0.05, 0.29)
        self.create_button("Apply Transformation", self.apply_transformation, 0.05, 0.37, button_width = 57)
