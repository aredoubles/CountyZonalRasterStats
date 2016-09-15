from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.schema import CreateSchema
import psycopg2
import pandas as pd
from path import path

dbname = 'lymeforecast'
username = 'rogershaw'
engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))
print engine.url

if not database_exists(engine.url):
    create_database(engine.url)
    print(database_exists(engine.url))

con = None
con = psycopg2.connect(database=dbname, user=username)

# Get the Lyme data in first
# Lyme/ld-case-counts-by-county-00-14.csv
lyme_data = pd.read_csv('Lyme/ld-case-counts-by-county-00-14.csv')
# Make a 'CtyID' column similar to the Bioclim IDs
# First, convert state codes into strings, for later concatenation
strngr = lambda x: str(x)
lyme_data['Stcode'] = list(map(strngr, lyme_data['Stcode']))
zdig = lambda x: '0' + x
for stc in lyme_data['Stcode']:
    if len(stc) < 2:
        lyme_data['Stcode'] = list(map(zdig, lyme_data['Stcode']))
        #lyme_data['Stcode'] = list(map(zdig, lyme_data['Stcode']))
# Now can finally crate CountyID column!
lyme_data['CtyID'] = lyme_data['Ctyname'] + lyme_data['Stcode']
lyme_data.to_sql('lyme_data_table', engine, if_exists='replace')

lyme_data.to_csv('lyme_CtyID.csv')

# Should create a Cty_ID column similar to the Bioclim files
# CtyID = Lancaster31

# Get all/some Bioclim tables in Postgres too
# Setup schema, one for each band/var (ex: Bio1)
for x in range(1, 15, 1):
    band = 'bio' + str(x)
    engine.execute(CreateSchema(band))

# Get all/some Bioclim tables into their respective schema
# Work on Bio01 first

bpath = path('Clim/FlatBioclim/Bio01')
for f in bpath.files(pattern='*.csv'):
    yrbio = pd.read_csv(f)
    # Rename the 'mean' column to: mean-bio2-08
    mncol = 'mean-bio1-' + str(f[-6:-4])
    yrbio.rename(columns={'Mean': mncol}, inplace=True)
    # Generate a name for the table, including schema
    # schemaname.tablename => bio2-2008
    tbnm = '{}{}{}'.format('bio1.', 'bio1-', f[-8:-4])
    yrbio.to_sql(tbnm, engine, if_exists='replace')

'''
Now want to use Inner Joins to create a master table for each year/band
Could pull columns from SQL,
But do most of the joining here in Python?
Start with Barnstable25
'''
barnstable25 = lyme_data[lyme_data['CtyID'] == 'Barnstable025']

barnstable = pd.DataFrame(barnstable25)
# How did I remove the extraneous columns?
barnstable = barnstable.ix[:, 4:-1]
barnstable['variable'] = 'LymeCases'

barnstable = barnstable.set_index('variable')
barnstable.columns = range(2000, 2015, 1)

for yrcol in range(2000, 2015, 1):
    barnstable.set_value('Bio01', yrcol, 20)

barnstable.to_csv('barnstable.csv')

for yr in range(2000, 2015, 1):
    # Get all these variables names set
    yr = str(yr)
    yrvar = '{}{}{}'.format('"mean-bio1-', yr[-2:], '"')
    yrtab = '{}{}{}'.format('"bio1.bio1-20', yr[-2:], '"')

    sql_query = '{} {} {} {} {}'.format('SELECT', yrvar, 'FROM', yrtab,
                                        '''WHERE "CtyID" LIKE 'Barnstable%' ''')

    cell_from_sql = pd.read_sql_query(sql_query, con)

    barnstable.set_value('Bio01', int(yr), cell_from_sql.ix[0, yrvar[1:-1]])
