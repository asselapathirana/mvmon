import pandas as pd
import flask

from dash import Dash, dcc, html, Input, Output, callback, State
#import dash_ag_grid as dag
import feffery_antd_components as fac
# import html components from dash
from dash import html
from dash.exceptions import PreventUpdate
import support as sp    
import dash_bootstrap_components as dbc

HFACT=0.99
VFACT=0.99

server = flask.Flask(__name__)

tree=fac.AntdTree(id="tree", treeData=sp.treeData, checkable=True, defaultExpandAll=True,
                  persistence_type='local', persistence=True)
#gr=dcc.Graph( style={'height': '150vh', 'width': '73vw'}, config={"displaylogo": False,})
graph=html.Div(id="graphwindow", children=[])


zoombox=dbc.Container([
    dbc.Row([
        html.Label("Vertical Zoom"),
        dcc.Slider(
            id='vertical-zoom-slider',
            min=50,
            max=200,
            step=10,
            value=100,
            marks={50: '50%', 100: '100%', 200: '200%'},
            
        ),
    ], ),
    dbc.Row([
        html.Label("Horizontal Zoom"),
        dcc.Slider(
            id='horizontal-zoom-slider',
            min=50,
            max=200,
            step=10,
            value=100,
            marks={50: '50%', 100: '100%', 200: '200%'}
        ),
    ], ),

]  
)

app = Dash(__name__, title = "3SWater Monitoring Stations", external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# Build layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dbc.Card(tree), dbc.Card(zoombox)], lg=3),
        dbc.Col([dbc.Card(graph)], lg=9),
    ]),

],fluid=True)

"""
@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='tree', component_property='checkedKeys')
)
def update_output_div(input_value):
    return sp.get_graph(input_value)
"""

@app.callback(
    Output('graphwindow', 'children'),
    [Input('vertical-zoom-slider', 'value'),
    Input('horizontal-zoom-slider', 'value'),
    Input('tree', 'checkedKeys')]
)
def update_graph(vertical_zoom, horizontal_zoom,  input_value):
    horizontal_zoom=HFACT*int(horizontal_zoom)
    vertical_zoom=VFACT*int(vertical_zoom)
    print(f"horizontal_zoom={horizontal_zoom}, vertical_zoom={vertical_zoom}, checkedKeys={input_value}")
    return dcc.Graph(figure=sp.get_graph(input_value), 
                        style={'height': f'{vertical_zoom}vh', 'width': f'{horizontal_zoom}%'},
                        config={"displaylogo": False,})

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
