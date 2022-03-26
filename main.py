import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import dash_table, dash, html, dcc
import pandas as pd
import plotly.express as px

# ---------------------- Create Dash App ---------------------- #

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

# ---------------------- Load & Clean Data ---------------------- #

df = pd.read_csv('Data_Incidents_Raised.csv')

df.drop(['Incidenct Code','Customer Company','Incident Description','Support Group','Tower Group','Domain Group','Urgency','Resolution Description','Assigned Organization','Inc. Category','Last Modified Date','Inc. Element','Aging (Days)','Localización Cliente','Departamento Cliente'], axis=1, inplace=True)

df.drop(df.index[df['Customer Company Group'] == 'IAG CARGO'], inplace=True)
df.drop(df.index[df['Customer Company Group'] == 'IBERIA EXPRESS'], inplace=True)
df.drop(df.index[df['Customer Company Group'] == 'OTHERS'], inplace=True)
df.drop('Customer Company Group', axis=1, inplace=True)

df['Create Date-Time'] = pd.to_datetime(df['Create Date-Time'], dayfirst = True)
df['Resolution Date-Time'] = pd.to_datetime(df['Resolution Date-Time'], dayfirst = True)
df['time_to_resolve'] = df['Resolution Date-Time'] - df['Create Date-Time']

df['SLA'] = df.apply(lambda _: '', axis=1)
for i in df.index: 
    if df.Priority[i] == "Baja":
        df.at[i, 'SLA'] =  pd.Timedelta("15 days 00:00:00")
    elif df.Priority[i] == "Media":
        df.at[i, 'SLA'] =  pd.Timedelta("5 days 00:00:00")
    elif df.Priority[i] == "Alta":
        df.at[i, 'SLA'] =  pd.Timedelta("0 days 08:00:00")
    elif df.Priority[i] == "Crítica":
        df.at[i, 'SLA'] =  pd.Timedelta("0 days 04:00:00")

df['meets SLA?'] = df.apply(lambda _: '', axis=1)
for i in df.index:    
    if df.time_to_resolve[i] < df.SLA[i]:
        df.at[i, 'meets SLA?'] = "yes"
    elif df['Resolution Date-Time'].isnull()[i]:
        df.at[i, 'meets SLA?'] = "unresolved"
    else:
        df.at[i, 'meets SLA?'] = "no"

df['Priority'] = df['Priority'].replace(['Baja'],'Low')
df['Priority'] = df['Priority'].replace(['Media'],'Medium')
df['Priority'] = df['Priority'].replace(['Alta'],'High')
df['Priority'] = df['Priority'].replace(['Crítica'],'Critical')

df['Inc. Type'] = df['Inc. Type'].replace(['SECURITY ISSUE.INFORM. SECURITY POLICIES AND BEST PRACTICES'],'SECURITY ISSUE.INFORM.POLICIES')
df['Inc. Type'] = df['Inc. Type'].replace(['SECURITY ISSUE.PHYSICAL AND ENVIRONMENTAL SECURITY'],'SECURITY ISSUE.PHYSICAL SEC')

dft = df.copy()

dft['Create Date-Time'] = dft['Create Date-Time'].dt.strftime('%Y-%m')

df1 = dft.groupby(['Create Date-Time','Priority'], sort = False).size().reset_index().rename(columns={0:'Incidents'})

df2 = dft.groupby(['Create Date-Time','Inc. Type'], sort = False).size().reset_index().rename(columns={0:'Incidents'})
df2t = dft.groupby(['Create Date-Time','Inc. Type'], sort = False)['time_to_resolve'].mean().reset_index()
for i in df2t.index:
    df2t['time_to_resolve'][i] = pd.Timedelta(df2t['time_to_resolve'][i]).round(freq = 's')
df2["Avg. Resolution Time"] = df2t['time_to_resolve'].astype(str)
df2 = df2.sort_values(by='Incidents', ascending=False)

df3 = dft.groupby(['Priority','Create Date-Time','meets SLA?'], sort = True).size().reset_index().rename(columns={0:'Incidents'})

df4 = pd.get_dummies(dft, columns = ['meets SLA?'], drop_first = False)

df5 = dft

df5["Incidents"] = 1

df6 = df5

df7 = dft.groupby(['Create Date-Time'], sort = False).size().reset_index().rename(columns={0:'Incidents'})
df7.rename(columns={'Create Date-Time': 'Month'}, inplace = True)
df7['Month'] = df7['Month'].replace(['2021-01'],'January')
df7['Month'] = df7['Month'].replace(['2021-02'],'February')
df7['Month'] = df7['Month'].replace(['2021-03'],'March')
df7['Month'] = df7['Month'].replace(['2021-04'],'April')


# ---------------------- Project Dashboard ---------------------- #

# -- Tabs

app_tabs = html.Div(
     [
         dbc.Tabs(
             [
                 dbc.Tab(label="Incidents", tab_id="tab-incidents", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                 dbc.Tab(label="Priority", tab_id="tab-priority", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                 dbc.Tab(label="Category", tab_id="tab-category", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                 dbc.Tab(label="SLA Target", tab_id="tab-SLA", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
             ],
             id="tabs",
             active_tab="tab-priority",
         ),
     ], className="mt-3"
)

app.layout = dbc.Container([
    html.Br(),
    dbc.Row(dbc.Col(html.H1("Iberia KPI Calculations Dashboard",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])
])


# -- Incidents

fig = px.line(df7, x="Month", y="Incidents", color_discrete_sequence=px.colors.qualitative.T10)

fig.update_xaxes(showline=True, linecolor='black', linewidth=2)
fig.update_yaxes(showgrid=False, showline=True, linecolor='black',gridcolor='Orange')
fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

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


# -- Priority

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

# -- Category

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
    
    dcc.Graph(id="histogram"),

])


# -- SLA Target

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

])


# ---------------------- App Callback ---------------------- #

# -- Tabs

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-incidents":
        return incidents_layout
    elif tab_chosen == "tab-priority":
        return priority_layout
    elif tab_chosen == "tab-category":
        return category_layout
    elif tab_chosen == "tab-SLA":
        return SLA_layout
    return html.P("This shouldn't be displayed for now...")


# -- Priority

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


# -- Category

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


# -- SLA Target

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


# ---------------------- Main ---------------------- #

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)