from rasterstats import zonal_stats
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
import time
import rasterio
from path import path


'''
Have to repeat this zonal_stats calculation
For each of 19 bands (bioclim variable)
'''

# Get names of bioclim files
# Run processing loop for each file
# Ultimately, should move each of these bioclim files into PostgreSQL,
# Would most likely make it easier to work with

#bio2 = rasterio.open('Clim/Bioclim/bioclim_2000.tif')
# bio2.count  # Confirm that it does have all 19 bands
# Load these rasters using Rasterio each time through?

'''
Will want to loop through bands eventually
range(2,8,1) => [2,3,4,5,6,7]
Massively indent, Atom should be able to do that.
'''

x=2
bpath = path('Clim/Bioclim')
#for x in range(2, 9, 1):
#    print '{} {} {}'.format('BAND', x, 'NOW IN PROGRESS')
for f in bpath.files(pattern='*.tif'):
    # Get zonal summaries for each year of bioclim data, focusing on Band 1
    print '{} {} {}'.format(time.ctime(), f, 'zoning in progress...')
    with rasterio.open(f) as src:
        affine = src.affine
        array = src.read(x)   # 12 is the band of interest
    zonesum = zonal_stats('Counties/tl_2016_us_county.shp', f,
                          band_num=x, stats='mean', geojson_out=True)
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
    # f sliced to remove dir and ext
    # Bioclim band/variable number also added to filename
    fname = 'bio0' + str(x) + '_' + f[13:25] + '.csv'
    slimson.to_csv(fname, encoding='utf-8')
    print '{} {} {} {} {}'.format(time.ctime(), f, 'flattened into', fname, '!')
    #print '{} {} {}'.format('BAND', x, 'NOW COMPLETED!')
# slimson.ix['Barnstable_25']
# MA is state #25
