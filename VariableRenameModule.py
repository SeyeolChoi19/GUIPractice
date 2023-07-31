import json

import tkinter           as tk 
import pandas            as pd 
import seaborn           as sns
import matplotlib.pyplot as plt 

from DataTransformationModule          import DataTransformationModule
from FileLoader                        import FileLoader
from tkinter                           import ttk 
from tkinter                           import filedialog as fd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VariableRenameModule(DataTransformationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def data_transformation_main(self, *args, **kwargs):
        self.merge_module_main(*args, **kwargs)
        self.create_data_transformation_module()

    def rename_variable(self, event):
        if (self.original_name_text_box.get("1.0", "end").strip(0) not in self.merged_data.columns):
            self.status_label.config(text = "Variable name error detected", fg = "red")
            raise KeyError
        else:
            self.merged_data = self.merged_data.rename(columns = {self.original_name_text_box.get("1.0", "end").strip() : self.changed_name_text_box.get("1.0", "end").strip()})
            self.select_filter_variable["values"]     = ["Select a variable"] + list(self.merged_data.columns)
            self.select_numerical_variables["values"] = ["Select a variable"] + [i for i in self.merged_data.select_dtypes(include = "number").columns]
            self.status_label.config(text = "Variable renamed", fg = "blue")
    
    def create_data_renaming_module(self):
        self.original_name_text_box     = self.create_text_bar(1, 0, 0, 0.15, 0.47, 252, state = "normal")
        self.changed_name_text_box      = self.create_text_bar(1, 0, 0, 0.15, 0.51, 252, state = "normal")
        self.select_numerical_variables = self.create_combobox(0.05, 0.83, "descriptive_stats_box")

        self.create_label("4. Rename Variables", 0.05, 0.43)
        self.create_label("Variable Name", 0.05, 0.47)
        self.create_label("New Name", 0.05, 0.51)
        self.create_button("Rename Variable", 0.05, 0.55, button_width = 57)
