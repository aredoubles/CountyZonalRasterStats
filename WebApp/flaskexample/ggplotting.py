def PlotIt(countyid, countyname, the_result):
    #%matplotlib inline
    #import ggplot
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import seaborn as sns
    import tempfile
    import matplotlib
    matplotlib.use('Agg') # this allows PNG plotting
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-white')


    dbname = 'lymeforecast'
    username = 'rogershaw'
    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    con = None
    con = psycopg2.connect(database=dbname, user=username)


    quoter = '{}{}{}'.format("'", countyid, "'")
    countyfind = '''SELECT "Year", lymecases FROM grandtable WHERE county = ''' + quoter
    thiscounty = pd.read_sql_query(countyfind, con)

    rfpredict = the_result     # Obviously change this to the model prediction
    thiscounty.set_value(15, 'lymecases', rfpredict)

    #thiscounty = thiscounty.set_index(thiscounty.Year)
    #cplot = sns.tsplot([thiscounty.lymecases])
    #cplot.savefig('cplot.png')


    #cplot = ggplot(thiscounty, aes(x='Year', y='lymecases')) + geom_line(size=2) + \
    #    theme_bw() + labs(x='Year', y='# of Lyme Disease cases', title=countyid)
    #ggsave(plot = cplot, filename = 'cplot.png')

    '''Plotting'''
    # generate matplotlib plot
    fig = plt.figure(figsize=(7,5),dpi=100)
    axes = fig.add_subplot(1,1,1)
    # plot the data
    axes.plot(thiscounty.Year,thiscounty.lymecases,'-')
    # labels
    axes.set_xlabel('Year')
    axes.set_ylabel('# of Lyme Cases')
    plt.xlim(2000,2016)
    plt.ylim(50,350)
    axes.set_title(countyname)
    # make the temporary file
    f = tempfile.NamedTemporaryFile(dir='flaskexample/static/temp', suffix='.png',delete=False)
    # save the figure to the temporary file
    #f = 'flaskexample/static/cplot.png'
    '''plt.savefig(f)'''
    '''f.close() # close the file'''
    # get the file's name (rather than the whole path)
    # (the template will need that)
    plotPng = f.name.split('/')[-1]
    #plotPng = f
    return plotPng

    '''Bokeh plotting'''
    #plot = figure ()
    #plot.circle([1,2], [3,4])

    #html = file_html(plot, CDN, "my plot")

    #with open('flaskexample/circlebokeh.html', 'w') as file_:
    #    file_.write(html)

    #return html

def OverPlot(countyid, countyname, the_result):
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import seaborn as sns
    import tempfile
    import matplotlib
    matplotlib.use('Agg') # this allows PNG plotting
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-white')


    dbname = 'lymeforecast'
    username = 'rogershaw'
    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    con = None
    con = psycopg2.connect(database=dbname, user=username)


    quoter = '{}{}{}'.format("'", countyid, "'")
    countyfind = '''SELECT "Year", lymecases FROM grandtable WHERE county = ''' + quoter
    thiscounty = pd.read_sql_query(countyfind, con)
    thiscounty = thiscounty.ix[0:14]


    rfpredict = pd.DataFrame(the_result)
    #thiscounty.set_value(15, 'lymecases', rfpredict[0])
    rfpredict['Year'] = (2015,2016)
    rfpredict.ix[2] = (thiscounty.ix[14][1],2014)
    rfpredict = rfpredict.sort_values(by='Year')


    '''Plotting'''
    # generate matplotlib plot
    fig = plt.figure(figsize=(7,5),dpi=100)
    axes = fig.add_subplot(1,1,1)
    # plot the data
    axes.plot(thiscounty.Year,thiscounty.lymecases, linestyle='solid', color='steelblue', linewidth=2.5)
    axes.plot(rfpredict.Year,rfpredict.lymecasespred, linestyle='solid', color='darkorange', linewidth=2.5)
    # labels
    axes.set_xlabel('Year')
    axes.set_ylabel('# of Lyme Cases')
    plt.xlim(2000,2017)
    #plt.ylim(50,350)
    axes.set_title(countyname)
    # make the temporary file
    f = tempfile.NamedTemporaryFile(dir='flaskexample/static/temp', suffix='.png',delete=False)
    # save the figure to the temporary file
    #f = 'flaskexample/static/cplot.png'
    plt.savefig(f)
    f.close() # close the file
    # get the file's name (rather than the whole path)
    # (the template will need that)
    plotPng = f.name.split('/')[-1]
    #plotPng = f
    return plotPng
