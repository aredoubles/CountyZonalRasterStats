import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
from path import path
import time
from progressbar import Bar, Percentage, ProgressBar, ETA

dbname = 'lymeforecast'
username = 'rogershaw'
engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

con = None
con = psycopg2.connect(database=dbname, user=username)

# Add Lyme Data


def BuildLyme(ctycode0):
    lyme_data = pd.read_csv('lyme_CtyID.csv', index_col='CtyID')
    # Subset to just the Years columns
    lyme_data = lyme_data[
        [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]
    # Rename columns (will later become rows in county table)
    lyme_data.loc['YrCol'] = range(2000, 2015, 1)
    yrcol = lyme_data.iloc[-1]
    lyme_data = lyme_data[:-1]
    lyme_data = lyme_data.rename(columns=yrcol)
    # Query the county we're working with
    thislyme = lyme_data.ix[ctycode0]
    thislyme = thislyme.ix[5:]     # Row vector, cases in each year
    lymebuild = pd.DataFrame(thislyme)
    lymebuild.rename(columns={ctycode0: 'lymecases'}, inplace=True)
    lymebuild.index.name = 'Year'
    if ctycode0[-2:] == '09':
        ctquery = 'SELECT * FROM ct2015'
        ct15 = pd.read_sql_query(ctquery, con, index_col='county')
        lymebuild.set_value(2015, 'lymecases', ct15.ix[ctycode0][1])
    lymebuild['county'] = ctycode0
    return lymebuild
# Returns 'lymebuild', a dataframe of years x Lyme, county-code

# Add Bioclim data


def BioClim(ctycode, lymebuild, ctycode0):
    for band in range(1, 20, 1):
        band0 = '{}{}{}'.format('bio', str(0), band)
        band = 'bio' + str(band)
        for yr in range(2000, 2016, 1):
            # Get all these variables names set
            yr = str(yr)
            #yrvar = '{}{}{}'.format('"mean-bio8-', yr[-2:], '"')
            yrvar = '{}{}{}{}{}'.format('"mean-', band, '-', yr[-2:], '"')
            #yrtab = '{}{}{}'.format('"bio8.bio8-20', yr[-2:], '"')
            yrtab = '{}{}{}{}{}{}{}'.format(
                '"', band, '.', band, '-20', yr[-2:], '"')
            '''Needs to be ctycode0, if state code is < 10. How to tell?'''
            if ctycode[-2].isdigit() == True:
                ctystrquo = '{}{}{}'.format("'", ctycode, "'")
            else: ctystrquo = '{}{}{}'.format("'", ctycode0, "'")
            sql_query = '{} {} {} {} {} {}'.format('SELECT', yrvar, 'FROM', yrtab,
                                                   'WHERE "CtyID" =', ctystrquo)
            cell_from_sql = pd.read_sql_query(sql_query, con)
            lymebuild.set_value(
                int(yr), band0, cell_from_sql.ix[0, yrvar[1:-1]])
    lymebuild.set_value(2015, 'county', ctycode0)
    countybio = lymebuild
    return countybio
# returns 'countybio', a complete dataframe for a single county

# Add lat/lon


def LatLon(ctycode, countybio, ctycode0):      # ctycode = Bioclim, has lat/lon
    if ctycode[-2].isdigit() == True:
        quotecounty = '{}{}{}'.format("'", ctycode, "'")
    else: quotecounty = '{}{}{}'.format("'", ctycode0, "'")
    latlonquery = '{}{}'.format(
        '''SELECT "Lat", "Lon" FROM "bio1.bio1-2000" WHERE "CtyID" = ''', quotecounty)
    latlonsql = pd.read_sql_query(latlonquery, con)
    countybio['lat'] = latlonsql['Lat'][0]
    countybio['lon'] = latlonsql['Lon'][0]
    countyspace = countybio
    return countyspace
# Returns 'countyspace', a dataframe that also includes lat/lon

# Add populations


def PopAdd(ctycode, countyspace, ctycode0):
    # for each year of pop, grab cell, add, fill in other values
    for yr in range(2000, 2016, 5):
        yr = str(yr)
        yearfile = '{}{}{}'.format('pop', yr, '.csv')
        yeartable = '{}{}{}{}'.format('"', 'populations.pop', yr, '"')
        denstable = '{}{}{}{}'.format('"', 'populations.popdens', yr, '"')
        if ctycode[-2].isdigit() == True:
            quotecounty = '{}{}{}'.format("'", ctycode, "'")
        else: quotecounty = '{}{}{}'.format("'", ctycode0, "'")
        yrquery = '{} {} {} {}'.format('''SELECT "Mean" FROM''', yeartable,
                                       '''WHERE "CtyID" =''', quotecounty)
        densquery = '{} {} {} {}'.format('''SELECT "Mean" FROM''', denstable,
                                       '''WHERE "CtyID" =''', quotecounty)
        cell_from_sql = pd.read_sql_query(yrquery, con)
        dens_from_sql = pd.read_sql_query(densquery, con)
        countyspace.set_value(
            int(yr), 'population', cell_from_sql.ix[0, 0])
        countyspace.set_value(
            int(yr), 'popdens', dens_from_sql.ix[0, 0])
    for yr in range(2001,2005,1):
        interp = countyspace.ix[2000, 'population']
        densinter = countyspace.ix[2000, 'popdens']
        countyspace.set_value(
            int(yr), 'population', interp)
        countyspace.set_value(
            int(yr), 'popdens', densinter)
    for yr in range(2006,2010,1):
        interp = countyspace.ix[2005, 'population']
        densinter = countyspace.ix[2005, 'popdens']
        countyspace.set_value(
            int(yr), 'population', interp)
        countyspace.set_value(
            int(yr), 'popdens', densinter)
    for yr in range(2011,2015,1):
        interp = countyspace.ix[2010, 'population']
        densinter = countyspace.ix[2010, 'popdens']
        countyspace.set_value(
            int(yr), 'population', interp)
        countyspace.set_value(
            int(yr), 'popdens', densinter)

    pluspop = countyspace
    return pluspop
# Returns 'pluspop', the completed dataframe for the county

# Send to CSV and SQL
def Saveways(ctycode, fullcounty):
    namecsv = '{}{}{}'.format('CountyTables/', ctycode, '.csv')
    namesql = 'counties.' + ctycode
    fullcounty.to_csv(namecsv)
    fullcounty.to_sql(namesql, engine, if_exists='replace')

# Generate list of counties to include
def CountyList():
    bigquery = '''
    SELECT "Name", "State", "CtyID" FROM "bio1.bio1-2000" WHERE
    "State" = 25 OR
    "State" = 44 OR
    "State" = 9 OR
    "State" = 33 OR
    "State" = 50 OR
    "State" = 23
    '''
    biglist = pd.read_sql_query(bigquery, con)
    return biglist

    '''
    Number of counties:
    Massachusetts (25): 14
    Connecticut (9): 8
    Rhode Island (44): 5
    New Hampshire (33): 10
    Vermont (50): 14
    Maine (23): 16
    TOTAL: 67
    '''

# Combine all counties into a grandtable, save to csv and sql
def CombineCounties():
    i=1
    cpath = path('CountyTables')
    for f in cpath.files(pattern='*.csv'):
        if i == 1:   # Seed the grand table with the first county table
            GrandTable = pd.read_csv(f)
            i += i
        else:
            newcount = pd.read_csv(f)
            GrandTable = pd.concat([GrandTable, newcount])
        # Save GrandTable to csv and sql
        GrandTable.to_csv('_grandtable.csv')
        GrandTable.to_sql('grandtable', engine, if_exists='replace')

def main():
    biglist = CountyList()
    totcounties = biglist.shape[0]

    pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=totcounties).start()

    for index, row in biglist.iterrows():
        ctycode = row['CtyID']                        # Barnstable25, Bioclim
        ctycode0 = '{}{}{}'.format(row['Name'], '0', row['State'])      # Barnstable025, Lyme
        lymebuild = BuildLyme(ctycode0)
        countybio = BioClim(ctycode, lymebuild, ctycode0)
        countyspace = LatLon(ctycode, countybio, ctycode0)
        pluspop = PopAdd(ctycode, countyspace, ctycode0)
        fullcounty = pluspop
        Saveways(ctycode, fullcounty)
        pbar.update(index+1)
    CombineCounties()
    pbar.finish()

main()
