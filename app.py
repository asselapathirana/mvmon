#import dash_ag_grid as dag
import feffery_antd_components as fac
import flask
import pandas as pd
import support as sp
# import html components from dash
from dash import Dash, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import loginornot


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
title = f"3SWater Monitoring Stations ({loginornot.version})"
app = Dash(__name__, title=title, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

auth=loginornot.get_auth(app)
# Build layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Alert(id='banner-title', children=[
            html.H1(title),
            dbc.Button(id='close-button', children='X', className='close-button')
        ], color='primary', className='banner-title'),
    ]),
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
    #print(f"horizontal_zoom={horizontal_zoom}, vertical_zoom={vertical_zoom}, checkedKeys={input_value}")
    print(f"input_value={input_value}")
    # Drop values starting with "_"
    input_value = [x for x in input_value if not x.startswith("_")]
    print(f"input_value={input_value}")	
    return dcc.Graph(figure=sp.get_graph(input_value, auth=auth, clean=True), 
                        style={'height': f'{vertical_zoom}vh', 'width': f'{horizontal_zoom}%'},
                        config={"displaylogo": False,})


@app.callback(
    Output('banner-title', 'is_open'),
    Input('close-button', 'n_clicks')
)
def toggle_banner(n):
    #print("toggle_banner", n)
    if n:
        return False
    return True

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter