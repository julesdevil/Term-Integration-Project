from dash.dependencies import Output, Input
from dash import dash_table, html, dcc
import plotly.express as px

from data import df3, df4
from style import app


# ----------------------------------
# app layout

SLA_layout = html.Div([

    html.Br(),
    html.H3('Incidents meeting SLA'),

    dcc.Dropdown(
        id="select_month3",
        options=[{"label": "January", "value": '2021-01'},
                 {"label": "February", "value": '2021-02'},
                 {"label": "March", "value": '2021-03'},
                 {"label": "April", "value": '2021-04'}],
        multi=False,
        value='2021-01',
        style={'width': "40%"}
    ), 

    dcc.Dropdown(
        id="select_priority3",
        options=[{"label": "Low", "value": 'Low'},
                 {"label": "Medium", "value": 'Medium'},
                 {"label": "High", "value": 'High'},
                 {"label": "Critical", "value": 'Critical'}],
        multi=False,
        value='Low',
        style={'width': "40%"}
    ), 


    html.Br(),

    dash_table.DataTable(
        id='table3',
        columns=[{"name": i, "id": i} for i in ['Priority', 'meets SLA?', 'Incidents']],
        data=df3.to_dict('records'),
        style_cell=dict(textAlign='left', height='auto', width='200px'),
        style_header=dict(backgroundColor="paleturquoise", fontWeight='bold'),
        style_data=dict(backgroundColor="lavender")
    ),

    html.Br(),

    dcc.Graph(id="pie_chart"),

    # html.P("Month/Priority:"),    
    # dcc.Dropdown(
    #     id='sl_month',
    #     options=[{"label": "January", "value": '2021-01'},
    #              {"label": "February", "value": '2021-02'},
    #              {"label": "March", "value": '2021-03'},
    #              {"label": "April", "value": '2021-04'}],
    #     multi=False,
    #     clearable=False,
    #     value='2021-01',
    #     style={'width': "40%"}
    # ), 
    
    # dcc.Dropdown(
    #     id="sl_priority",
    #     options=[{"label": "Low", "value": 'Low'},
    #              {"label": "Medium", "value": 'Medium'},
    #              {"label": "High", "value": 'High'},
    #              {"label": "Critical", "value": 'Critical'}],
    #     multi=False,
    #     clearable=False,
    #     value='Low',
    #     style={'width': "40%"}
    # ), 

    # dcc.Graph(id="pie_chart"),

    # html.Br(),

])

# -------------------------------------------
# app callback

@app.callback(
    [Output('table3', 'data'),
    Output('pie_chart', 'figure')],
    [Input('select_month3', 'value'),
    Input('select_priority3', 'value')]
)
def update_rows(selected_month, selected_priority):
    dff3 = df3[(df3['Create Date-Time'] == selected_month) & (df3['Priority'] == selected_priority)]
    dff4 = df4

    sla_yes = dff4[(dff4['Create Date-Time'] == selected_month) & (dff4['Priority'] == selected_priority)]['meets SLA?_yes'].sum()
    sla_no = dff4[(dff4['Create Date-Time'] == selected_month) & (dff4['Priority'] == selected_priority)]['meets SLA?_no'].sum()
    sla_unresolved = dff4[(dff4['Create Date-Time'] == selected_month) & (dff4['Priority'] == selected_priority)]['meets SLA?_unresolved'].sum()

    piechart = px.pie(  data_frame = dff4, 
                        values = [sla_yes, sla_no, sla_unresolved],
                        names = ['Yes', 'No', 'Unresolved'], 
                        hole = .4, 
                        color_discrete_sequence = px.colors.qualitative.T10
                        )

    return dff3.to_dict('records'), (piechart)


# @app.callback(
#     Output('pie_chart', 'figure'),
#     [Input('sl_month', 'value'),
#     Input('sl_priority', 'value')]
#     )
# # def update_rows(month, priority):
# def update_rows(sel_month, sel_priority):
#     dff4 = df4

#     sla_yes = dff4[(dff4['Create Date-Time'] == sel_month) & (dff4['Priority'] == sel_priority)]['meets SLA?_yes'].sum()
#     sla_no = dff4[(dff4['Create Date-Time'] == sel_month) & (dff4['Priority'] == sel_priority)]['meets SLA?_no'].sum()
#     sla_unresolved = dff4[(dff4['Create Date-Time'] == sel_month) & (dff4['Priority'] == sel_priority)]['meets SLA?_unresolved'].sum()

#     piechart = px.pie(  data_frame = dff4, 
#                         values = [sla_yes, sla_no, sla_unresolved],
#                         names = ['Yes', 'No', 'Unresolved'], 
#                         hole = .4, 
#                         color_discrete_sequence = px.colors.sequential.RdBu
#                         )
#     return (piechart)