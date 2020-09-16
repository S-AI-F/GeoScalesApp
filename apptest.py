import pandas as pd
import plotly.express as px
import json

# load census data
census_data_all = pd.read_csv("assets/communes_regions_census_2017.csv")
census_data_all['PopTotalv2'] = 2 * census_data_all['PopulationTotal']

# load geojson data from local file
with open("assets/geo_regions_municipalities.json") as f:
    geo_zones = json.load(f)

# filter data
scale = 'Region'
kpi = 'PopulationTotal'

data = census_data_all[census_data_all['Level'] == scale]
fig = px.choropleth_mapbox(data,
                           geojson=geo_zones,
                           color=kpi,
                           locations="Code", featureidkey="properties.Code",
                           center={"lat": 48.8534, "lon": 2.3488},
                           mapbox_style="carto-positron", zoom=7, height=600)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


fig.show()