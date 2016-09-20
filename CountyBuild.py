import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

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
    lymebuild['county'] = ctycode0
    lymebuild.index.name = 'Year'
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
        if ctycode[-2].isdigit() == True:
            quotecounty = '{}{}{}'.format("'", ctycode, "'")
        else: quotecounty = '{}{}{}'.format("'", ctycode0, "'")
        yrquery = '{} {} {} {}'.format('''SELECT "Mean" FROM''', yeartable,
                                       '''WHERE "CtyID" =''', quotecounty)
        cell_from_sql = pd.read_sql_query(yrquery, con)
        countyspace.set_value(
            int(yr), 'population', cell_from_sql.ix[0, 0])
    for yr in range(2001,2005,1):
        interp = countyspace.ix[2000, 'population']
        countyspace.set_value(
            int(yr), 'population', interp)
    for yr in range(2006,2010,1):
        interp = countyspace.ix[2005, 'population']
        countyspace.set_value(
            int(yr), 'population', interp)
    for yr in range(2011,2015,1):
        interp = countyspace.ix[2010, 'population']
        countyspace.set_value(
            int(yr), 'population', interp)

    pluspop = countyspace
    return pluspop
# Returns 'pluspop', the completed dataframe for the county

# Send to CSV and SQL


def Saveways(ctycode, fullcounty):
    namecsv = '{}{}{}'.format('CountyTables/', ctycode, '.csv')
    namesql = 'counties.' + ctycode
    fullcounty.to_csv(namecsv)
    fullcounty.to_sql(namesql, engine, if_exists='replace')


def main():
    # Input: county, state
    '''IMPORTANT: Need to include single-quotes when entering both!'''
    county = str(input("County name: "))
    state = str(input("State number: "))
    ctycode = county + state                            # Barnstable25, Bioclim
    ctycode0 = '{}{}{}'.format(county, '0', state)      # Barnstable025, Lyme
    lymebuild = BuildLyme(ctycode0)
    countybio = BioClim(ctycode, lymebuild, ctycode0)
    countyspace = LatLon(ctycode, countybio, ctycode0)
    pluspop = PopAdd(ctycode, countyspace, ctycode0)
    fullcounty = pluspop
    Saveways(ctycode, fullcounty)

main()
