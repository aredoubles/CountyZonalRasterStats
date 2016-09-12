from rasterstats import zonal_stats
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

'''
Have to repeat this zonal_stats calculation
For every year
'''
# First batch-generate the variable/file names
str15 = map(str, range(15))
for x in range(10):
    str15[x] = str(0) + str15[x]
clim_nms = range(15)
for x in range(15):
    clim_nms[x] = 'bioclim20' + str15[x]
clim_files = range(15)
for x in range(15):
    clim_files[x] = 'Clim/Bioclim/' + clim_nms[x] + '.tif'

# Get zonal stats for each year's bioclim data

'''
Create a dictionary to hold the zonal stats for each string/variable name
This test seemed to work fine:
testdict = {}
for x in range(15):
    testdict[x] = x * 5
'''
bioclims_all = {}

for x in range(15):
    bioclims_all[clim_nms[x]] = zonal_stats('Counties/tl_2016_us_county.shp',
                                            clim_files[x],
                                            stats="mean std", band=1, geojson_out=True)

'''
Should look like:
'bioclim2000' : Huge JSON output
'bioclim2001' : Huge JSON output
etc.
'''

'''
Original, lone-year implementation
bioclim_2000 = zonal_stats('Counties/tl_2016_us_county.shp',
                           'Clim/Bioclim/bioclim_2000.tif',
                           stats="mean std", band=1, geojson_out=True)
'''

'''
# Flatten the JSON file into a dataframe
flatson = json_normalize(us_bioclim)
# Takes 2.5 minutes to complete
slimson = flatson[[12, 13, 17, 19, 20, 21]]
slimson.columns = ['Lat', 'Lon', 'Name', 'State', 'Mean', 'StDev']
slimson['CtyID'] = slimson['Name'] + '_' + slimson['State']
slimson = slimson.set_index('CtyID')
slimson.to_csv('precip_2001.csv')
'''

for key in bioclims_all:
    flatson = json_normalize(bioclims_all[key])
    slimson = flatson[[12, 13, 17, 19, 20, 21]]
    slimson.columns = ['Lat', 'Lon', 'Name', 'State', 'Mean', 'StDev']
    slimson['CtyID'] = slimson['Name'] + '_' + slimson['State']
    slimson = slimson.set_index('CtyID')
    fname = key + '.csv'
    slimson.to_csv(fname)



# slimson.ix['Barnstable_25']
# MA is state #25
