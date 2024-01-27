import tkinter as tk
from tkinter import filedialog
from data.data_loader import load_data
from analysis.descriptive_stats import calculate_descriptive_stats
from analysis.linear_regression import perform_linear_regression
from analysis.outlier_detection import detect_outliers

class DataAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Analysis App")
        self.geometry("500x300")

        self.create_widgets()

    def create_widgets(self):
        # TODO: Dodaj kod do tworzenia interfejsu graficznego
        pass

if __name__ == "__main__":
    app = DataAnalysisApp()
    app.mainloop()
