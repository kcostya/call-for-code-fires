import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from flask import Flask
import numpy as np
import dash_table



df_fp = pd.read_csv('sample_df_start_2016-04-21_12_00_00.csv')
df_h = pd.read_csv('historical_df_start_2016-04-20_12_00_00.csv')
df_wp = pd.read_csv('sample_start_2016-04-21_12h_step_12h_pred_noinputfire_bestseparator_min079.csv')


### Define Starting Fig ####

chart_type = "scattermapbox"
mapbox_access_token = "pk.eyJ1IjoicnNheGJ5IiwiYSI6ImNqeWNxcHh4MDBsMDMzYmtvbWMyc2VzODQifQ.35O16QEQ1KwDovug6aBQ7Q"


data = dict(
            type=chart_type, 
            meta =  dict(columnNames = {
                                      "lat": "lat", 
                                      "lon": "lon", 
                                      "fire count": "fire count", 
                                        "timestamp": "timestamp"
                                    },
                         colorscale='jet',
                         colorbar=dict(thickness=20, ticklen=4),

                        ), 
            mode = "markers", 
            name = '12', 
            lat = list(df_fp['lat']),
            lon = list(df_fp['lon']), 
            visible = True,
            marker = dict(
                    cmax = 15, 
                    cmin = 0, 
                    opacity = 0.4, 
                    sizeref = 0.03333333333333333, 
                    size = list(df_fp['fire count']),
                    color = list(df_fp['fire count']),
                    sizemode = "area", 
                    showscale = True, 
                    # symbol = 'square',
                ),
            text = list(df_fp['fire count'].astype(str)),
            ), 
layout = dict(
              title = "CA Fires", 
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
                              header=dict(values= ['timestep', "lat", "lon", "fire count"],
                                          fill_color='darkkhaki',
                                          align='left',
                                           ),
                              cells=dict(values=[df_fp.timestep, df_fp.lat, df_fp.lon, df_fp['fire count']],
                                         fill_color='antiquewhite',
                                         align='left'))
                  ])

### DASH layout ####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

filter_options = ['(-0.001, 1.0]', '(1.0, 5.0]', '(5.0, 10.0]', '(10.0, 100.0]']

app.layout = html.Div([
    html.Div([

#### Div 1 for dropdown menu
        html.Div([
            dcc.Dropdown(
                id='fire-count-display',
                options=[{'label': i, 'value': i} for i in filter_options],
                value=filter_options,
                multi=True,
                # placeholder="Select fire count range",

                ),
            dcc.RadioItems(
                id='forecast-type',
                options=[{'label': i, 'value': i} for i in ['Fire-driven forecast', 'Weather-driven forecast', 'Previous day - actual']],
                value='Fire-driven forecast',
                labelStyle={'display': 'inline-block'}
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
            ## table
             # dcc.Graph(id='table'),

            ], style={'width': '50%', 'position':'fixed', 'left':'70%', 'top':'50%', 'margin-top':-300, 'margin-left':-300}),

  html.Div([
      dcc.Graph(id='datatable'),
      # dash_table.DataTable(
      #     id='datatable',
      #     columns=[
      #         {"name": i, "id": i, "deletable": True} for i in df.columns if i not in ['fire count category', 'timestep']
      #     ],
      #     data=df.to_dict('records'),
      #     fill_width=False,
      #     page_size=12,
      #     sort_action='native',
      # ),
  ], style={'width': '50%', 'position':'fixed', 'left':'25%', 'top':'25%', 'margin-bottom':-300, 'margin-left':-300})



])

## Call backs
@app.callback(
    # we want to filter by fire count only
    [Output('firecount-graphic', 'figure'),
    Output('datatable', 'figure')],
    [Input('fire-count-display', 'value'),
     Input('timestep--slider', 'value'),
     Input('forecast-type', 'value'),]) #

## Update the figure itself
def update_fig(fire_count,timestep_value, forecast_type):
  dff = df_fp

  if forecast_type == 'Weather-driven forecast':
    dff = df_wp
  elif forecast_type == 'Previous day - actual':
    dff = df_h

  if isinstance(fire_count, str):
    dff = dff[(dff['timestep'] == timestep_value) & (dff['fire count category'] == fire_count)]
  else:
    dff = dff[(dff['timestep'] == timestep_value) & (dff['fire count category'].isin(fire_count))]

  ## Update the data within the figure
  def update_data(df, fig1, fig2):

    # for table
    df.sort_values(by='fire count', inplace=True, ascending=False)
    fig2['data'][0]['cells']['values'] = [df.timestep, df.lat, df.lon, df['fire count']]

    # access the first (and only trace) of the data, then reassign the properties
    fig['data'][0]['name'] = timestep_value
    fig['data'][0]['lat']  = list(df['lat']) if len(df['lat']) > 0 else [0]
    fig['data'][0]['lon'] = list(df['lon'])if len(df['lon']) > 0 else [0]
    fig['data'][0]['marker'] = dict(
                          cmax = 25, 
                          cmin = 0, 
                          opacity = 0.4, 
                          sizeref = 0.03333333333333333, 
                          size = list(df['fire count']),
                          color = list(df['fire count']),
                          sizemode = "area", 
                          showscale = True, )
    fig['data'][0]['text'] = list(df['fire count'].astype(str))

    return fig1, fig2

  return update_data(dff, fig, fig2)




if __name__ == '__main__':
  # local
  # app.run_server(debug=True, port=8000) #%tb
  # public
  app.run_server(debug=True)



