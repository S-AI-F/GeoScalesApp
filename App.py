
# load census data

import pandas as pd
census_data_all = pd.read_csv("assets/communes_regions_census_2017.csv")

census_data_all['PopTotalv2'] = 2 * census_data_all['PopulationTotal']



# load geojson

import json

# load geojson data from local file
with open("assets/geo_regions_municipalities.json") as f:
    geo_zones = json.load(f)

# load geojson data from url
# content = requests.get("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson")
# geo_zones = json.loads(content.content)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# css style

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB],
    # specify meta_tags in order to make the app responsive to width-device
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "OpenGeoKPI"
server = app.server

# navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Navbar Simple",
    brand_href="#",
    color="secondary",
    dark=True,
)

# scale selection


scale_selection_text = html.P(
    'Select scale:',
    style={
        'font-size': '120%',
        'margin-bottom': '15px',
        'margin-top': '15px',
        'margin-left': '5%'
    }
)

dropdown_scale = dcc.Dropdown(
    id='scale',
    options=[
        {'label': 'Municipality', 'value': 'Municipality'},
        {'label': 'Region', 'value': 'Region'}
    ],
    value='Region',
    style={
        'width': '90%',
        # 'width': '400px',
        'margin-left': '2%'}
)

# kpi selector

kpi_selection_text = html.P(
    'Select KPI:',
    style={
        'font-size': '120%',
        'margin-bottom': '15px',
        'margin-top': '15px',
        'margin-left': '5%'
    }
)

dropdown_kpi = dcc.Dropdown(
    id='kpi',
    # options=[{'label': i, 'value': i} for i in communes_list],
    options=[
        {'label': 'Population', 'value': 'PopulationTotal'},
        {'label': 'Population v2', 'value': 'PopTotalv2'}
    ],
    # value='PopulationTotal',
    style={
        'width': '90%',
        'margin-left': '2%',
        'margin-bottom': '15px',
    }
)

# body

body = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            scale_selection_text
                        ),
                        dbc.Row(
                            dropdown_scale
                        ),
                        dbc.Row(
                            kpi_selection_text
                        ),
                        dbc.Row(
                            dropdown_kpi
                        )
                    ],
                    md=4
                ),
                dbc.Col(
                    dcc.Graph(id='map_communes'),
                    md=8
                )
            ]
        )
    ],
    className="mt-2",
    fluid=True
)

app.layout = html.Div([navbar, body])


@app.callback(
    Output('map_communes', 'figure'),
    [
        Input('scale', 'value'),
        Input('kpi', 'value'),
     ]
)
def update_map_kpi(scale, kpi):
    data = census_data_all[census_data_all['Level'] == scale]
    fig = px.choropleth_mapbox(data,
                               geojson=geo_zones,
                               color=kpi,
                               locations="Code", featureidkey="properties.Code",
                               center={"lat": 48.8534, "lon": 2.3488},
                               mapbox_style="carto-positron", zoom=7, height=600)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == '__main__':
    app.run_server()

# app.run_server(debug=True, use_reloader=False)