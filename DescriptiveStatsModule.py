from SaveDataModule import SaveDataModule
from tkinter        import filedialog as fd 

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
