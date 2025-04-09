from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df = base_anual_jovenes

app.layout = html.Div([
    html.H1('Sueldo promedio por profesionista en México', 
            style={'textAlign': 'center', 'color': "blue", 'font-size': 30}),
    
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': c, 'value': c} for c in df['Descripción_Campo_amplio'].unique()],
        value='Artes y humanidades'
    ),

    html.Label("Selecciona estado(s) a resaltar:"),
    dcc.Checklist(
        id='checklist-estados',
        options=[{'label': e, 'value': e} for e in sorted(df['DESCRIP'].unique())],
        value=[],  # por defecto ninguno seleccionado
        inline=True
    ),

    dcc.Graph(id='graph'), 
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'),
    Input('checklist-estados', 'value')
)
def update_graph(selected_campo, estados_resaltados):
    filtered_df = df[df['Descripción_Campo_amplio'] == selected_campo]

    fig = px.scatter(
        filtered_df,
        x="Año",
        y="Sueldo promedio por profesionista",
        color="DESCRIP",
        size="fac_tri",
        size_max=25,
        height=500,
        width=900,
        template="simple_white",
        labels={
            "DESCRIP": "Estado",
            "fac_tri": "Profesionistas"
        }
    )
    fig.update_xaxes(type="category")

    # Baja opacidad general y resalta los estados seleccionados
    fig.for_each_trace(
        lambda trace: trace.update(marker=dict(opacity=1)) 
        if trace.name in estados_resaltados 
        else trace.update(marker=dict(opacity=0.3))
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
