import pandas as pd
import plotly.graph_objects as go  
import plotly.express as px
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import textwrap



COUNTRY="The Maldives"
STATIONTYPE=["Rain Gauge", "Groundwater", "Groundwater+", "Tide", "GroundwaterWeather"]
DEFAULTGRAPHS=['A07Rr']
PUBLICWINDOW={'from': -8, 'to': -1	}
MAXTIMEGAP=2 # in hours


#Solar Intensity (W/m²)	Wind Speed (km/h)	Wind Direction (°)	Conductivity (mS/cm)	Temperature (°C)	Water Depth (m)	

GRAPHGROUPS={'P': "Atmospheric pressure (mH20)", 'H': "Water level (m)", 'T': "Temperature (C°)", 'C':'Conductivity (mS/cm)', 'V': "Relative Humidity (%)",
             'R':"Rainfall (mm)", "L": "Tide Level (m)", 'Z': "Solar Intensity (W/m²)", 'W': "Wind Speed (m/s)", 'D': "Wind Direction (°)"}
COL2PARAM={
    'H1': "Groundwater Level (m)",	
    'P0': "Atmospheric Pressure (mH2O)"	,
    'T0': "Atmospheric Temperature (C°)",	
    'V0': "Relative Humidity (%)",
    'T1': "Temperature in ground (C°)",	
    'C1': "Electrical Conductivity (mS/cm)",
    'H2': "Infiltration pit water level (m)",
    'T2': "Infiltration pit water temperature (C°)",
    'R'	: "Accumulated rainfall (mm)",
    'Rr': "Rainfall (mm)",
    'L0': "Tide Level-s-1 (m)",
    'L1': "Tide Level-s-2 (m)",
    'W0': "Wind Speed (m/s)",
    'D0': "Wind Direction (°)",
    'Z0': "Solar Intensity (W/m²)",
    
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
    'A09': STATIONTYPE[4],
    
}


def append_to_children(tree, target_keys, new_child):
    for node in tree:
        # Check if the node matches any level in the target_keys
        if node['key'] == target_keys[0]:
            # If only one key is left, append the new child
            if len(target_keys) == 1:
                node['children'].append(new_child)
                return
            else:
                # If there are more keys, continue searching the children
                append_to_children(node['children'], target_keys[1:], new_child)
        
        # If the node does not match, continue searching its children
        if 'children' in node and node['children']:
            append_to_children(node['children'], target_keys, new_child)

# Tree structure
treeData = [
    {
        'title': COUNTRY,
        'key': COUNTRY,
        'children': [
            {
                'title': 'Meemu Atoll',
                'key': '_Meemu Atoll',
                'children': [
                    {'title': 'Mulah', 'key': '_Mulah', 'children': []},
                    {'title': 'Muli', 'key': '_Muli', 'children': []},
                    {'title': 'Kolhufushi', 'key': '_Kolhufushi', 'children': []},
                ],
            },
            {
                'title': 'Kaafu Atoll',
                'key': '_Kaafu Atoll',
                'children': [
                    {'title': 'Thulusdhoo', 'key': '_Thulusdhoo', 'children': []}
                ],
            }
        ]
    }
]

                

COLORS=['blue', 'black', 'brown', 'purple', 'red', 
        'orange', 'green',  'grey', 'cyan', 'maroon', 'magenta', 'lime', 'maroon', 'navy', 
        'olive', 'silver', 'teal',
        'pink', 'magenta', 'lime', 'maroon', 'navy', 
        'olive', 'silver', 'teal']
DASHES=['solid',  'dash', 'dot', 'longdash', 'dashdot', 'longdashdot']
stationarray=[]
for station in STATIONTYPES.items():
    
   
    if station[1] == STATIONTYPE[0]: # rainfall
        subst=['R', 'Rr']
    elif (station[1] == STATIONTYPE[1]): # groundwater
        subst=['H1', 'P0', 'T0', 'T1', 'C1']
    elif (station[1] == STATIONTYPE[2]): # groundwater+
        subst=['H1', 'P0', 'T0', 'T1', 'C1', 'H2', 'T2']
    elif (station[1] == STATIONTYPE[3]): # tide
        subst=['L0', 'L1']
    elif (station[1] == STATIONTYPE[4]): # weather
        subst=['P0', 'W0', 'D0', 'V0', 'T0', 'C1', 'T1', 'H1', 'Z0', 'R', 'Rr']
    
    if station[0]=='A01' or station[0]=='A02' or station[0]=='A07':
        island='_Mulah'
        province='_Meemu Atoll'
    elif station[0]=='A03' or station[0]=='A04' or station[0]=='A08':
        island='_Kolhufushi'
        province='_Meemu Atoll'
    elif station[0]=='A05' or station[0]=='A06':
        island='_Muli'
        province='_Meemu Atoll'
    elif station[0]=='A09':
        island='_Thulusdhoo'
        province='_Kaafu Atoll'
          
      
    
    tc2p={key: COL2PARAM[key] for key in subst}

    var=[]
    for col in tc2p.items():
        var.append({
                'title': col[1],
                #create a unique key from station and column
                'key': station[0]+col[0],
            })  

    child={
        'title': station[0],
        'key': station[0],
        'children': var
    }
    append_to_children(treeData, [province, island], child)


    #stationarray.append(tmp)

  

def subsample(df, auth=None):
    # if auth is not None return the whole dataframe
    if auth is not None:
        return df
    else:
        # get the last time in data based on REC_TINM
        lasttime=df['REC_TIME'].max()
        # use time delta to get the window
        frm_=lasttime+pd.Timedelta(days=PUBLICWINDOW['from'])
        to__=lasttime+pd.Timedelta(days=PUBLICWINDOW['to'])
        return df[(df['REC_TIME']>=frm_) & (df['REC_TIME']<=to__)]

def get_graph_types(selectedkeys):
    graph_types={x:[] for x in GRAPHGROUPS.keys()}
    for key in selectedkeys:
        graph_types[key[-2]].append(key)
    graph_types={key: value for key, value in graph_types.items() if len(value)}
    return graph_types


def clean_data(df):
    # replace all H0 < 100 with NaN
    df.loc[df['H0']<1, 'H0']=None # less than 1 mH20 is not possible for atmospheric pressure
    return df


def find_timestep(df):
   
    # Calculate time differences
    time_diffs = df['REC_TIME'].diff().dropna()
    
    # Convert to hours
    time_diffs_hours = time_diffs.dt.total_seconds() / 3600
    
    # Find the most common time interval
    most_common_timestep = time_diffs_hours.mode()[0]  # Get the most frequent timestep
    
    return most_common_timestep


def resample(df, dt):
    """
    Fill gaps in the DataFrame based on a given time step.
    
    Parameters:
    df (pd.DataFrame): Original DataFrame with a 'REC_TIME' column.
    dt (float): Detected time step in hours.

    Returns:
    pd.DataFrame: DataFrame with missing timestamps filled and NaNs for missing data.
    """
    # Ensure REC_TIME is in datetime format
    df = df.copy()  # Avoid modifying the original DataFrame
    df.loc[:, 'REC_TIME'] = pd.to_datetime(df['REC_TIME'])
    
    # Generate a full time range from min to max REC_TIME with the given step
    full_time_range = pd.date_range(start=df['REC_TIME'].min(), 
                                    end=df['REC_TIME'].max(), 
                                    freq=f'{int(dt)}H')

    # Create a DataFrame with the full time range
    df_full = pd.DataFrame({'REC_TIME': full_time_range})

    # Merge with the original DataFrame to align timestamps and insert missing values
    df_filled = df_full.merge(df, on='REC_TIME', how='left')

    return df_filled

    

def get_graph(selectedkeys, auth=None, clean=False):
    if not (selectedkeys and len(selectedkeys)):
        selectedkeys=DEFAULTGRAPHS
    #(f"selectedkeys={selectedkeys}")
    # drop all selectedkeys that are not exactly 5 chars long 
    selectedkeys=[x for x in selectedkeys if len(x)==5 ]
    
    df=pd.read_pickle('./data/all_stations_data.pkl').reset_index()

    
    if clean:
        df = clean_data(df)
    #print(df.columns)
    #Now rename column H0 to P0
    df.rename(columns={'H0': 'P0'}, inplace=True)
    gt=get_graph_types(selectedkeys)
    #print("types: ", gt)
    n=len(gt)
    # Create figure
    fig = go.Figure()
    #vertically stack n=len(gt) plots inside fig
    fig = make_subplots(rows=n, cols=1, vertical_spacing=0.01, shared_xaxes=True)
    for i,key in enumerate(gt):
            for item in gt[key]:
                #print (f" Adding {item} to subplot {i+1} with {item[:-2]}")
                df_=df[df['UNIT_ID']==item[:-2]]
                df_=subsample(df_, auth=auth)
                DT=find_timestep(df_)
                #print(f"DT={DT}")
                df_=resample(df_, DT)
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
                elif item[-2:]=='L0' or item[-2:]=='L1':
                    # tide. Need some hacking to 

                    dftmp=df[df['UNIT_ID']==item[:-2]][['REC_TIME',item[-2:]]]
                    
                    dftmp=subsample(dftmp, auth=auth)
                    # sort by REC_TIME
                    # select rows with LO is not null
                    dftmp=dftmp[dftmp[item[-2:]].notnull()]
                    dftmp=dftmp.sort_values(by='REC_TIME')
                    fig.add_trace(
                        go.Scatter(name=name, x=list(dftmp['REC_TIME']), y=list(dftmp[item[-2:]]), line={'color':color, 'dash':dash}), i+1, 1)
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
    