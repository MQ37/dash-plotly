import numpy as np
from dash import Dash, html, dcc, Output, Input, State
import plotly.express as px
from flask_caching import Cache

# Nastavení cache
CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 0,
}

# Vytvoření instance aplikace
app = Dash(__name__)
# Získání flask serveru
server = app.server

# Inicializace cache
cache = Cache()
# Připojení cache k serveru
cache.init_app(app.server, config=CACHE_CONFIG)


# memoize - cache si pamatuje výsledky funkce pro dané vstupy
@cache.memoize()
def compute_mandelbrot_set(x_min, x_max, y_min, y_max, resolution,
                           max_iterations):
    """
    Funkce pro výpočet množiny Mandelbrotových bodů.
    Vrací množinu bodů, které jsou v množině Mandelbrotových bodů pro dané vstupy.
    Vrací také v jaké iteraci se bod dostal mimo množinu.
    """
    x_values = np.linspace(x_min, x_max, resolution)
    y_values = np.linspace(y_min, y_max, resolution)
    points = set()

    for x in x_values:
        for y in y_values:
            c = complex(x, y)
            z = complex(0, 0)
            iterations = 0
            while abs(z) <= 2 and iterations < max_iterations:
                z = z**2 + c
                iterations += 1
            #if iterations == max_iterations:
            #    points.add((x, y))
            points.add((x, y, iterations))
    return points


# Vytvoření layoutu
app.layout = html.Div([
    html.Div([
        "Resolution",
        # Slider pro výběr rozlišení
        dcc.Slider(1,
                   1000,
                   10,
                   value=100,
                   marks={val: str(val)
                          for val in range(0, 1000 + 1, 100)},
                   id="resolution"),
        "Max iterations",
        # Slider pro výběr maximálního počtu iterací
        dcc.Slider(1,
                   1000,
                   10,
                   value=100,
                   marks={val: str(val)
                          for val in range(0, 1000 + 1, 100)},
                   id="max_iterations"),
        # Tlačítko pro spuštění výpočtu
        html.Button("Compute", id="compute_btn")
    ]),
    html.Div([
        # Graf pro zobrazení výsledků
        dcc.Graph(id="graph"),
    ])
])


@app.callback(Output("graph", "figure"), Input("compute_btn", "n_clicks"),
              Input("graph", "relayoutData"), State("resolution", "value"),
              State("max_iterations", "value"))
def update_graph(_, selection, resolution, max_iter):
    """
    Funkce pro aktualizaci grafu.
    Reaguje na zoom a posunutí v grafu a na stisk tlačítka pro výpočet.
    Pracuje s hodnotou rozlišení a maximálního počtu iterací pomocí State, ale nereaguje na jejich změnu.
    Vrací graf.
    """

    # Získání aktuální pozice v grafu
    if selection is None:
        selection = {}
    x_min = selection.get("xaxis.range[0]")
    x_max = selection.get("xaxis.range[1]")
    y_min = selection.get("yaxis.range[0]")
    y_max = selection.get("yaxis.range[1]")

    # Defaultní pozice v grafu
    if not (x_min and x_max and y_min and y_max):
        x_min = -3
        x_max = 3
        y_min = -3
        y_max = 3

    # Výpočet množiny Mandelbrotových bodů
    points = compute_mandelbrot_set(x_min, x_max, y_min, y_max, resolution,
                                    max_iter)

    # Rozbalení bodů do x, y a iterací
    x, y, iterations = zip(*points)
    x = np.array(x)
    y = np.array(y)
    iterations = np.array(iterations)
    color = iterations

    # Vytvoření grafu
    fig = px.scatter(x=x, y=y, color=color, title="Mandelbrot set")
    fig.layout.width = 800
    fig.layout.height = 800
    # Nastavení velikosti bodů podle rozlišení
    fig.update_traces(marker={"size": 3000 * 1 / resolution})

    return fig


if __name__ == "__main__":
    app.run(debug=True)
