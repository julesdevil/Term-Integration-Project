from dash.dependencies import Output, Input
from dash import dash_table, html, dcc
import plotly.express as px

from data import df1, df5
from style import app


# ----------------------------------
# app layout

priority_layout = html.Div([

    html.Br(),
    html.H3('Incidents per Priority'),

    dcc.Dropdown(
        id="select_month",
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
        id='table',
        columns=[{"name": i, "id": i} for i in ['Priority','Incidents']],
        data=df1.to_dict('records'),
        style_cell=dict(textAlign='left', height='auto', width='200px'),
        style_header=dict(backgroundColor="paleturquoise", fontWeight='bold'),
        style_data=dict(backgroundColor="lavender")
    ),

    html.Br(),

    dcc.Dropdown(
        id="dropdown",
        options=[{"label": "Low", "value": 'Low'},
                 {"label": "Medium", "value": 'Medium'},
                 {"label": "High", "value": 'High'},
                 {"label": "Critical", "value": 'Critical'}],
        multi=False,
        clearable=False,
        value='Low',
        style={'width': "40%"}
    ),

    html.Br(),

    dcc.Graph(id="graph"),

])

# -------------------------------------------
# app callback

@app.callback(
    Output('table', 'data'),
    [Input('select_month', 'value')]
    )
def update_rows(selected_value):
    dff = df1[df1['Create Date-Time'] == selected_value]
    
    return dff.to_dict('records')

@app.callback(
    Output("graph", "figure"), 
    [Input("dropdown", "value")]
    )

def update_bar_chart(priority):

    pri = df5["Priority"] == priority

    fig = px.histogram(df5[pri], x="Create Date-Time", y="Incidents", barmode = 'group',
                 color="meets SLA?", color_discrete_sequence=px.colors.qualitative.T10)
    return fig
