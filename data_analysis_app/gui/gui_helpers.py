# data_analysis_app/gui/gui_helpers.py
import tkinter as tk
from tkinter import filedialog
from data.data_loader import load_data
from analysis.descriptive_stats import calculate_descriptive_stats
from analysis.linear_regression import perform_linear_regression
from analysis.outlier_detection import detect_outliers

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Wybierz plik CSV", filetypes=[("Pliki CSV", "*.csv")])
    return file_path

def load_data_and_display_stats(data_app_instance):
    file_path = open_file_dialog()
    if file_path:
        data = load_data(file_path)
        if data is not None:
            stats = calculate_descriptive_stats(data)
            data_app_instance.display_stats(stats)
        else:
            data_app_instance.display_error_message("Błąd podczas wczytywania danych.")
