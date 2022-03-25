import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import html

from style import app
from incidents import incidents_layout
from priority import priority_layout
from category import category_layout
from SLA import SLA_layout

server = app.server

# -----------------------------
# Tabs

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


# if __name__=='__main__':
#     app.run_server()
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050)