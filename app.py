import tkinter as tk
from tkinter import filedialog
from data_loader import load_csv
from data_analysis import analyze_data

class DataAnalysisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Analysis Tool")
        self.root.geometry("800x600")
        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):
        load_button = tk.Button(self.root, text="Load CSV Data", command=self.load_data)
        load_button.pack()

        analyze_button = tk.Button(self.root, text="Analyze Data", command=self.analyze_data)
        analyze_button.pack()

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            load_csv(file_path)

    def analyze_data(self):
        analyze_data()
