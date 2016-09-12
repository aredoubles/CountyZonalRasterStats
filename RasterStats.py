from rasterstats import zonal_stats
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

'''
Point this towards the new Bioclim geotiff instead
Have to specify each band
There are 19 bands, for the 19 Bioclim variables
'''
us_bioclim = zonal_stats("Counties/tl_2016_us_county.shp",
                         "Clim/bioclim_daymet.tif",
                         stats="mean std", band=1, geojson_out=True)

# In GeoJSON format...what other options do I have? Otherwise it's a list?

flatson = json_normalize(precip_2001)
'''Point this twoards the new Bioclim zonal stats too'''
flatson = json_normalize(us_bioclim)
# Takes 2.5 minutes to complete

# crickets.dtypes
# Columns I want to keep from the JSON 'properties' key:
# properties.STATEFP, properties.NAME, properties.INTPTLAT,
# properties.INTPTLON, properties.mean, properties.std
# These are columns:
# 12, 13, 17, 19, 20, 21

# crickets.drop(crickets.columns[[0,1,2,3,4,5,6,7,8,9,10,11]],
# axis=1,inplace=TRUE)
slimson = flatson[[12, 13, 17, 19, 20, 21]]
slimson.columns = ['Lat', 'Lon', 'Name', 'State', 'Mean', 'StDev']
slimson['CtyID'] = slimson['Name'] + '_' + slimson['State']
slimson = slimson.set_index('CtyID')


slimson.ix['Barnstable_25']
# MA is state #25

# Save this slimmer dataframe as a csv/feather

slimson.to_csv('precip_2001.csv')
