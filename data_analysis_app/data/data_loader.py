import pandas as pd

def load_data(file_path):
    """
    Funkcja wczytująca dane z pliku CSV.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Błąd podczas wczytywania danych: {e}")
        return None
