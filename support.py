import pandas as pd
import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate



COUNTRY="The Maldives"
PROVINCE="Meemu Atoll"
ISLANDS=["Mulah", "Muli", "Kolhufushi"]
STATIONTYPE=["Rain Gauge", "Groundwater", "Groundwater+"]
DEFAULTGRAPHS=['A07Rr']

GRAPHGROUPS={'P': "Atmospheric pressure (mH20)", 'H': "Water level (m)", 'T': "Temperature (C°)", 'C':'Hydraulic Conductivity (mS/cm)',
             'R':"Rainfall (mm)"}
COL2PARAM={
    'H1': "Groundwater Level (m)",	
    'P0': "Atmospheric Pressure (mH2O)"	,
    'T0': "Atmospheric Temperature (C°)",	
    'T1': "Temperature in ground (C°)",	
    'C1': "Hydraulic Conductivity (mS/cm)",
    'H2': "Infiltration pit water level (m)",
    'T2': "Infiltration pit water temperature (C°)",
    'R'	: "Accumulated rainfall (mm)",
    'Rr': "Rainfall (mm)",
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
}
stationarray=[]
for station in STATIONTYPES.items():
    var=[]
   
    if station[1] == STATIONTYPE[0]: # rainfall
        subst=['R', 'Rr']
    elif (station[1] == STATIONTYPE[1]): # groundwater
        subst=['H1', 'P0', 'T0', 'T1', 'C1']
    else:
        subst=['H1', 'P0', 'T0', 'T1', 'C1', 'H2', 'T2']
    
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
        }
    ]
}]

def get_graph_types(selectedkeys):
    graph_types={x:[] for x in GRAPHGROUPS.keys()}
    for key in selectedkeys:
        graph_types[key[-2]].append(key)
    graph_types={key: value for key, value in graph_types.items() if len(value)}
    return graph_types

def get_graph(selectedkeys):
    if not (selectedkeys and len(selectedkeys)):
        selectedkeys=DEFAULTGRAPHS
    # drop all selectedkeys that are not exactly 5 chars long and not starting with A
    selectedkeys=[x for x in selectedkeys if len(x)==5 and x[0]=='A']
    
    df=pd.read_pickle('./data/all_stations_data.pkl').reset_index()
    #Now rename column H0 to P0
    df.rename(columns={'H0': 'P0'}, inplace=True)
    gt=get_graph_types(selectedkeys)
    print(gt)
    n=len(gt)
    # Create figure
    fig = go.Figure()
    #vertically stack n=len(gt) plots inside fig
    fig = make_subplots(rows=n, cols=1, vertical_spacing=0.065, shared_xaxes=True)
    for i,key in enumerate(gt):
            for item in gt[key]:
                print (f" Adding {item} to subplot {i+1} with item[:-2]]/item[-2:]]")
                df_=df[df['UNIT_ID']==item[:-2]]
                print(item,item[:-2], )
                name=f"{item[:-2]}-{COL2PARAM[item[-2:]]}"
                if item[-2:]=='Rr':
                    # add bar chart
                                      
                    fig.add_trace(
                        go.Scatter(name=name, x=list(df_['REC_TIME']), y=list(df_[item[-2:]])), i+1, 1)
                else:
                    fig.add_trace(
                        go.Scatter(name=name, x=list(df_['REC_TIME']), y=list(df_[item[-2:]])), i+1, 1)
                    #print(f"fig.add_trace(go.Scatter(x=list(df_['REC_TIME']), y=list(df_[item[-2:]])), {i+1}, 1)")

    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )

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
    ytitles={f'yaxis{i+1}_title':GRAPHGROUPS[key] for i,key in enumerate(gt)}
    fig.update_layout(**rangeslidersetter, **ytitles,
                    xaxis_type="date")
    return fig


if __name__ == '__main__':
    print(treeData)
    