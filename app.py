import pandas as pd
import flask

from dash import Dash, dcc, html, Input, Output, callback, State
#import dash_ag_grid as dag
import feffery_antd_components as fac
# import html components from dash
from dash import html
import support as sp    
import dash_bootstrap_components as dbc

server = flask.Flask(__name__)

tree=fac.AntdTree(id="tree", treeData=sp.treeData, checkable=True, defaultExpandAll=True,
                  persistence_type='local', persistence=True)
graph=dcc.Graph(id="graph", style={'height': '100vh'})
store=dcc.Store(id='store', storage_type='local')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# Build layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([tree], width=3),
        dbc.Col([graph], width=9),
    ]),
    dbc.Row([
        store,
    ]),
],fluid=True)


@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='tree', component_property='checkedKeys')
)
def update_output_div(input_value):
    return sp.get_graph(input_value)

@callback(
    Output(component_id='store', component_property='data'),
    Input(component_id='tree', component_property='checkedKeys'),
)
def update_store(checkedKeys):
    #get the current range in the range slider
    print(f"checkedkeys: {checkedKeys}")
    return {'checkedKeys':checkedKeys}

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
