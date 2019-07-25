import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from flask import Flask
import numpy as np
import dash_table
import urllib
import glob


## Whether or not to use nrt data
use_nrt = False

if use_nrt:
  ## Read in NRT data ##
  all_files = glob.glob('nrt/*.csv')
  dfs = []

  for csv in all_files:
      df = pd.read_csv(csv, index_col=None, header=0)
      dfs.append(df)

  df_h = pd.concat(dfs, axis=0, ignore_index=True)

else:
  df_h = pd.read_csv('historical_df_start_2016-04-20_12_00_00.csv')

## The fire driven and weather driven predictions
df_fp = pd.read_csv('sample_df_start_2016-04-21_12_00_00.csv')
df_wp = pd.read_csv('sample_start_2016-04-21_12h_step_12h_pred_noinputfire_bestseparator_min079.csv')


## parameters for display
colorbar_max_val = 8
opacity = 1
marker_size = 12
colorscale = 'Viridis'#[[0, "rgb(166,206,227)"],
              # [0.25, "rgb(31,120,180)"],
              # [0.45, "rgb(178,223,138)"],
              # [0.65, "rgb(51,160,44)"],
              # [0.85, "rgb(251,154,153)"],
              # [1, "rgb(227,26,28)"]]
max_table_rows = 10

#### Define Starting Fig ####

chart_type = "scattermapbox"
mapbox_access_token = "pk.eyJ1IjoicnNheGJ5IiwiYSI6ImNqeWNxcHh4MDBsMDMzYmtvbWMyc2VzODQifQ.35O16QEQ1KwDovug6aBQ7Q"

def generate_table(dataframe, max_rows=max_table_rows):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


data = dict(
            type=chart_type, 
            meta =  dict(columnNames = {
                                      "lat": "lat", 
                                      "lon": "lon", 
                                      "fire count": "fire count", 
                                        "timestamp": "timestamp"
                                    },
                         # colorscale='jet',
                         colorbar=dict(thickness=20, ticklen=4,),

                        ), 
            mode = "markers", 
            name = '12', 
            lat = list(df_fp['lat']),
            lon = list(df_fp['lon']), 
            visible = True,
            marker = dict(
                    cmax = colorbar_max_val, 
                    cmin = 0, 
                    opacity = opacity,
                    colorscale= colorscale, 
                    sizeref = 0.03333333333333333, 
                    size = marker_size,
                    color = list(df_fp['fire count']),
                    sizemode = "area", 
                    showscale = True, 
                    # symbol = 'square',
                ),
            text = list(df_fp['fire count'].astype(str)),
            ), 
layout = dict(
              title = "CA Fires: Fire-driven Forecast", 
              width = 600, 
              height = 600, 
              autosize = False,
              hovermode = 'closest',
              showlegend = False,
              mapbox = go.layout.Mapbox(
                                  bearing=0,
                                  accesstoken=mapbox_access_token,
                                  center=go.layout.mapbox.Center(
                                                  lat=37.48049902482438,
                                                  lon=-118.33128991907188
                                                  ),
                                  pitch=0,
                                  zoom=4.50511930149945,
                                  style='satellite',
                                          ),

            geo = {
                      "scope": "world", 
                      "center": {
                                "lat": 37.44589155769352, 
                                "lon": -118.59118404059357
                                  }, 
                      'showocean': True, 
                      'projection' : {
                            "type": "mercator", 
                            "scale": 27.846113156698145, 
                            "rotation": {"lon": -118.59118404059357}
                          }, 
                      'resolution' : 110, 
                      'showcountries' : True
                },  
            xaxis= {
                  "range": [-1, 6], 
                  "autorange": True
                }, 
            yaxis= {
                  "range": [-1, 4], 
                  "autorange": True
                }, 
            legend = {"xanchor": "auto"}, 
            dragmode = "pan", 
            template= {
                  "data": {
                    "bar": [
                              {
                        "type": "bar", 
                        "marker": {"colorbar": {
                                                "ticks": "", 
                                                "outlinewidth": 0
                                                  }
                                  }
                              }
                            ], 
                    'table': [
                              {
                                "type": "table", 
                                "cells": {
                                          "fill": {"color": "#EBF0F8"}, 
                                          "line": {"color": "white"}
                                        }, 
                                "header": {
                                          "fill": {"color": "#C8D4E3"}, 
                                          "line": {"color": "white"}
                                        }
                                  }
                            ], 
                          }, 
                  'layout':{
                        "geo": {
                              "bgcolor": "white", 
                              "showland": True, 
                              "lakecolor": "white", 
                              "landcolor": "white", 
                              "showlakes": True, 
                              "subunitcolor": "#C8D4E3"
                            }, 
                        "font": {"color": "#2a3f5f"}, 
                        "polar": {
                                  "bgcolor": "white", 
                                  "radialaxis": {
                                                "ticks": "", 
                                                "gridcolor": "#EBF0F8", 
                                                "linecolor": "#EBF0F8"
                                              }, 
                                  "angularaxis": {
                                            "ticks": "", 
                                            "gridcolor": "#EBF0F8", 
                                            "linecolor": "#EBF0F8"
                                              }
                                    }, 
                    'scene': {
                              "xaxis": {
                                "ticks": "", 
                                "gridcolor": "#DFE8F3", 
                                "gridwidth": 2, 
                                "linecolor": "#EBF0F8", 
                                "zerolinecolor": "#EBF0F8", 
                                "showbackground": True, 
                                "backgroundcolor": "white"
                              }, 
                          "yaxis": {
                                "ticks": "", 
                                "gridcolor": "#DFE8F3", 
                                "gridwidth": 2, 
                                "linecolor": "#EBF0F8", 
                                "zerolinecolor": "#EBF0F8", 
                                "showbackground": True, 
                                "backgroundcolor": "white"
                              }, 
                          "zaxis": {
                                "ticks": "", 
                                "gridcolor": "#DFE8F3", 
                                "gridwidth": 2, 
                                "linecolor": "#EBF0F8", 
                                "zerolinecolor": "#EBF0F8", 
                                "showbackground": True, 
                                "backgroundcolor": "white"
                              }
                        }, 
                    'xaxis' : {
                          "ticks": "", 
                          "gridcolor": "#EBF0F8", 
                          "linecolor": "#EBF0F8", 
                          "automargin": True, 
                          "zerolinecolor": "#EBF0F8", 
                          "zerolinewidth": 2
                        }, 
                    'yaxis': {
                          "ticks": "", 
                          "gridcolor": "#EBF0F8", 
                          "linecolor": "#EBF0F8", 
                          "automargin": True, 
                          "zerolinecolor": "#EBF0F8", 
                          "zerolinewidth": 2
                        }, 
                    'ternary':{
                          "aaxis": {
                                    "ticks": "", 
                                    "gridcolor": "#DFE8F3", 
                                    "linecolor": "#A2B1C6"
                                  }, 
                          "baxis": {
                                    "ticks": "", 
                                    "gridcolor": "#DFE8F3", 
                                    "linecolor": "#A2B1C6"
                              }, 
                          "caxis": {
                                    "ticks": "", 
                                    "gridcolor": "#DFE8F3", 
                                    "linecolor": "#A2B1C6"
                              }, 
                          "bgcolor": "white"
                        }, 
                'colorway' : ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#19d3f3", "#e763fa", "#fecb52", "#ffa15a", "#ff6692", "#b6e880"], 
                'hovermode' : "closest", 
                'colorscale' : {
                              "diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], 
                              "sequential": [[0, "#0508b8"], [0.0893854748603352, "#1910d8"], [0.1787709497206704, "#3c19f0"], [0.2681564245810056, "#6b1cfb"], [0.3575418994413408, "#981cfd"], [0.44692737430167595, "#bf1cfd"], [0.5363128491620112, "#dd2bfd"], [0.6256983240223464, "#f246fe"], [0.7150837988826816, "#fc67fd"], [0.8044692737430168, "#fe88fc"], [0.8938547486033519, "#fea5fd"], [0.9832402234636871, "#febefe"], [1, "#fec3fe"]] ,
                              "sequentialminus": [[0, "#0508b8"], [0.0893854748603352, "#1910d8"], [0.1787709497206704, "#3c19f0"], [0.2681564245810056, "#6b1cfb"], [0.3575418994413408, "#981cfd"], [0.44692737430167595, "#bf1cfd"], [0.5363128491620112, "#dd2bfd"], [0.6256983240223464, "#f246fe"], [0.7150837988826816, "#fc67fd"], [0.8044692737430168, "#fe88fc"], [0.8938547486033519, "#fea5fd"], [0.9832402234636871, "#febefe"], [1, "#fec3fe"]]
                            }, 
                'plot_bgcolor' :  "white", 
                'paper_bgcolor' : "white", 
                'shapedefaults' : {
                  "line": {"width": 0}, 
                  "opacity": 0.4, 
                  "fillcolor": "#506784"
                }, 
                'annotationdefaults' : {
                  "arrowhead": 0, 
                  "arrowcolor": "#506784", 
                  "arrowwidth": 1
                }
              }, 
            }, 
          )   
data = go.Data(data)
fig = go.Figure(data=data,layout=layout)
# fig['data'][0]['marker']['symbol'] = 'square'

### Table Fig 

fig2 =  go.Figure(data=[go.Table(
                              header=dict(values= ['timestamp','timestep', "lat", "lon", "fire count"],
                                          fill_color='darkkhaki',
                                          align='left',
                                           ),
                              cells=dict(values=[df_fp.timestamp, df_fp.timestep, df_fp.lat, df_fp.lon, df_fp['fire count']],
                                         fill_color='antiquewhite',
                                         align='left'))
                  ])

### DASH layout ####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, )

server = app.server

filter_options = ['(-0.001, 1.0]', '(1.0, 5.0]', '(5.0, 10.0]', '(10.0, 100.0]']

app.layout = html.Div([
    html.Div([

#### Div 1 for dropdown menu
        html.Div([
            dcc.RadioItems(
                id='forecast-type',
                options=[{'label': i, 'value': i} for i in ['Fire-driven forecast', 'Weather-driven forecast', 'Previous day - actual']],
                value='Fire-driven forecast',
                labelStyle={'display': 'inline-block',},
                inputStyle= {'margin-right':'8px' ,'margin-top':'10px','margin-left': '18px'}
            )
             ],
        style={'width': '48%','display': 'inline-block',}),

    ]),

##### Div 2 - for graph and slider
    html.Div([
              ## fire forecast figure
              dcc.Graph(id='firecount-graphic'),
              ## slider for the timesteps
              dcc.Slider(
                id='timestep--slider',
                min=df_fp['timestep'].min(),
                max=df_fp['timestep'].max(),
                value=df_fp['timestep'].min(),
                marks={str(timestep): str(timestep) for timestep in df_fp['timestep'].unique()},
                step=None,
                  ),
            ], style={'width': '50%', 'position':'fixed', 'left':'70%', 'top':'45%', 'margin-top':-300, 'margin-left':-300}),

  html.Div([
          dash_table.DataTable(
                              id='table-filtering-be',
                              columns=[
                                  {"name": i, "id": i} for i in df_fp.columns 
                              ],
                              filter_action='custom',
                              filter_query='',
                              style_as_list_view=True,
                              style_cell_conditional=[
                                                        {
                                                            'if': {'column_id': 'timestamp'},'width': '8%',
                                                            
                                                        },                              
                                                        {
                                                            'if': {'column_id': 'fire count'},'width': '12%',
                                                            
                                                        }, 
       
                                                         {
                                                            'if': {'column_id': 'timestep'},'width': '10%', 
                                                            
                                                        }, 
                                                         {
                                                            'if': {'column_id': 'lat'},'width': '5%',
                                                            
                                                        },
                                                         {
                                                            'if': {'column_id': 'lon'},'width': '5%',
                                                        },
                                                      ],
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
                                          'maxHeight': '450px',
                                          'maxWidth': '500px',
                                          'overflowY': 'scroll',
                                          },
                              fixed_rows={ 'headers': True, 'data': 0 },

                          ),
                  html.A(
                          'Download Data',
                          id='download-link',
                          download="rawdata.csv",
                          href="",
                          target="_blank"
                      )
  ], style={'width': '50%', 'position':'fixed', 'left':'30%', 'top':'17%', 'margin-bottom':-300, 'margin-left':-325})

])

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


## Call backs
@app.callback(
    # we want to filter by fire count only
    [Output('firecount-graphic', 'figure'),
    dash.dependencies.Output('table-filtering-be', "data"),
    dash.dependencies.Output('download-link', 'href')],
    [
     Input('timestep--slider', 'value'),
     Input('forecast-type', 'value'),
     dash.dependencies.Input('table-filtering-be', "filter_query")]) #

## Update the figure itself
def update_fig(timestep_value, forecast_type, filter_query):
  dff = df_fp

  if forecast_type == 'Weather-driven forecast':
    dff = df_wp
  elif forecast_type == 'Previous day - actual':
    dff = df_h

  dff = dff[(dff['timestep'] == timestep_value)]
  fig.layout.title = "CA Fire: {}".format(forecast_type)


  def update_table(df, filter):
      filtering_expressions = filter.split(' && ')
      for filter_part in filtering_expressions:
          col_name, operator, filter_value = split_filter_part(filter_part)

          if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
              # these operators match pandas series operator method names
              df = df.loc[getattr(df[col_name], operator)(filter_value)]
          elif operator == 'contains':
              df = df.loc[dff[col_name].str.contains(filter_value)]
          elif operator == 'datestartswith':
              # this is a simplification of the front-end filtering logic,
              # only works with complete fields in standard format
              df = df.loc[df[col_name].str.startswith(filter_value)]
      return df


  dff = update_table(dff, filter_query)

  csv_string = dff.to_csv(index=False, encoding='utf-8')
  csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)

  ## Update the data within the figure
  def update_data(df, fig):

    # for table
    df.sort_values(by='fire count', inplace=True, ascending=False)

    # access the first (and only trace) of the data, then reassign the properties
    fig['data'][0]['name'] = timestep_value
    fig['data'][0]['lat']  = list(df['lat']) if len(df['lat']) > 0 else [0]
    fig['data'][0]['lon'] = list(df['lon'])if len(df['lon']) > 0 else [0]
    fig['data'][0]['marker'] = dict(
                          cmax = colorbar_max_val, 
                          cmin = 0, 
                          opacity = opacity, 
                          sizeref = 0.03333333333333333,
                          colorscale = colorscale, 
                          size = marker_size, #list(df['fire count']),
                          color = list(df['fire count']),
                          sizemode = "area", 
                          showscale = True, )
    fig['data'][0]['text'] = list(df['fire count'].astype(str))
    return fig

  return update_data(dff, fig), dff.to_dict('records'), csv_string




if __name__ == '__main__':
  # local 
  app.run_server(debug=True)
  #public
  # app.run_server(host='0.0.0.0', debug=True, port=8080)




