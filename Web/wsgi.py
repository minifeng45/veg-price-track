from flask import Flask, render_template
# test the plotly on html
from top_list import gainer, loser, general_list, toploser_list, topgainer_list, loser_list, gainer_list, ygainer, yloser, ytoploser_list, ytopgainer_list, yloser_list, ygainer_list, update_day
from json import dumps, loads

import plotly
# local function
import make_plot as mp


# get the data from csv

app = Flask(__name__)
@app.route('/')
def index():
    gain = gainer
    lose = loser
    topgainer = topgainer_list
    toploser = toploser_list
    ygain = ygainer
    ylose = yloser
    ytopgainer = ytopgainer_list
    ytoploser = ytoploser_list
    update = update_day
    return render_template('frontpage.html', 
    topgainer = topgainer, toploser = toploser,
    gainer = gain, loser = lose,
    ytopgainer = ytopgainer, ytoploser = ytoploser,
    ygainer = ygain, yloser = ylose,
    update_day = update)


@app.route('/graphics/<name>')
def graphics(name):
    topgainer = topgainer_list
    toploser = toploser_list
    fig0 = mp.make_plot(veg_name = name, duration_code = 'a1w')
    p0 = dumps(fig0, cls=plotly.utils.PlotlyJSONEncoder)
    fig1 = mp.make_plot(veg_name = name, duration_code = 'b1m')
    p1 = dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = mp.make_plot(veg_name = name, duration_code = 'c3m')
    p2 = dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = mp.make_plot(veg_name = name, duration_code = 'd6m')
    p3 = dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    fig4 = mp.make_plot(veg_name = name, duration_code = 'e1y')
    p4 = dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    fig5 = mp.make_plot(veg_name = name, duration_code = 'g5y')
    p5 = dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    bar1 = mp.seasonality_price(veg_name = name)
    b1 = dumps(bar1 , cls=plotly.utils.PlotlyJSONEncoder)
    bar2 = mp.seasonality_volume(veg_name = name)
    b2 = dumps(bar2 , cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graphics.html',  
    topgainer = topgainer, 
    toploser = toploser, 
    name = name,
    plot0 = p0,plot1 = p1,plot2 = p2,plot3 =p3, plot4 =p4, plot5 =p5,
    barplot1 = b1,
    barplot2 = b2,
    )

@app.route('/allveg')
def allveg():
    loserlist = loser_list
    gainlist = gainer_list
    generallist = general_list
    update = update_day
    return render_template('allveg.html', loser_list = loserlist, gain_list = gainlist, general_list = generallist, update_day = update)

@app.route('/allveg_seasonality')
def allvegseasonality():
    yloserlist = yloser_list
    ygainlist = ygainer_list
    return render_template('allveg.html', yloser_list = yloserlist, ygain_list = ygainlist)

@app.route('/loadingpage')
def load():
    
    return render_template('loadingpage.html')

if __name__ == '__main__':
    app.run()
