# data_analysis_app/analysis/outlier_detection.py
import pandas as pd
from scipy.stats import zscore

def detect_outliers(data, threshold=3):
    """
    Funkcja wykrywająca obserwacje odstające w danych.
    """
    z_scores = zscore(data)
    abs_z_scores = abs(z_scores)
    outliers = (abs_z_scores > threshold).all(axis=1)
    return outliers
