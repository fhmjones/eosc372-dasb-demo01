# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing 
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.

from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

# gather the list of soundings
# see Python routine "parse-csv.py" for the method of building this list
ocgysites = pd.read_csv("latlong-list-1each.csv")

# read the first data file to make the first station's temperature and salinity plots
def read_onedataset(file):
    df = pd.read_csv(file, skiprows = 39, index_col=False, names=['CTDPRS' , 'CTDPRS_FLAG_W' , 'CTDTMP' , 'CTDTMP_FLAG_W' , 'CTDSAL' , 'CTDSAL_FLAG_W' , 'CTDOXY' , 'CTDOXY_FLAG_W' , 'CTDXMISS' , 'CTDXMISS_FLAG_W' , 'CTDFLUOR' , 'CTDFLUOR_FLAG_W' , 'CTDRINKO' , 'CTDRINKO_FLAG_W'])
    return df.drop([len(df)-1])

app.layout = html.Div([
    dcc.Markdown('''
        ### CTD data from Cruise 33RR20180918

        Data for this demonstration app were obtained from the [GEOTRACES cruise GP15](https://geotraces-gp15.com/about-geotraces-gp15/).

        #### Purpose
        
        1. A preliminary demonstration to learn how to write an app that facilitates efficient exploration of geographically located datasets.
        2. To inspire creative ways of exploring, analyzing or interpreting data for lessons, labs or assignments. 
        
        #### Instructions 
        An interactive map is shown with measurement stations along longitude -152E, from Alaska to the equator. 
        
        - Mouse-over a station (dots) will plot the corresponding temperature, salinity & oxygen profiles.  
        - Mouse wheel zooms within the map.  
        - Map background and station dot color can be adjusted with checkboxes.  
        - The map's slider changes vertical size of the map.  
        - Depth scale can be adjusted for all three plots together using the slider above the three depth profiles.  
        - Each depth profile can be saved as a figure which students could submit with an assignment.  
  
        Other types of interactivity can be easiy included, depending on the needs of the users and learning goals. 

        ----------
        '''),    

# slider or checklist details at https://dash.plotly.com/dash-core-components
# checkboxes can be lumped together but then logic in "update_graph" is messier.
# Content can be delivered using html, but markdown is simpler. 
    html.Div([
        dcc.Markdown('''
        **Select point colour, map type & size**
        '''),
        # switch between plain or satellite view for the map
        dcc.Checklist(
            id='background',
            options=[
                {'label': 'Satellite (from USGS)', 'value': 'satellite'}
            ],
            value=['plain']
        ),
        # change colour to be more visible on satellite.
        dcc.Checklist(
            id='color_checkbox',
            options=[
                {'label': 'change dot color', 'value': 'fuscia'}
            ],
            value=['blue']
        ),
        #this slider is not necessary but demonstrates use of sliders that may be useful in other apps
        html.Label('map vertical size:'),
        dcc.Slider(id='mapheight', min=300, max=500, value=400, step=50,
            marks={300:'300 pixels', 400:'400', 500:'500',}
        )
    ], style={'width': '38%', 'display': 'inline-block'}),

    html.Div([
        dcc.Markdown('''
        **Measured values versus depth.**          
        Click-drag to zoom graphs. Double click to auto-scale. Reset all using axis slider. 
        '''),
        
        #Adjust depth axes
        html.Label('Depth axis, DBars'),
        dcc.Slider(id='depthaxis', min=200, max=3500, value=2500, step=None,
            marks={200:'200', 500:'500', 1000:'1000', 1500:'1500', 2500:'2500', 3500:'3500'}
        )
        
    ], style={'width': '60%', 'display': 'inline-block', 'textAlign': 'center'}),

    # the map with location points
    html.Div([
        dcc.Graph(
            id='map',
            config={
                'staticPlot': False,     # True, False
                'scrollZoom': True,      # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,        # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d','select2d', 'lasso2d'],
            },
            # hoverData={'points:'}
        )
    ], style={'width': '38%', 'display': 'inline-block', 'padding': '0 20'}),

    # two side-by-side data plots
    # these have reduced interactivity to simplify the look and feel
    html.Div([
        dcc.Graph(
            id='temperature',
            config={
                'staticPlot': False,      # True, False
                'scrollZoom': False,      # True, False
                'doubleClick': 'reset',   # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,         # True, False
                'displayModeBar': 'hover',  # True, False, 'hover'
                'watermark': False,
                'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'autoScale2d'],
            }
        ),
    ], style={'display': 'inline-block', 'width': '20%'}),
    html.Div([
        dcc.Graph(
            id='salinity',
            config={
                'staticPlot': False,      # True, False
                'scrollZoom': False,      # True, False
                'doubleClick': 'reset',   # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,         # True, False
                'displayModeBar': 'hover',  # True, False, 'hover'
                'watermark': False,
                'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'autoScale2d'],
            }
        ),        
    ], style={'display': 'inline-block', 'width': '20%'}),
    html.Div([
        dcc.Graph(
            id='oxygen',
            config={
                'staticPlot': False,      # True, False
                'scrollZoom': False,      # True, False
                'doubleClick': 'reset',   # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,         # True, False
                'displayModeBar': 'hover',  # True, False, 'hover'
                'watermark': False,
                'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'autoScale2d'],
            }
        ),        
    ], style={'display': 'inline-block', 'width': '20%'}),

    dcc.Markdown('''
        ----
        
        ### Questions for students

        To be added when an actual oceanography dashboard is created.

        ### Attributions

        - **Data source**: Cutter, G. 2018. _CTD data from Cruise 33RR20180918, exchange version_. Accessed from CCHDO https://cchdo.ucsd.edu/cruise/33RR20180918. Access date 2021-03-09. 
        - **Code:** F. Jones. Based on ideas learned in [Plotly interactive graphing](https://dash.plotly.com/interactive-graphing) documentation and a [great video on interactive plots](https://www.youtube.com/watch?v=G8r2BB3GFVY) using "hover" or "click" events.
  
        ''')
], style={'width': '1000px'})

# The callback function with it's app.callback wrapper.
@app.callback(
    Output('map', 'figure'),
    Input('mapheight', 'value'),
    Input('color_checkbox', 'value'),
    Input('background', 'value')
    )    
def update_map(mapheight, color_checkbox, background):
    # Dot color, map type and map zoom are interactive.
    # code from https://plotly.com/python/mapbox-layers/ without the "fig.show".
    
    if color_checkbox==['blue']: dotcolor = "blue"
    else: dotcolor = 'fuchsia'
    
    fig = px.scatter_mapbox(ocgysites, lat="lat", lon="long", hover_name="locn", hover_data=["drop"],
                            color_discrete_sequence=[dotcolor], zoom=1.2, height=mapheight,
                            custom_data=['filename'])
            
    # use this for a plain, easy-to-read street map
    if background==['plain']:
        fig.update_layout(mapbox_style="open-street-map")

    # or, use this for a USGS colored topography raster instead of "open-street-map"
    # I do not know how that URL actually delivers the images
    # it is interactive but loading tiles upon "zoom in" may be slowish. 
    # Also, at smaller scales, tiles outside of USA may be blank. 
    else: 
        fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {"below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": ["https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"]
            }
        ])
    
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title='GP15 sounding locns') # use "t":30 to put map below controls if they were there.
 
    return fig

# Temperature graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='temperature', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('depthaxis', 'value')
)
def update_tgraph(hov_data, depthaxis):
    if hov_data is None: # necessary for startup before interacting with the map.
        readfile = "data/33RR20180918_00001_00002_ct1.csv"
        latit = 56.05826
        longit = -156.9622
    
    else:
        readfile = hov_data['points'][0]['customdata'][0]
        latit = hov_data['points'][0]['lat']  
        longit = hov_data['points'][0]['lon']
    
    sitedf = read_onedataset(readfile)
    xvals = sitedf["CTDTMP"]
    yvals = sitedf["CTDPRS"].astype('float') # SEEMS NECESSARY OR GRAPHS HAVE "CATEGORIES" FOR Y-AXIS
    annot_lat = f'Lat: {latit:4.4f}N'
    annot_long = f'Lon: {longit:4.4f}E'
        
    figT = px.line(x=xvals, y=yvals, title='Temperature')
    figT.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    figT.update_xaxes(range=[0,30], title="deg. C.")
    # figT.update_xaxes(range=[0,30], title="deg. C.", side="top")
    figT.update_yaxes(range=[depthaxis,0], title="Depth in DBars")
    
    # this puts location information at bottom right of the temperature graph
    # better than making it a title since positioning is more versatile
    # there are no doubt other ways of adding this information
    figT.add_annotation(text=annot_lat,
                  xref="paper", yref="paper", # Google this annotation function for explanation of "paper"
                  x=.14, y=.1, showarrow=False)
    figT.add_annotation(text=annot_long,
                  xref="paper", yref="paper",
                  x=.14, y=.05, showarrow=False)

    return figT

# Salinity graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='salinity', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('depthaxis', 'value')
)
def update_sgraph(hov_data, depthaxis):
    if hov_data is None:
        readfile = "data/33RR20180918_00001_00002_ct1.csv"
        # lat/long not needed since annotation is on the temperature plot. 
    else:
        readfile = hov_data['points'][0]['customdata'][0]
    
    sitedf = read_onedataset(readfile)
    xvals = sitedf["CTDSAL"]
    yvals = sitedf["CTDPRS"].astype('float') # SEEMS NECESSARY OR GRAPHS HAVE "CATEGORIES" FOR Y-AXIS

    figS = px.line(x=xvals, y=yvals, title='Salinity')
    figS.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    figS.update_xaxes(range=[31,37], title="PSS-78")
    figS.update_yaxes(range=[depthaxis,0], title="Depth in DBars")
    
    return figS

# Oxygen graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='oxygen', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('depthaxis', 'value')
)
def update_sgraph(hov_data, depthaxis):
    if hov_data is None:
        readfile = "data/33RR20180918_00001_00002_ct1.csv"
        # lat/long not needed since annotation is on the temperature plot. 
    else:
        readfile = hov_data['points'][0]['customdata'][0]
    
    sitedf = read_onedataset(readfile)
    xvals = sitedf["CTDOXY"]
    yvals = sitedf["CTDPRS"].astype('float') # SEEMS NECESSARY OR GRAPHS HAVE "CATEGORIES" FOR Y-AXIS

    figO = px.line(x=xvals, y=yvals, title='Oxygen')
    figO.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    figO.update_xaxes(range=[0,320], title="UMOL/KG")
    figO.update_yaxes(range=[depthaxis,0], title="Depth in DBars")
    
    return figO

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
