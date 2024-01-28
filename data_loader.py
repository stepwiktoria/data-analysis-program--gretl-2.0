import pandas as pd

def load_csv(file_path):
    data = pd.read_csv(file_path)
    # Tutaj możesz dodać więcej logiki, np. wyświetlanie danych w GUI
    return data
