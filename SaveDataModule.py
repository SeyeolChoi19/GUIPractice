import json

from VariableRenameModule import VariableRenameModule
from tkinter              import filedialog as fd 

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
