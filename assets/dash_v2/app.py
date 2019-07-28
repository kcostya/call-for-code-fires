import dash_table
from flask import Flask
import numpy as np
import urllib
import urllib.parse
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from calendar import monthrange
import datetime
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import pandas as pd
import matplotlib.colors
from utils import * 
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px



app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# Parameters

time_window = 48
time_step = 12


marker_size = 18
marker_symbol = 'circle'#'square'
colorbar_max_val = 8
# weather_opacity = 0.3
fire_opacity = 0.9
max_rows = 10
colorscale = 'solar'#.reversed(name=None)#cmocean_to_plotly(cmocean.cm.solar, colorbar_max_val, reverse=True)


### Initialize data frames
# fire driven forecast
df_fp = pd.read_csv(
    "data/sample_df_start_2017-11-13.csv", 
    dtype=object,
)
# binarize predictions
df_fp['fire count'] = np.where(df_fp['fire count'].astype(np.float) > 0., (1.), 0.)
df_fp.rename(columns={"timestamp": "Timestamp", "timestep":"Timestep","lat": "Lat", "lon": "Lon", "fire count": "Fire Count"}, inplace=True)

# combined weather and fire forecast
df_comb = pd.read_csv(
    "data/sample_start_2017-11-13_12h_step_12h_pred_comb_weather_fire_forecast.csv",
    dtype=object,
)
df_comb.rename(columns={"timestamp": "Timestamp", "timestep":"Timestep","lat": "Lat", "lon": "Lon", "fire count": "Fire Count"}, inplace=True)

# hist data
df_h = pd.read_csv(
    "data/historical_df_start_2017-11-13.csv",
    dtype=object,
)
df_h.rename(columns={"timestamp": "Timestamp", "timestep":"Timestep", "lat": "Lat", "lon": "Lon", "fire count": "Fire Count"}, inplace=True)

## historic and nrt weather
df_w_nrt = pd.read_csv('data/nrt_weather.csv')
df_w_nrt.rename(columns={"timestamp": "Timestamp", "timestep":"Timestep", "lat": "Lat", "lon": "Lon", "fire count": "Fire Count", "T2M":"2m Temperature", "PRECTOT":"Precipitation", "SPEEDMAX":"Max Windspeed",}, inplace=True)

df_w_h = pd.read_csv('data/hist_weather.csv')
df_w_h.rename(columns={"timestamp": "Timestamp", "timestep":"Timestep", "lat": "Lat", "lon": "Lon", "fire count": "Fire Count", "T2M":"2m Temperature", "PRECTOT":"Precipitation", "SPEEDMAX":"Max Windspeed",}, inplace=True)
# units for weather
units = {"2m Temperature": " (K)", "Precipitation": " (kg/m2/s)", "Max Windspeed": " (m/s)", "MIR\N{ASTERISK}":"", "Fires Only":""}


# Layout of Dash App
app.layout = html.Div(
    
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("seer_logo.png"), height=200,
                        ),
                        html.H2("Deep Learning: SEER"),
                        html.P("CA Firecast and Near-real-time Data App"),
                        html.I(
                            """Select the hour and report using the dropdown menu."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                    dcc.Dropdown(
                                            id='timestep--dropdown',
                                            options=[{'label': str(timestep), 'value': str(timestep)}for timestep in df_fp['Timestep'].unique()],
                                           placeholder="Select the hour"
                                            ),
                                    ],

                            ),
                        # Change to side-by-side for mobile layout
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=[
                                            # Dropdown for locations on map
                                            dcc.Dropdown(
                                                id="forecast-type-dropdown",
                                                options=[{'label': i, 'value': i} for i in ['Fire-driven forecast', 'Previous day - actual']],
                                                placeholder="Select a report/forecast",
                                            )
                                        ],
                                    ),
                                 ],
                            ),

                            # Change to side-by-side for mobile layout
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=[
                                            # Dropdown for locations on map
                                            dcc.Dropdown(
                                                id="map-type-dropdown",
                                                options=[{'label': "Map: {}".format(i.capitalize()), 'value': i} for i in [ 'dark', 'outdoors', 'satellite-streets']],
                                                placeholder="Select a map type",
                                                value='dark',
                                            )
                                        ],
                                    ),
                                 ],
                            ),
                            dcc.RadioItems(
                                id="weather-checklist",
                                options=[{'label': i + units[i], 'value': i} for i in ["Fires Only","2m Temperature", "Max Windspeed", "MIR\N{ASTERISK}", "Precipitation"]],
                                labelStyle={'display': 'inline-block'},
                                value='Fires Only',
                                inputStyle= {'margin-right':'8px' ,'margin-top':'10px','margin-left': '18px'},
                            ) ,
                        html.P(id="total-fires", style={'margin-top':'20px'}),
                        html.P(id="forecast-type",),
                        html.P(id="timestep-value"),
                        html.A(
                                'Download Dataframe as CSV',
                                id='download-link',
                                download="rawdata.csv",
                                href="",
                                target="_blank",
                            ),
                        html.Div(
                            className="text-padding",
                            children=[
                                "\N{ASTERISK}MIR, or mid-infrared is considered a good indicator of fuel-moisture content.",
                            ],
                        ),

                    ],
                ),

              
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="firecount-graphic"),
                        dcc.Slider(
                                    id='opacity-slider',
                                    min=0,
                                    max=10,
                                    value=3,
                                    ) ,
                    html.Div( className='table',
                        children=[
                                dash_table.DataTable(
                                            id='table-filtering-be',
                                            columns=[
                                                {"name": i, "id": i} for i in df_fp.columns if i != 'Timestep' 
                                            ],
                                            filter_action='custom',
                                            filter_query='',
                                            style_as_list_view=True,
                                            style_cell={"font-family": "Open Sans",'background':'#AAA89D', 'color':'#2A2A29' ,},
                                            style_data_conditional=[
                                                                    {
                                                                    'if': {'row_index': 'odd'},
                                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                                    }
                                                                    ],
                                            style_header={
                                                        'backgroundColor': 'rgb(230, 230, 230)',
                                                        'fontWeight': 'bold',
                                                            },
                          
                                            style_table={
                                                        # 'height': '500px',
                                                        'overflowY': 'scroll',
                                                        },
                                            fixed_rows={ 'headers': True, 'data': 0 },
                                    ),
                                ],  
                            ),
                    ],  
                ),
            ],
        )
    ]
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3



# Update Map Graph
@app.callback(
        [Output('firecount-graphic', 'figure'),
        dash.dependencies.Output('table-filtering-be', "data"),
        dash.dependencies.Output('download-link', 'href'),
        Output('total-fires', 'children'),
        Output('forecast-type', 'children'),
        Output('timestep-value', 'children')
        ],
    [
        Input("timestep--dropdown", "value"),
        Input("forecast-type-dropdown", "value"),
        dash.dependencies.Input('table-filtering-be', "filter_query"),
        Input("map-type-dropdown", "value"),
        Input("weather-checklist", "value"),
        Input("opacity-slider", "value"),
    ],
)

def update_graph(timestep_value, forecast_type, filter_query, map_type, weather_checklist, weather_opacity):

    

    if forecast_type == 'Weather-driven forecast':
        dff = df_wp
        dff_w = df_w_nrt # nrt weather
    elif forecast_type == 'Previous day - actual':
        dff = df_h
        dff_w = df_w_h # historic weather
    elif forecast_type == 'Combined weather and fire-driven forecast':
        dff = df_comb
        dff_w = df_w_nrt # nrt weather
    else:
        forecast_type = "Fire-driven forecast"
        dff = df_fp
        dff_w = df_w_nrt # nrt weather

    # no timestep chosen so we don't want to display any data
    dff = dff[(dff['Timestep'] == timestep_value)] 
    if timestep_value:
        dff_w = dff_w[dff_w['Timestep'] == int(timestep_value)]
    else:
        dff_w =  []


    def update_table(df, filter):
      filtering_expressions = filter.split(' && ')
      for filter_part in filtering_expressions:
          col_name, operator, filter_value = split_filter_part(filter_part)

          if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
              # these operators match pandas series operator method names
              df = df.loc[getattr(df[col_name].astype(np.float), operator)(filter_value)]
          elif operator == 'contains':
              df = df.loc[dff[col_name].str.contains(filter_value)]
          elif operator == 'datestartswith':
              # this is a simplification of the front-end filtering logic,
              # only works with complete fields in standard format
              df = df.loc[df[col_name].str.startswith(filter_value)]
      return df


    # update datatable
    dff = update_table(dff, filter_query)
    fire_count = dff['Fire Count'].apply(lambda x: np.float(x)).sum()
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)


    zoom = 4.7
    latInitial = 37.44589155769352
    lonInitial = -116.59118404059357
    bearing = 0
     ## Update the data within the figure
    def update_data(dff, dff_w, forecast_type, map_type, selected_weather, weather_opacity):
        # for table
        dff.sort_values(by='Fire Count', inplace=True, ascending=False)
        # access the first (and only trace) of the data, then reassign the properties
        # fig['data'][0]['name'] = timestep_value
        lat  = list(dff['Lat']) if len(dff['Lat']) > 0 else [0]
        lon = list(dff['Lon'])if len(dff['Lon']) > 0 else [0]
        text = list(dff['Fire Count'].astype(str))

        if selected_weather != 'Fires Only' and len(dff_w) > 1:
            # weather plot
            w_lat = list(dff_w['Lat']) 
            w_lon = list(dff_w['Lon'])
            if selected_weather == 'MIR\N{ASTERISK}' :
                    selected_weather = 'MIR'
            weather_text = [selected_weather + ": "] + np.round(dff_w[selected_weather], decimals=3).astype(str)
        else:
            w_lat, w_lon = [0], [0]
            weather_text = [""]

        fig = go.Figure(
                        data=[
                            # Data for fire report / forecast
                            Scattermapbox(
                                lat=lat,
                                lon=lon,
                                mode="markers",
                                hoverinfo="lat+lon+text",
                                text=text,
                                marker=dict(
                                    symbol = marker_symbol,
                                    showscale=True,
                                    color= dff['Fire Count'].astype(np.float) ,
                                    opacity=fire_opacity,
                                    size=marker_size,
                                    colorscale=colorscale,
                                    reversescale=True,
                                    cmin=0.,
                                    cmax=colorbar_max_val,
                                    colorbar=dict(
                                        # title="Fire Count",
                                        x=0.93,
                                        xpad=0,
                                        nticks=colorbar_max_val,
                                        tickvals = [0, 4, 8],
                                        ticktext = ["Low", "Medium", "High"],
                                        tickfont=dict(color="#d8d8d8"),
                                        titlefont=dict(color="#d8d8d8"),
                                        thicknessmode="pixels",
                                    ),
                                ),
                            ),
                      # Data for weather
                            Scattermapbox(
                                lat=w_lat,
                                lon=w_lon,
                                mode="markers",
                                hoverinfo="lat+lon+text",
                                text=weather_text,
                                marker=dict(
                                    symbol = marker_symbol,
                                    color=(dff_w[selected_weather].astype(np.float))  if len(w_lat) > 1 else [0],
                                    opacity=weather_opacity/10,
                                    size=marker_size,
                                    reversescale=True,
                                    colorscale=colorscale,

                                ),
                            ),
                        ],
                        layout=Layout(
                            title = "CA Fire: {}".format(forecast_type)
, 
                            autosize=True,
                            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                            showlegend=False,
                            mapbox=dict(
                                accesstoken=mapbox_access_token,
                                center=dict(lat=latInitial, lon=lonInitial), 
                                style=map_type,
                                bearing=bearing,
                                zoom=zoom,
                            ),
                            geo = {
                                      "scope": "world",
                                      "center": {
                                                "lat": latInitial,
                                                "lon": lonInitial,
                                                  },
                                      'showocean': True,
                                      'projection' : {
                                            "type": "mercator",
                                            "scale": 27.846113156698145,
                                            "rotation": {"lon":lonInitial}
                                          },
                                      'resolution' : 110,
                                      'showcountries' : True
                                },
                            updatemenus=[
                                dict(
                                    buttons=(
                                        [
                                            dict(
                                                args=[
                                                    {
                                                        "mapbox.zoom": zoom,
                                                        "mapbox.center.lon": str(lonInitial),
                                                        "mapbox.center.lat": str(latInitial),
                                                        "mapbox.bearing": bearing,
                                                        "mapbox.style": map_type,
                                                    }
                                                ],
                                                label="Reset Zoom",
                                                method="relayout",
                                            )
                                        ]
                                    ),
                                    direction="left",
                                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                                    showactive=False,
                                    type="buttons",
                                    x=0.45,
                                    y=0.02,
                                    xanchor="left",
                                    yanchor="bottom",
                                    bgcolor="#323130",
                                    borderwidth=1,
                                    bordercolor="#6d6d6d",
                                    font=dict(color="#FFFFFF"),
                                )
                            ],
                        ),
                    )
        return fig


    if not timestep_value:
        timestep_value = ""
        fire_count = "Select the hour"
        forecast_type = ""
        weather_checklist = None
    else:
        if forecast_type == "Previous day - actual":
            timestep_value = "{} hours ago".format(timestep_value)
            fire_count = "Total Actual Fires: {}".format(fire_count)
        else:
            timestep_value = "{} hours from now".format(timestep_value)
            fire_count = "Total Forecasted Fires: {}".format(fire_count)


    return update_data(dff,dff_w, forecast_type, map_type, weather_checklist, weather_opacity), dff.to_dict('records'), csv_string, fire_count, forecast_type, timestep_value


if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(host='0.0.0.0', debug=True, port=8080)