# Dash-based dashboards

Dashboard apps for EOSC 372, [Introductory Oceanography: Circulation and Plankton](https://www.eoas.ubc.ca/academics/courses/eosc372).

First attemp uses [mapbox-layers](https://plotly.com/python/mapbox-layers/) to plot measurement locations on a map (data gathered from GEOTRACES - see app.py), then displays temperature and salinity on vertical graphs next to the map based on mouse-over (hover) on points of the map.

The "app.py" file includes comments and attributions for data sources and code inspirations.

File "latlon-list-1each.csv" was constructed by parsing all data files using "parse-csv.py". 

Folder "data" contains all the soundings data from this GEOTRACE GP15 mission. They must be there for code to run since each sounding-data plot is read in only as needed.

Data were culled so only "drop 2" at each location was used. This may not be the optimal choice, but better choices require reviewing all 167 data sets. For example, station 4, drop 9 extends to 5700 meters.  