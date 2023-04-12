import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from collections import deque
from cpe import CPE


cpe = CPE()
rssi_data = deque(maxlen=100)
sinr_data = deque(maxlen=100)

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    html.H1('CPE Dashboard', className='text-center my-4'),
    dbc.Card([
        dbc.Checklist(
            id='auto-refresh',
            options=[{'label': 'Auto-refresh', 'value': 'enabled'}],
            value=['enabled'],
            labelStyle={'font-weight': 'bold', 'margin-right': '10px'}
        )
    ], body=True, style={'position': 'fixed', 'top': '10px', 'right': '10px', 'width': '200px'}),
    dbc.Tabs([
        dbc.Tab(label="KPIs", children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='rssi-chart', animate=True, style={'height': '45vh'}),
                    dcc.Graph(id='sinr-chart', animate=True, style={'height': '45vh'})
                ], width=9),
                dbc.Col([
                    dcc.Graph(id='wifi-score-chart', animate=True, style={'height': '45vh'}),
                    dcc.Graph(id='n-clients-chart', animate=False, style={'height': '45vh'})
                ], width=3),
            ], justify='between'),
        ]),
        dbc.Tab(label="Neighbors", children=[
            html.P("TODO: Add Neighbors tab content here...")
        ]),
    ]),
    dcc.Interval(
        id='update-interval',
        interval=5*1000,
        n_intervals=0
    )
], fluid=True)

@app.callback([Output('rssi-chart', 'figure'),
               Output('sinr-chart', 'figure'),
               Output("wifi-score-chart", "figure"),
               Output("n-clients-chart", "figure")
               ],
              [Input('update-interval', 'n_intervals')],
              [State('auto-refresh', 'value')])
def update_charts(n, refresh):
    rssi = cpe.get_rssi()
    sinr = cpe.get_sinr()
    wifi_score = cpe.get_wifi_score()
    n_clients = cpe.get_n_clients()

    rssi_data.append(rssi)
    sinr_data.append(sinr)

    if not refresh:
        return dash.no_update

    rssi_fig = go.Figure(
        data=[go.Scatter(x=list(range(len(rssi_data))), y=list(rssi_data), mode='lines+markers', hovertemplate='RSSI: %{y} dBm')],
        layout=go.Layout(title='RSSI Chart (dBm)', yaxis=dict(title='dBm', range=[-90, -30]))
    )
    rssi_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=-65, y1=-20, fillcolor='green', opacity=0.2)
    rssi_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=-75, y1=-65, fillcolor='yellow', opacity=0.2)
    rssi_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=-100, y1=-75, fillcolor='red', opacity=0.2)

    sinr_fig = go.Figure(
        data=[go.Scatter(x=list(range(len(sinr_data))), y=list(sinr_data), mode='lines+markers', hovertemplate='SINR: %{y} dB')],
        layout=go.Layout(title='SINR Chart (dB)', yaxis=dict(title='dB', range=[-10, 35]))
    )
    sinr_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=15, y1=50, fillcolor='green', opacity=0.2)
    sinr_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=5, y1=15, fillcolor='yellow', opacity=0.2)
    sinr_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y', y0=-50, y1=5, fillcolor='red', opacity=0.2)

    rssi_fig.update_layout(xaxis_range=[0, len(rssi_data)-1])
    sinr_fig.update_layout(xaxis_range=[0, len(sinr_data)-1])

    wifi_score_fig = go.Figure(
            data=[go.Indicator(
                    mode="gauge+number",
                    value = wifi_score,
                    title = {'text': "WiFi score (%)"},
                    gauge = {'axis': {'range': [0, 100]}},
                    )]
            )

    n_clients_fig = go.Figure(
            data=[go.Indicator(
                    mode="number",
                    value = n_clients,
                    title = {'text': "Connected clients"},
                    )]
            )

    return rssi_fig, sinr_fig, wifi_score_fig, n_clients_fig



if __name__ == '__main__':
    app.run_server(debug=True)
