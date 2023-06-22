from dash import Dash, dcc, html, Input, Output

# Vytvoříme instanci Dash aplikace
app = Dash(__name__)

# Definujeme data - místa na světě
places = {
    "Europe": ["Prague", "Berlin", "Paris"],
    "America": ["New York", "Washington DC", "San Francisco"],
}

# Definujeme layout/strukturu aplikace
app.layout = html.Div([
    # Nadpis
    html.Div("Interactive dashboard",
             style={
                 "textAlign": "center",
                 "fontSize": 33
             }),
    # Horizontální čára
    html.Hr(),
    html.Div([
        "Name:",
        html.Br(),
        # Vstupní pole pro jméno
        dcc.Input(id="input-name", type="text", value=""),
        # Výstupní pole pro jméno
        html.Div(id="output-name"),
    ],
             style={"textAlign": "center"}),
    html.Div([
        "Value:",
        html.Br(),
        # Slider
        dcc.Slider(0, 100, step=5, value=50, id="input-slider"),
        # Výstupní pole pro slider
        html.Div(id="output-slider"),
    ],
             style={
                 "width": "50%",
                 "marginLeft": "auto",
                 "marginRight": "auto"
             }),
    html.Div([
        "X: ",
        # Vstupní pole pro x
        dcc.Input(id="input-x", type="number", value=1),
        # Výstupní tabulka pro x
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th(["x", html.Sup(2)]),
                    html.Th(["x", html.Sup(3)]),
                    html.Th(["x", html.Sup("x")]),
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(id="output-x-2"),
                    html.Td(id="output-x-3"),
                    html.Td(id="output-x-x"),
                ])
            ])
        ])
    ],
             style={
                 "width": "50%",
                 "marginLeft": "auto",
                 "marginRight": "auto"
             }),
    html.Div([
        "Select continent:",
        html.Br(),
        # Radio buttony pro kontinenty
        dcc.RadioItems(list(places.keys()), value="Europe", id="continent"),
        # Dropdown pro města
        dcc.Dropdown(id="city"),
        # Výstupní pole pro města
        html.Div(id="output-places"),
    ],
             style={
                 "width": "50%",
                 "marginLeft": "auto",
                 "marginRight": "auto"
             }),
])


@app.callback(Output(component_id="output-name",
                     component_property="children"),
              Input(component_id="input-name", component_property="value"))
def update_name(val):
    """
    Funkce, která se spustí při změně vstupního pole pro jméno.
    Výstup z této funkce se zobrazí v komponentě s id="output-name".
    """
    if val:
        return "Entered: %s" % val


@app.callback(
    Output(component_id="output-slider", component_property="children"),
    Input(component_id="input-slider", component_property="value"))
def update_slider(val):
    """
    Funkce, která se spustí při změně slideru a získá hodnotu slideru.
    Výstup z této funkce se zobrazí v komponentě s id="output-slider".
    """
    return "Slider value: %s" % val


@app.callback(Output(component_id="output-x-2", component_property="children"),
              Output(component_id="output-x-3", component_property="children"),
              Output(component_id="output-x-x", component_property="children"),
              Input(component_id="input-x", component_property="value"))
def update_x(x):
    """
    Funkce, která se spustí při změně vstupního pole pro x.
    Výstup z této funkce se zobrazí v komponentách s id="output-x-2", id="output-x-3" a id="output-x-x"
    v tabulce.
    """
    if x is not None:
        return x**2, x**3, x**x
    return None, None, None


@app.callback(
    Output(component_id="city", component_property="options"),
    Input(component_id="continent", component_property="value"),
)
def update_city(val):
    """
    Funkce, která se spustí při změně radio buttonů pro kontinenty.
    Výstup této funkce se zobrazí jako možnosti v dropdownu pro města.
    """
    return places[val]


@app.callback(
    Output(component_id="output-places", component_property="children"),
    Input(component_id="city", component_property="value"),
    Input(component_id="city", component_property="options"),
)
def update_place(val, options):
    """
    Funkce, která se spustí při změně dropdownu pro města.
    Výstup této funkce se zobrazí v komponentě s id="output-places".
    """
    if val not in options:
        return None
    return "Selected: %s" % val


if __name__ == "__main__":
    app.run_server(debug=True)
