from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Vytvoříme instanci Dash aplikace
app = Dash(__name__)

# Definujeme barvy
colors = {
    "background": "black",
    "text": "aqua",
}

# Vytvoříme dummy data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# Vytvoříme bar plot
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout(plot_bgcolor=colors['background'],
                  paper_bgcolor=colors['background'],
                  font_color=colors['text'])

# Definujeme layout/strukturu aplikace
app.layout = html.Div(children=[
    # Nadpis
    html.H1(children='Hello World',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
    # Popisek
    html.Div(children='''
        Dash: A web application framework for your data.
    ''',
             style={
                 'textAlign': 'center',
                 'color': colors['text']
             }),
    # Graf
    dcc.Graph(id='example-graph', figure=fig)
],
                      style={'backgroundColor': colors['background']})

if __name__ == '__main__':
    app.run_server(debug=True)
