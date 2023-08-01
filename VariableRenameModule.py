from DataTransformationModule import DataTransformationModule

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
