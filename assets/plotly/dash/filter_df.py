import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import urllib

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')



def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash(__name__)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
# app.layout = html.Div([
#     html.Label('Filter'),

#     dcc.Dropdown(
#         id='field-dropdown',
#         options=[
#             {'label': i, 'value': i} for i in
#             (['all'] + list(df['c'].unique()))],
#         value='all'
#     ),
#     html.Div(id='table'),
#     html.A(
#         'Download Data',
#         id='download-link',
#         download="rawdata.csv",
#         href="",
#         target="_blank"
#     )
# ])


app.layout = html.Div([dash_table.DataTable(
                                            id='table-filtering-be',
                                            columns=[
                                                {"name": i, "id": i} for i in sorted(df.columns)
                                            ],
                                            filter_action='custom',
                                            filter_query='',
                                            style_as_list_view=True,
                                            style_cell_conditional=[
                                                                    {
                                                                        'if': {'column_id': c},
                                                                        'textAlign': 'left'
                                                                    } for c in ['Date', 'Region']
                                                                    ],
                                            style_data_conditional=[
                                                                    {
                                                                    'if': {'row_index': 'odd'},
                                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                                    }
                                                                    ],
                                            style_header={
                                                        'backgroundColor': 'rgb(230, 230, 230)',
                                                        'fontWeight': 'bold'
                                                            },
                                            style_table={
                                                        'maxHeight': '300px',
                                                        'maxWidth': '300px',
                                                        'overflowY': 'scroll'
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

# def filter_data(value):
#     if value == 'all':
#         return df
#     else:
#         return df[df['c'] == value]






@app.callback([
    dash.dependencies.Output('table-filtering-be', "data"),
    dash.dependencies.Output('download-link', 'href')],
    [dash.dependencies.Input('table-filtering-be', "filter_query")])
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)
    return dff.to_dict('records'), csv_string


# @app.callback(
#     dash.dependencies.Output('download-link', 'href'),
#     [dash.dependencies.Input('table-filtering-be', "filter_query")])
# def update_download_link(filter_value):
#     dff = update_table(filter_value)
#     csv_string = dff.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)
#     return csv_string



if __name__ == '__main__':
    app.run_server(debug=True)