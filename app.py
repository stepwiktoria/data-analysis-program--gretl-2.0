from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

app = Flask(__name__)

# Domyślna konfiguracja - zmienne do analizy
selected_dependent_var = None
selected_independent_vars = []

# Ścieżka do przykładowego pliku CSV
example_file_path = 'static/data/example_data.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global selected_dependent_var, selected_independent_vars

    # Wczytaj przykładowe dane
    df = pd.read_csv(example_file_path)

    dependent_var = request.form['dependent']
    independent_vars = request.form.getlist('independent')

    # Zapisz wybrane zmienne
    selected_dependent_var = dependent_var
    selected_independent_vars = independent_vars

    return redirect(url_for('analyze'))

@app.route('/analyze')
def analyze():
    global selected_dependent_var, selected_independent_vars

    # Wczytaj przykładowe dane
    df = pd.read_csv(example_file_path)

    # Wybierz wybrane zmienne
    df_selected = df[[selected_dependent_var] + selected_independent_vars]

    # Podstawowe analizy
    description = df_selected.describe().to_html()

    # Korelacja
    correlation = df_selected.corr().to_html()

    return render_template('analyze.html', description=description, correlation=correlation)


@app.route('/remove_variable/<variable_name>')
def remove_variable(variable_name):
    global selected_dependent_var, selected_independent_vars
    if variable_name == selected_dependent_var:
        selected_dependent_var = None
    elif variable_name in selected_independent_vars:
        selected_independent_vars.remove(variable_name)

    return redirect(url_for('analyze'))

@app.route('/linear_regression')
def linear_regression():
    global selected_dependent_var, selected_independent_vars

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_data.csv')
    df = pd.read_csv(file_path)

    # Wybierz wybrane zmienne
    df_selected = df[[selected_dependent_var] + selected_independent_vars]

    # Usuń wiersze z brakującymi danymi
    df_selected = df_selected.dropna()

    # Przygotuj dane do regresji liniowej
    X = df_selected[selected_independent_vars]
    y = df_selected[selected_dependent_var]

    # Utwórz model regresji liniowej
    model = LinearRegression()
    model.fit(X, y)

    # Dokonaj predykcji
    predictions = model.predict(X)

    # Oblicz R-squared
    r_squared = r2_score(y, predictions)

    return render_template('linear_regression.html', predictions=predictions, r_squared=r_squared)

if __name__ == '__main__':
    app.run(debug=True)
