import pandas as pd


from dash import Dash, dcc, html, Input, Output, callback, State
#import dash_ag_grid as dag
import feffery_antd_components as fac
# import html components from dash
from dash import html
import support as sp    
import dash_bootstrap_components as dbc


tree=fac.AntdTree(id="tree", treeData=sp.treeData, checkable=True, defaultExpandAll=True)
graph=dcc.Graph(id="graph", style={'height': '100vh'})


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Build layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([tree], width=3),
        dbc.Col([graph], width=9)
    ]),
    dbc.Row([html.Div(id='my-output')])
])

@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='tree', component_property='checkedKeys')
)
def update_output_div(input_value):
    app.logger.info(input_value)
    return f'Output: {input_value}'


@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='tree', component_property='checkedKeys')
)
def update_output_div(input_value):
    return sp.get_graph(input_value)

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
