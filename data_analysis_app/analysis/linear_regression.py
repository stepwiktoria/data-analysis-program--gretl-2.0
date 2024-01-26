# data_analysis_app/analysis/linear_regression.py
import pandas as pd
from sklearn.linear_model import LinearRegression

def perform_linear_regression(data, independent_var, dependent_var):
    """
    Funkcja przeprowadzająca regresję liniową na danych.
    """
    model = LinearRegression()
    X = data[[independent_var]]
    y = data[dependent_var]

    model.fit(X, y)
    return model
