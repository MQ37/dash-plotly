import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from collections import deque
from cpe import CPE

from config import RSSI_BANDS, SINR_BANDS


# Inicializace CPE
cpe = CPE()
# Vytvoření front pro ukládání realtime dat
rssi_data = deque(maxlen=100)
sinr_data = deque(maxlen=100)

# Vytvoření aplikace
app = dash.Dash(__name__,
                # Bootstrap stylovaní
                external_stylesheets=[dbc.themes.BOOTSTRAP])


# Vytvoření layoutu s využitím Bootstrap komponent
app.layout = dbc.Container([
    # Nadpis
    html.H1('CPE Dashboard', className='text-center my-4'),
    # Tlačítko pro automatické obnovení dat
    dbc.Card([
        dbc.Checklist(
            id='auto-refresh',
            options=[{'label': 'Auto-refresh', 'value': 'enabled'}],
            value=['enabled'],
            labelStyle={'font-weight': 'bold', 'margin-right': '10px'}
        )
    ], body=True, style={'position': 'fixed', 'top': '10px', 'right': '10px', 'width': '200px'}),
    # Taby
    dbc.Tabs([
        # Tab pro KPIs
        dbc.Tab(label="KPIs", children=[
            dbc.Row([
                # RSSI a SINR grafy
                dbc.Col([
                    dcc.Graph(id='rssi-chart', animate=True, style={'height': '45vh'}),
                    dcc.Graph(id='sinr-chart', animate=True, style={'height': '45vh'})
                ], width=9),
                # Wifi score a počet klientů
                dbc.Col([
                    dcc.Graph(id='wifi-score-chart', animate=True, style={'height': '45vh'}),
                    dcc.Graph(id='n-clients-chart', animate=False, style={'height': '45vh'})
                ], width=3),
            ], justify='between'),
        ]),
        # Tab pro sousedy
        dbc.Tab(label="Neighbors", children=[
            # Graf sousedů podle kanálu
            dcc.Graph(id='channels-chart', animate=True, style={'height': '80vh'}),
        ]),
    ]),
    # Interval pro automatické obnovení dat
    dcc.Interval(
        id='update-interval',
        interval=5*1000,
        n_intervals=0
    )
], fluid=True)

def create_rssi_fig(rssi_data, rssi_bands):
    # Vytvoření grafu RSSI
    rssi_fig = go.Figure(
        data=[go.Scatter(x=list(range(len(rssi_data))), y=list(rssi_data), mode='lines+markers', hovertemplate='RSSI: %{y} dBm')],
        layout=go.Layout(title='RSSI Chart (dBm)', yaxis={"title": 'dBm', "range": [-90, -40]})
    )
    # Přidání barevných pásem
    for (ymin, ymax, color) in rssi_bands:
        rssi_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y',
                           y0=ymin, y1=ymax, fillcolor=color,
                           opacity=0.2)

    # Zoomnutí na data
    rssi_fig.update_layout(xaxis_range=[0, len(rssi_data)-1])

    return rssi_fig

def create_sinr_fig(sinr_data, sinr_bands):
    # Vytvoření grafu SINR
    sinr_fig = go.Figure(
        data=[go.Scatter(x=list(range(len(sinr_data))), y=list(sinr_data), mode='lines+markers', hovertemplate='SINR: %{y} dB')],
        layout=go.Layout(title='SINR Chart (dB)', yaxis={'title': 'dB', 'range': [-10, 35]})
    )
    # Přidání barevných pásem
    for (ymin, ymax, color) in sinr_bands:
        sinr_fig.add_shape(type='rect', xref='paper', x0=0, x1=1, yref='y',
                           y0=ymin, y1=ymax, fillcolor=color,
                           opacity=0.2)

    # Zoomnutí na data
    sinr_fig.update_layout(xaxis_range=[0, len(sinr_data)-1])

    return sinr_fig

def create_wifi_score_fig(wifi_score):
    # Vytvoření WiFi score indikátoru
    wifi_score_fig = go.Figure(
            data=[go.Indicator(
                    mode="gauge+number",
                    value = wifi_score,
                    title = {'text': "WiFi score (%)"},
                    gauge = {'axis': {'range': [0, 100]}},
                    )]
            )

    return wifi_score_fig


def create_n_clients_fig(n_clients):
    # Vytvoření indikátoru počtu klientů
    n_clients_fig = go.Figure(
            data=[go.Indicator(
                    mode="number",
                    value = n_clients,
                    title = {'text': "Connected clients"},
                    )]
            )

    return n_clients_fig

def create_channels_fig(channels, current_channel):
    # Vytvoření bar plotu s počtem AP na jednotlivých kanálech
    bars = []
    for i, count in enumerate(channels):
        bars.append(go.Bar(
            x=[i+1],
            y=[count],
            name=f'Channel {i+1}',
            marker={"color" : "#33cc33", "opacity": 0.8},
            hovertext=f'{count} APs',
            hoverinfo='text',
            showlegend=False
        ))

    # Zobrazit vlastní kanál AP
    bars.append(go.Bar(
        x=[current_channel],
        y=[1],
        marker={"color": "#0099ff"},
        hovertext=f'Your CPEs AP',
        hoverinfo='text',
        showlegend=False
    ))

    # Upravení layoutu
    layout = go.Layout(
        title={"text" : 'WiFi neighbors 2.4 GHz', "x" : 0.5 },
        xaxis={
            'title': 'Channel',
            'tickvals': list(range(1, len(channels)+1)),
            'ticktext': [f'{i+1}' for i in range(len(channels))]
        },
        yaxis={"title": 'Number of APs'},
        barmode='stack'
    )

    # Aktualizovat y osu podle největšího počtu AP
    channels_fig = go.Figure(data=bars, layout=layout)
    y_max = max(channels) * 1.2
    channels_fig.update_yaxes(range=[0, y_max])

    return channels_fig

@app.callback(Output('rssi-chart', 'figure'),
               Output('sinr-chart', 'figure'),
               Output("wifi-score-chart", "figure"),
               Output("n-clients-chart", "figure"),
               Output("channels-chart", "figure"),
              Input('update-interval', 'n_intervals'),
              State('auto-refresh', 'value'))
def update_charts(n, refresh):
    """
    Funkce pro aktualizaci grafů.
    Reaguje na uplynutí intervalu, nic nedělá pokud není zaškrtnuto auto-refresh.
    Pracuje s hodnotou checkboxu auto-refresh, která je předána jako state, nereaguje na ni.
    Vrací aktualizované grafy.
    """
    if not refresh:
        return dash.no_update

    rssi = cpe.get_rssi()
    sinr = cpe.get_sinr()
    wifi_score = cpe.get_wifi_score()
    n_clients = cpe.get_n_clients()
    channels = cpe.get_channels()
    current_channel = cpe.get_current_channel()

    rssi_data.append(rssi)
    sinr_data.append(sinr)

    rssi_fig = create_rssi_fig(rssi_data, RSSI_BANDS)
    sinr_fig = create_sinr_fig(sinr_data, SINR_BANDS)
    wifi_score_fig = create_wifi_score_fig(wifi_score)
    n_clients_fig = create_n_clients_fig(n_clients)
    channels_fig = create_channels_fig(channels, current_channel)

    return rssi_fig, sinr_fig, wifi_score_fig, n_clients_fig, channels_fig



if __name__ == '__main__':
    app.run_server(debug=True)
