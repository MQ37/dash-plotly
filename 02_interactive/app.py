from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

places = {
    "Europe": ["Prague", "Berlin", "Paris"],
    "America": ["New York", "Washington DC", "San Francisco"],
}

app.layout = html.Div([
    html.Div("Interactive dashboard",
             style={
                 "textAlign": "center",
                 "fontSize": 33
             }),
    html.Hr(),
    html.Div([
        "Name:",
        html.Br(),
        dcc.Input(id="input-name", type="text", value=""),
        html.Div(id="output-name"),
    ],
             style={"textAlign": "center"}),
    html.Div([
        "Value:",
        html.Br(),
        dcc.Slider(0, 100, step=5, value=50, id="input-slider"),
        html.Div(id="output-slider"),
    ],
             style={
                 "width": "50%",
                 "marginLeft": "auto",
                 "marginRight": "auto"
             }),
    html.Div([
        "X: ",
        dcc.Input(id="input-x", type="number", value=1),
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
        dcc.RadioItems(list(places.keys()), value="Europe", id="continent"),
        dcc.Dropdown(id="city"),
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
    if val:
        return "Entered: %s" % val


@app.callback(
    Output(component_id="output-slider", component_property="children"),
    Input(component_id="input-slider", component_property="value"))
def update_slider(val):
    return "Slider value: %s" % val


@app.callback(Output(component_id="output-x-2", component_property="children"),
              Output(component_id="output-x-3", component_property="children"),
              Output(component_id="output-x-x", component_property="children"),
              Input(component_id="input-x", component_property="value"))
def update_x(x):
    if x is not None:
        return x**2, x**3, x**x
    return None, None, None


@app.callback(
    Output(component_id="city", component_property="options"),
    Input(component_id="continent", component_property="value"),
)
def update_city(val):
    return places[val]


@app.callback(
    Output(component_id="output-places", component_property="children"),
    Input(component_id="city", component_property="value"),
    Input(component_id="city", component_property="options"),
)
def update_place(val, options):
    if val not in options:
        return None
    return "Selected: %s" % val


if __name__ == "__main__":
    app.run_server(debug=True)
