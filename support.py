import pandas as pd
import plotly.graph_objects as go  
import plotly.express as px
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import textwrap



COUNTRY="The Maldives"
PROVINCE="Meemu Atoll"
ISLANDS=["Mulah", "Muli", "Kolhufushi"]
STATIONTYPE=["Rain Gauge", "Groundwater", "Groundwater+", "Tide"]
DEFAULTGRAPHS=['A07Rr']

GRAPHGROUPS={'P': "Atmospheric pressure (mH20)", 'H': "Water level (m)", 'T': "Temperature (C°)", 'C':'Conductivity (mS/cm)',
             'R':"Rainfall (mm)", "L": "Tide Level (m)"}
COL2PARAM={
    'H1': "Groundwater Level (m)",	
    'P0': "Atmospheric Pressure (mH2O)"	,
    'T0': "Atmospheric Temperature (C°)",	
    'T1': "Temperature in ground (C°)",	
    'C1': "Electrical Conductivity (mS/cm)",
    'H2': "Infiltration pit water level (m)",
    'T2': "Infiltration pit water temperature (C°)",
    'R'	: "Accumulated rainfall (mm)",
    'Rr': "Rainfall (mm)",
    'L0': "Tide Level-s-1 (m)",
    'L1': "Tide Level-s-2 (m)",
}	
STATIONTYPES={
    'A01': STATIONTYPE[2],
    'A02': STATIONTYPE[1],
    'A03': STATIONTYPE[1],
    'A04': STATIONTYPE[1],
    'A05': STATIONTYPE[1],
    'A06': STATIONTYPE[1],
    'A07': STATIONTYPE[0],
    'A08': STATIONTYPE[0],
    'L20': STATIONTYPE[3],
    'L21': STATIONTYPE[3],
}
COLORS=['blue', 'black', 'brown', 'purple', 'red', 
        'orange', 'green',  'grey', 'cyan', 'yellow', 
        'pink', 'magenta', 'lime', 'maroon', 'navy', 
        'olive', 'silver', 'teal',
        'pink', 'magenta', 'lime', 'maroon', 'navy', 
        'olive', 'silver', 'teal']
DASHES=['solid',  'dash', 'dot', 'longdash', 'dashdot', 'longdashdot']
stationarray=[]
for station in STATIONTYPES.items():
    var=[]
   
    if station[1] == STATIONTYPE[0]: # rainfall
        subst=['R', 'Rr']
    elif (station[1] == STATIONTYPE[1]): # groundwater
        subst=['H1', 'P0', 'T0', 'T1', 'C1']
    elif (station[1] == STATIONTYPE[2]): # groundwater+
        subst=['H1', 'P0', 'T0', 'T1', 'C1', 'H2', 'T2']
    elif (station[1] == STATIONTYPE[3]): # tide
        subst=['L0', 'L1']
    
    tc2p={key: COL2PARAM[key] for key in subst}
    for col in tc2p.items():
        var.append({
                'title': col[1],
                #create a unique key from station and column
                'key': station[0]+col[0],
            })  
        
    tmp={    
        'title': f"{station[1]} ({station[0]})",
        'key': station[0],
        'children': var,
    }
    stationarray.append(tmp)

  

treeData =[
    {
    'title': COUNTRY,
    'key': COUNTRY,
    'children': [
        {
            'title': PROVINCE,
            'key': PROVINCE,
            'children': stationarray
        },
    ]
}]

def get_graph_types(selectedkeys):
    print(f"got selecte keys {selectedkeys}")
    graph_types={x:[] for x in GRAPHGROUPS.keys()}
    for key in selectedkeys:
        graph_types[key[-2]].append(key)
    graph_types={key: value for key, value in graph_types.items() if len(value)}
    return graph_types

def get_graph(selectedkeys):
    if not (selectedkeys and len(selectedkeys)):
        selectedkeys=DEFAULTGRAPHS
    print(f"selectedkeys={selectedkeys}")
    # drop all selectedkeys that are not exactly 5 chars long 
    selectedkeys=[x for x in selectedkeys if len(x)==5 ]
    
    df=pd.read_pickle('./data/all_stations_data.pkl').reset_index()
    print(df.columns)
    #Now rename column H0 to P0
    df.rename(columns={'H0': 'P0'}, inplace=True)
    gt=get_graph_types(selectedkeys)
    print("types: ", gt)
    n=len(gt)
    # Create figure
    fig = go.Figure()
    #vertically stack n=len(gt) plots inside fig
    fig = make_subplots(rows=n, cols=1, vertical_spacing=0.01, shared_xaxes=True)
    for i,key in enumerate(gt):
            for item in gt[key]:
                print (f" Adding {item} to subplot {i+1} with {item[:-2]}")
                df_=df[df['UNIT_ID']==item[:-2]]
                #print(df_.tail())
                color=COLORS[int(item[1:-2])]
                
                #print(item,item[:-2], color )
                name=f"{item[:-2]}-{COL2PARAM[item[-2:]]}"
                name='<br>'.join(textwrap.wrap(name, width=20))
                if item[-2:]=='Rr' or item[-1]=='R':
                    dash=DASHES[0]
                else:
                    t=int(item[-1:])
                    t=0 if t==1 else t
                    dash=DASHES[t]
                if item[-2:]=='Rr':
                    # add bar chart                
                    fig.add_trace(
                        go.Scatter(name=name, x=list(df_['REC_TIME']), y=list(df_[item[-2:]]), line={'color':color, 'dash':dash}), i+1, 1)
                else:
                    
                    fig.add_trace(
                        go.Scatter(name=name, x=list(df_['REC_TIME']), y=list(df_[item[-2:]]), line={'color':color, 'dash':dash}), i+1, 1)
                    #print(f"fig.add_trace(go.Scatter(x=list(df_['REC_TIME']), y=list(df_[item[-2:]])), {i+1}, 1)")



    # Add range slider
    fig.update_layout(
        showlegend=True,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
        )
        
        )
    axes=[f"xaxis{i+1}_rangeslider_visible" for i in range(n)]
    #make a dict with all xaxis rangeslider_visible set to False except the last one
    rangeslidersetter={x: False for x in axes} # no rangeslider
    rangeslidersetter[axes[-1]]=True # but only in the last subplot
    #print(rangeslidersetter)
    ytitles={f'yaxis{i+1}_title':'<br>'.join(textwrap.wrap(GRAPHGROUPS[key], width=12)) for i,key in enumerate(gt)}
    fig.update_layout(**rangeslidersetter, **ytitles,
                    xaxis_type="date")
    fig.update_xaxes(rangeslider_thickness = 0.025)
    fig.update_yaxes(automargin=True)
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )
    # this single line is responsible to keep the range slider in place
    fig.update_layout(uirevision='constant')
    return fig


if __name__ == '__main__':
    get_graph(['L20L0', "Rr"])
    