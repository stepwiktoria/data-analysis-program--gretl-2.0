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
        load_button.grid(row=0, column=0, pady=10, padx=10)

        target_label = ttk.Label(self.root, text="Select Target Variable:")
        target_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.target_combobox = ttk.Combobox(self.root, textvariable=self.target_variable, state="readonly")
        self.target_combobox.grid(row=1, column=1, pady=5, padx=10)

        explanatory_label = ttk.Label(self.root, text="Select Explanatory Variables:")
        explanatory_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.explanatory_combobox = ttk.Combobox(self.root, textvariable=self.explanatory_variables, state="readonly", width=30)
        self.explanatory_combobox.grid(row=2, column=1, pady=5, padx=10)

        analyze_button = ttk.Button(self.root, text="Analyze Data", command=self.analyze_data)
        analyze_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

        correlation_button = ttk.Button(self.root, text="Correlation Analysis", command=self.correlation_analysis)
        correlation_button.grid(row=4, column=0, pady=5, padx=10, columnspan=2)

        variable_stats_button = ttk.Button(self.root, text="Variable Statistics", command=self.variable_statistics)
        variable_stats_button.grid(row=5, column=0, pady=5, padx=10, columnspan=2)

        linear_regression_button = ttk.Button(self.root, text="Linear Regression", command=self.linear_regression)
        linear_regression_button.grid(row=6, column=0, pady=5, padx=10, columnspan=2)

        # Nowe przyciski
        correlation_selection_button = ttk.Button(self.root, text="Correlation Variable Selection", command=self.correlation_variable_selection)
        correlation_selection_button.grid(row=7, column=0, pady=5, padx=10, columnspan=2)

        descriptive_stats_button = ttk.Button(self.root, text="Descriptive Statistics", command=self.descriptive_statistics)
        descriptive_stats_button.grid(row=8, column=0, pady=5, padx=10, columnspan=2)

        linear_regression_selection_button = ttk.Button(self.root, text="Linear Regression Variable Selection", command=self.linear_regression_variable_selection)
        linear_regression_selection_button.grid(row=9, column=0, pady=5, padx=10, columnspan=2)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, pady=10, padx=10, sticky="nsew")

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
            self.explanatory_variables.set(columns[:2])

    def analyze_data(self):
        target_variable = self.target_variable.get()
        explanatory_variables = self.explanatory_variables.get()

        if target_variable and explanatory_variables:
            self.model = LinearRegression()
            X = self.data[list(explanatory_variables)]
            y = self.data[target_variable]
            self.model.fit(X, y)

            self.show_analyze_result(X, y)

    def show_analyze_result(self, X, y):
        result_window = tk.Toplevel(self.root)
        result_window.title("Analysis Result")

        fig, ax = plt.subplots()
        ax.scatter(X.iloc[:, 0], y, color='blue', label='Actual data')

        if self.model:
            ax.plot(X.iloc[:, 0], self.model.predict(X), color='red', linewidth=2, label='Linear regression')

        ax.set_xlabel(self.explanatory_variables.get())
        ax.set_ylabel(self.target_variable.get())
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=result_window)
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def correlation_analysis(self):
        target_variable = self.target_variable.get()
        explanatory_variables = self.explanatory_variables.get()

        if target_variable and explanatory_variables:
            selected_variables = [target_variable] + list(explanatory_variables)
            correlation_matrix = self.data[selected_variables].corr()

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
            X = self.data[list(explanatory_variables)]
            y = self.data[target_variable]
            self.model.fit(X, y)

            r_squared = r2_score(y, self.model.predict(X))

            stats_text = f"R-squared: {r_squared:.4f}"
            self.show_info_window("Linear Regression Stats", stats_text)

    def correlation_variable_selection(self):
        correlation_selection_window = tk.Toplevel(self.root)
        correlation_selection_window.title("Correlation Variable Selection")

        label = ttk.Label(correlation_selection_window, text="Select variables for correlation analysis:")
        label.pack(pady=10)

        variables_listbox = tk.Listbox(correlation_selection_window, selectmode=tk.MULTIPLE)
        variables_listbox.pack(pady=10)

        # Wypełnij listbox dostępnymi zmiennymi
        columns = self.data.columns.tolist()
        for column in columns:
            variables_listbox.insert(tk.END, column)

        analyze_button = ttk.Button(correlation_selection_window, text="Analyze", command=lambda: self.correlation_variable_analysis(variables_listbox.curselection()))
        analyze_button.pack(pady=10)

    def correlation_variable_analysis(self, selected_indices):
        selected_variables = [self.data.columns[i] for i in selected_indices]

        if len(selected_variables) >= 2:
            correlation_matrix = self.data[selected_variables].corr()

            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title("Correlation Matrix")
            plt.show()

    def descriptive_statistics(self):
        variable = self.target_variable.get()

        if variable:
            stats = self.data[variable].describe()

            stats_text = "Variable Statistics:\n\n" + str(stats)
            self.show_info_window("Variable Statistics", stats_text)

    def linear_regression_variable_selection(self):
        linear_regression_selection_window = tk.Toplevel(self.root)
        linear_regression_selection_window.title("Linear Regression Variable Selection")

        label = ttk.Label(linear_regression_selection_window, text="Select variables for linear regression analysis:")
        label.pack(pady=10)

        variables_listbox = tk.Listbox(linear_regression_selection_window, selectmode=tk.MULTIPLE)
        variables_listbox.pack(pady=10)

        # Wypełnij listbox dostępnymi zmiennymi
        columns = self.data.columns.tolist()
        for column in columns:
            variables_listbox.insert(tk.END, column)

        analyze_button = ttk.Button(linear_regression_selection_window, text="Analyze", command=lambda: self.linear_regression_variable_analysis(variables_listbox.curselection()))
        analyze_button.pack(pady=10)

    def linear_regression_variable_analysis(self, selected_indices):
        selected_variables = [self.data.columns[i] for i in selected_indices]

        if len(selected_variables) >= 2:
            self.model = LinearRegression()
            X = self.data[selected_variables]
            y = self.data[self.target_variable.get()]
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
