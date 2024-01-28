from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.filechooser import FileChooserListView

class DataAnalysisApp(BoxLayout):
    def load_data(self, path, filename):
        if filename:
            self.data = pd.read_csv(filename[0])
            self.visualize_data()

    def visualize_data(self):
        self.fig, self.ax = plt.subplots()
        if not self.data.empty:
            self.data.hist(ax=self.ax)
            self.ids.graph_container.clear_widgets()
            self.ids.graph_container.add_widget(FigureCanvasKivyAgg(self.fig))

class DataAnalysisAppRoot(App):
    def build(self):
        return DataAnalysisApp()

if __name__ == '__main__':
    DataAnalysisAppRoot().run()
