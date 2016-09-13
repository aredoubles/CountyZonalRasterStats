from rasterstats import zonal_stats
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
import time
import os
import glob
from path import path
from unidecode import unidecode
#import sys

# Some county names have special characters, try to avoid in advance
#reload(sys)
#sys.setdefaultencoding('utf8')

'''
Have to repeat this zonal_stats calculation
For each of 19 bands (bioclim variable)
'''

# Get names of bioclim files
# Run processing loop for each file
# Ultimately, should move each of these bioclim files into PostgreSQL,
# Would most likely make it easier to work with

bpath = path('Clim/Bioclim')
for f in bpath.files(pattern='*.tif'):

    # Get zonal summaries for each year of bioclim data, focusing on Band 1
    print '{} {} {}'.format(time.ctime(), f, 'zoning in progress...')
    zonesum = zonal_stats('Counties/tl_2016_us_county.shp', f,
                          stats='mean', band=1, geojson_out=True)
    print '{} {} {}'.format(time.ctime(), f, 'zoning done!')
    # Zonal stats: 861 seconds (14.5 minutes)

    # Flatten the resulting zonal summaries, clean, write to file
    print '{} {} {}'.format(time.ctime(), f, 'flattening in progress...')
    flatson = json_normalize(zonesum)
    print '{} {} {}'.format(time.ctime(), f, 'flattening done!')
    slimson = flatson[[12, 13, 17, 19, 20]]
    slimson.columns = ['Lat', 'Lon', 'Name', 'State', 'Mean']
    # Some county names have unicode characters, decode them
    # for x in range(len(slimson['Name'])):
        # slimson['Name'][x] = unidecode(slimson['Name'][x])
    slimson['CtyID'] = slimson['Name'] + slimson['State'].apply(str)
    slimson = slimson.set_index('CtyID')
    fname = 'bio01_' + f[13:25] + '.csv'    # f sliced to remove dir and ext
    slimson.to_csv(fname, encoding = 'utf-8')
    print '{} {} {} {} {}'.format(time.ctime(), f, 'flattened into', fname, '!')


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
'''
for key in bioclims_all:
    print key
    flatson = json_normalize(bioclims_all[key])
    slimson = flatson[[12, 13, 17, 19, 20, 21]]
    slimson.columns = ['Lat', 'Lon', 'Name', 'State', 'Mean', 'StDev']
    slimson['CtyID'] = slimson['Name'] + '_' + slimson['State']
    slimson = slimson.set_index('CtyID')
    fname = 'bio01_' + key + '.csv'
    slimson.to_csv(fname)
t2 = time.time()
flattime = t2 - t1
print flattime

# slimson.ix['Barnstable_25']
# MA is state #25
'''
