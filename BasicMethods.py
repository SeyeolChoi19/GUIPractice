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

        self.window = tk.Tk()
        self.window.title(self.window_message)
        self.window.geometry(self.window_geometry)
        self.window_resizable(0, 0)

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
        vars_combobox.bind("<<ComboboxSelected", combobox_trigger)

        return vars_combobox
