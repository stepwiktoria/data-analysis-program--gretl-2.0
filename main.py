import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Tool")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        load_button = tk.Button(self.root, text="Load CSV Data", command=self.load_data)
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
        self.ax.clear()
        if not self.data.empty:
            self.data.hist(ax=self.ax)
            self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
