import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

# Aktuální složka
PATH = os.path.dirname(os.path.realpath(__file__))
# Složka s daty
COIN_PATH = os.path.join(PATH, "coins")
# Vytvoření instance aplikace
app = Dash(__name__)

app.layout = html.Div(children=[
    # 5 min interval pro aktualizaci dat
    dcc.Interval(id="interval", interval=300_000),
    # Nadpis
    html.H1(children='Cryptocurrency Prices'),
    # Dropdown pro výběr coinu
    dcc.Dropdown(id='crypto-dropdown', placeholder="Select a coin"),
    # Graf
    html.Div([dcc.Graph(id='crypto-graph', figure={})], id="graph-container"),
])


@app.callback(Output("crypto-dropdown", "options"),
              Input("interval", "n_intervals"))
def update_options(_):
    """
    Funkce pro aktualizaci možností v dropdownu pro výběr coinu.
    Spustí se při každém uplynutí intervalu.
    """
    coin_list = [{
        "label": filename.split(".")[0].capitalize(),
        "value": os.path.join(COIN_PATH, filename)
    } for filename in os.listdir(COIN_PATH)]
    return coin_list


@app.callback(
    Output('crypto-graph', 'figure'),
    Output('graph-container', 'hidden'),
    Input('crypto-dropdown', 'value'),
    State('crypto-dropdown', 'options'),
)
def update_graph(value, options):
    """
    Funkce pro aktualizaci grafu.
    Spustí se při každé změně hodnoty v dropdownu.
    Přistupuje k možnostem v dropdownu pomocí State, ale nereaguje na jejich změnu.
    Výstupem je graf a boolean, který určuje, zda se má graf zobrazit.
    """
    
    # Pokud není vybrán žádný coin, nebo nejsou načteny možnosti, vrátí se prázdný graf
    if value is None or options is None:
        return {}, True
    # Načtení dat
    df = pd.read_csv(value)

    # Získání názvu coinu
    label = [opt["label"] for opt in options if opt["value"] == value][0]

    # Vytvoření grafu
    fig = px.line(df,
                  x='Date',
                  y='Close',
                  title=f"{label} Price",
                  labels={
                      "Close": "Price (USD)",
                  })
    return fig, False


if __name__ == '__main__':
    app.run_server(debug=True)
