import pandas            as pd 
import seaborn           as sns
import matplotlib.pyplot as plt 

from DescriptiveStatsModule            import DescriptiveStatsModule
from tkinter                           import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
