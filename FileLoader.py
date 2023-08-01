import json

import pandas as pd 

from BasicMethods import BasicMethods
from tkinter      import filedialog as fd 

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
