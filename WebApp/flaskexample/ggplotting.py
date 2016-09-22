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
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import file_html


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
    fig = plt.figure(figsize=(5,4),dpi=100)
    axes = fig.add_subplot(1,1,1)
    # plot the data
    axes.plot(thiscounty.Year,thiscounty.lymecases,'-')
    # labels
    axes.set_xlabel('Year')
    axes.set_ylabel('# of Lyme Cases')
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

    '''Bokeh plotting'''
    #plot = figure ()
    #plot.circle([1,2], [3,4])

    #html = file_html(plot, CDN, "my plot")

    #with open('flaskexample/circlebokeh.html', 'w') as file_:
    #    file_.write(html)

    #return html
