import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Tool")
        self.root.geometry("800x600")

        self.data = pd.DataFrame()
        self.target_variable = tk.StringVar()
        self.explanatory_variables = tk.StringVar()
        self.model = None

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")  # Set ttk theme to "clam" (ttkthemes)

        load_button = ttk.Button(self.root, text="Load CSV Data", command=self.load_data)
        load_button.pack(pady=10)

        target_label = ttk.Label(self.root, text="Select Target Variable:")
        target_label.pack(pady=5)

        self.target_combobox = ttk.Combobox(self.root, textvariable=self.target_variable, state="readonly")
        self.target_combobox.pack(pady=5)

        explanatory_label = ttk.Label(self.root, text="Select Explanatory Variables:")
        explanatory_label.pack(pady=5)

        self.explanatory_combobox = ttk.Combobox(self.root, textvariable=self.explanatory_variables, state="readonly")
        self.explanatory_combobox.pack(pady=5)

        analyze_button = ttk.Button(self.root, text="Analyze Data", command=self.analyze_data)
        analyze_button.pack(pady=10)

        correlation_button = ttk.Button(self.root, text="Correlation Analysis", command=self.correlation_analysis)
        correlation_button.pack(pady=5)

        variable_stats_button = ttk.Button(self.root, text="Variable Statistics", command=self.variable_statistics)
        variable_stats_button.pack(pady=5)

        linear_regression_button = ttk.Button(self.root, text="Linear Regression", command=self.linear_regression)
        linear_regression_button.pack(pady=5)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.populate_comboboxes()

    def populate_comboboxes(self):
        columns = self.data.columns.tolist()

        self.target_combobox["values"] = columns
        self.explanatory_combobox["values"] = columns

        if columns:
            self.target_variable.set(columns[0])
            self.explanatory_variables.set(columns[0])

    def analyze_data(self):
        target_variable = self.target_variable.get()
        explanatory_variables = self.explanatory_variables.get()

        if target_variable and explanatory_variables:
            self.model = LinearRegression()
            X = self.data[[explanatory_variables]]
            y = self.data[target_variable]
            self.model.fit(X, y)

            self.visualize_data(X, y)

    def visualize_data(self, X, y):
        self.ax.clear()
        self.ax.scatter(X, y, color='blue', label='Actual data')
        
        if self.model:
            self.ax.plot(X, self.model.predict(X), color='red', linewidth=2, label='Linear regression')

        self.ax.set_xlabel(self.explanatory_variables.get())
        self.ax.set_ylabel(self.target_variable.get())
        self.ax.legend()

        self.canvas.draw()

    def correlation_analysis(self):
        target_variable = self.target_variable.get()
        explanatory_variables = self.explanatory_variables.get()

        if target_variable and explanatory_variables:
            correlation_matrix = self.data[[target_variable, explanatory_variables]].corr()

            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title("Correlation Matrix")
            plt.show()

    def variable_statistics(self):
        variable = self.target_variable.get()

        if variable:
            stats = self.data[variable].describe()

            stats_text = "Variable Statistics:\n\n" + str(stats)
            self.show_info_window("Variable Statistics", stats_text)

    def linear_regression(self):
        target_variable = self.target_variable.get()
        explanatory_variables = self.explanatory_variables.get()

        if target_variable and explanatory_variables:
            self.model = LinearRegression()
            X = self.data[[explanatory_variables]]
            y = self.data[target_variable]
            self.model.fit(X, y)

            r_squared = r2_score(y, self.model.predict(X))

            stats_text = f"R-squared: {r_squared:.4f}"
            self.show_info_window("Linear Regression Stats", stats_text)

    def show_info_window(self, title, text):
        info_window = tk.Toplevel(self.root)
        info_window.title(title)

        text_widget = tk.Text(info_window, wrap="word", height=10, width=50)
        text_widget.insert("1.0", text)
        text_widget.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
