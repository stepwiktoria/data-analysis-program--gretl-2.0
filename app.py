import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Analysis Tool")
        self.root.geometry("800x600")
        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('TLabel', font=('Arial', 12), padding=6)

        load_button = ttk.Button(self.root, text="Load CSV Data", command=self.load_data)
        load_button.pack(pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.visualize_data()

    def visualize_data(self):
        # Prosta wizualizacja danych
        self.ax.clear()
        if not self.data.empty:
            self.data.hist(ax=self.ax)
            self.canvas.draw()
