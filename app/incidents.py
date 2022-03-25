from dash.dependencies import Output, Input
from dash import dash_table, html, dcc
import plotly.express as px

from data import df7
from app import app


# ----------------------------------
# app layout

fig = px.line(df7, x="Month", y="Incidents", color_discrete_sequence=px.colors.qualitative.T10)

fig.update_xaxes(showline=True, linecolor='black', linewidth=2)
fig.update_yaxes(showgrid=False, showline=True, linecolor='black',gridcolor='Orange')
fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
                        # margin=dict(t=100, b=0, l=70, r=40),
                        # hovermode="x unified",
                        # xaxis_tickangle=360,
                        # xaxis_title=' ', yaxis_title=" ",
                        # plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
                        # title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                        # font=dict(color='#8a8d93'),
                        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        #   )


incidents_layout = html.Div([

    html.Br(),
    html.H3('Total Incidents'),
    html.Br(),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in ['Month','Incidents']],
        data=df7.to_dict('records'),
        style_cell=dict(textAlign='left', height='auto', width='200px'),
        style_header=dict(backgroundColor="paleturquoise", fontWeight='bold'),
        style_data=dict(backgroundColor="lavender")
    ),

    html.Br(),

    dcc.Graph(id="graph", figure=fig),

])

# -------------------------------------------
# app callback