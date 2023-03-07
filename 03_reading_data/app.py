import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

PATH = os.path.dirname(os.path.realpath(__file__))
COIN_PATH = os.path.join(PATH, "coins")
app = Dash(__name__)

app.layout = html.Div(children=[
    # 5 min interval
    dcc.Interval(id="interval", interval=300_000),
    html.H1(children='Cryptocurrency Prices'),
    dcc.Dropdown(id='crypto-dropdown', placeholder="Select a coin"),
    html.Div([dcc.Graph(id='crypto-graph', figure={})], id="graph-container"),
])


@app.callback(Output("crypto-dropdown", "options"),
              Input("interval", "n_intervals"))
def update_options(_):
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
    if value is None or options is None:
        return {}, True
    df = pd.read_csv(value)

    label = [opt["label"] for opt in options if opt["value"] == value][0]

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
