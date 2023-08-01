import json

from DataVisualizationModule import DataVisualizationModule
from tkinter                 import ttk  

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
