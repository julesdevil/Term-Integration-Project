from dash.dependencies import Output, Input
from dash import dash_table, html, dcc
import plotly.express as px

from data import df2, df6
from style import app


# ----------------------------------
# app layout

category_layout = html.Div([

    html.Br(),
    html.H3('Incidents per Category'),

    dcc.Dropdown(
        id="select_month2",
        options=[{"label": "January", "value": '2021-01'},
                 {"label": "February", "value": '2021-02'},
                 {"label": "March", "value": '2021-03'},
                 {"label": "April", "value": '2021-04'}],
        multi=False,
        value='2021-01',
        style={'width': "40%"}
    ), 

    html.Br(),

    dash_table.DataTable(
        id='table2',
        columns=[{"name": i, "id": i} for i in ['Inc. Type','Incidents','Avg. Resolution Time']],
        data=df2.to_dict('records'),
        style_cell=dict(textAlign='left', height='auto', width='200px'),
        style_header=dict(backgroundColor="paleturquoise", fontWeight='bold'),
        style_data=dict(backgroundColor="lavender")
    ),
    
    # html.Br(), 

    # dcc.Dropdown(
    #     id="month",
    #     options=[{"label": "January", "value": '2021-01'},
    #              {"label": "February", "value": '2021-02'},
    #              {"label": "March", "value": '2021-03'},
    #              {"label": "April", "value": '2021-04'}],
    #     multi=False,
    #     clearable=False,
    #     value='2021-01',
    #     style={'width': "40%"}
    # ),

    # html.Br(),

    dcc.Graph(id="histogram"),

])

# -------------------------------------------
# app callback

@app.callback(
    [Output('table2', 'data'),
    Output("histogram", "figure")],
    [Input('select_month2', 'value')]
    )
def update_rows(selected_value):
    dff2 = df2[df2['Create Date-Time'] == selected_value]

    mon = df6["Create Date-Time"] == selected_value

    fig = px.histogram(df6[mon], x="Inc. Type", y="Incidents", color_discrete_sequence=px.colors.qualitative.T10).update_xaxes(categoryorder='total descending')

    return dff2.to_dict('records'), fig

# @app.callback(
#     Output("histogram", "figure"), 
#     [Input("month", "value")]
#     )

# def update_bar_chart(month):

#     mon = df6["Create Date-Time"] == month

#     fig = px.histogram(df6[mon], x="Inc. Type", y="Incidents", color_discrete_sequence=px.colors.qualitative.T10)
#     return fig