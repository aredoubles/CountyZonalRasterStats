import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
from path import path

dbname = 'lymeforecast'
username = 'rogershaw'
engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

con = None
con = psycopg2.connect(database=dbname, user=username)

def TableNames(band, year):
    band = str(band)
    year = str(year)
    bandit = 'bio' + band       #Bio6, Bioclim
    if len(band) = 1:
        band0 = 'bio0' + band   #Bio06, ?
    else: band0 = bandit        #Bio12, Bioclim

    # "bio2.bio2-2008", band-year tables
    # "mean-bio8-04", indiv. table values

    targettable = '{}{}{}{}{}{}{}'.format('"', bandit, '.', bandit, '-', year, '"')
    biocol = '{}{}{}{}{}'.format('"mean-', bandit, '-', yr[-2:], '"')

# Add Lyme Data
def BuildLyme(ctycode0):
    lyme_data = pd.read_csv('lyme_CtyID.csv', index_col='CtyID')
    # Subset to just the Years columns
    lyme_data = lyme_data[[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]]
    # Rename columns (will later become rows in county table)
    lyme_data.loc['YrCol'] = range(2000,2015,1)
    yrcol = lyme_data.iloc[-1]
    lyme_data = lyme_data[:-1]
    lyme_data = lyme_data.rename(columns=yrcol)
    # Query the county we're working with
    thislyme = lyme_data.ix[ctycode0]
    thislyme = thislyme.ix[5:]     # Row vector, cases in each year
    lymebuild = pd.DataFrame(thislyme)
    lymebuild.rename(columns={ctycode0 : 'lymecases'}, inplace=True)
    lymebuild['county'] = ctycode0
    return lymebuild
# Returns 'lymebuild', a dataframe of years x Lyme, county-code

# Add lat/lon
def LatLon (ctycode, lymebuild):      # ctycode = Bioclim, has lat/lon
    yrs = range(2000,2017,1)
    #thiscounty['county'] = ctycode
    latlonquery = {}{}{}{}.format('''SELECT "Lat", "Lon" FROM "bio1.bio1-2000" WHERE "CtyID" = ''', "'", ctycode, "'")
    latlonsql = pd.read_sql_query(latlonquery, con)
    lymebuild['lat'] = latlonsql['Lat'][0]
    lymebuild['lon'] = latlonsql['Lon'][0]
    countychar = lymebuild
    return countychar
# Returns 'countychar', a dataframe that also includes lat/lon

# Add Bioclim data
def BioClim(ctycode, countychar):
    for band in range(1,19,1):
        band0 = '{}{}{}'.format('bio', str(0), band)
        band = 'bio' + str(band)
        for yr in range(2000, 2016, 1):
            # Get all these variables names set
            yr = str(yr)
            #yrvar = '{}{}{}'.format('"mean-bio8-', yr[-2:], '"')
            yrvar = '{}{}{}{}{}'.format('"mean-', band, '-', yr[-2:], '"')
            #yrtab = '{}{}{}'.format('"bio8.bio8-20', yr[-2:], '"')
            yrtab = '{}{}{}{}{}{}{}'.format('"', band, '.', band, '-20', yr[-2:], '"')
            ctystrquo = '{}{}{}'.format("'", ctycode, "'")
            sql_query = '{} {} {} {} {} {}'.format('SELECT', yrvar, 'FROM', yrtab,
                                                'WHERE "CtyID" =', ctystrquo)
            cell_from_sql = pd.read_sql_query(sql_query, con)
            countychar.set_value(int(yr),band0,cell_from_sql.ix[0, yrvar[1:-1]])
    #countychar.set_value(2015,'Year2',2015)
    countychar.set_value(2015,'County',ctycode)
    fullcounty = countychar
    return fullcounty
# returns 'fullcounty', a complete dataframe for a single county

# Send to CSV and SQL
def Saveways(ctycode, fullcounty):
    namecsv = ctycode + '.csv'
    namesql = 'counties.' + ctycode
    barnstable.to_csv(namecsv)
    barnstable.to_sql(namesql, engine, if_exists='replace')

'''
Append to grand table, save to CSV and SQL
'''

def main():
    # Input: county, state
    county = str(input("County name: "))
    state = str(input("State number: "))
    ctycode = county + state                            # Barnstable25, Bioclim
    ctycode0 = '{}{}{}'.format(county, '0', state)      # Barnstable025, Lyme
    lymebuild = BuildLyme(ctycode0)
    countychar = LatLon(ctycode, lymebuild)
    fullcounty = BioClim(ctycode, countychar)
    Saveways(ctycode, fullcounty)

    '''
    Need to add other functions here, as part of main!
    '''

main()
