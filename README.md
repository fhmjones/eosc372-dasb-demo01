# Dash-based dashboards

Dashboard apps for EOSC 372, [Introductory Oceanography: Circulation and Plankton](https://www.eoas.ubc.ca/academics/courses/eosc372).

This first attempt (a preliminary demo for ocgy instructors) uses [mapbox-layers](https://plotly.com/python/mapbox-layers/) to plot measurement locations on a map (data gathered from GEOTRACES - see app.py), then displays temperature, salinity & oxygen on vertical graphs next to the map based on mouse-over (hover) on points of the map.

File `app.py` includes comments and attributions for data sources and code inspirations. File `parse-csv.py` is not needed for the dashboard app but was used to gather and organize the data.

File `latlon-list-1each.csv` is used by the mapping function to plot sampled locations on the map. It was constructed first by parsing all data files with `parse-csv.py` then hand-editing to simplify. Data were culled so only "drop 2" at each location was used. This may not be the optimal choice, but better choices require reviewing all 167 data sets. For example, station 4, drop 9 extends to 5700 meters. See also comments in `parse-csv.py`.

Folder "data" contains all the soundings data from this GEOTRACE GP15 mission. They must be there for code to run since data for each sounding is read only as needed.
