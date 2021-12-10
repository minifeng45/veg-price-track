import pandas as pd
import sqlite3 as lite
import datetime
import sys
sys.path.append('./Web')
import dataclean
# end dat got from yesterday
df = dataclean.dataclean()
import datetime
def YTD_value(Sr, df_t):
    value = df_t[
        (df_t['Date'] < Sr['Date'] - datetime.timedelta(days=358))& 
        (df_t['Date'] > Sr['Date'] - datetime.timedelta(days=372))
        ]['平均價(元/公斤)'].mean()
    return value

def make_plot(veg_name, duration_code):

    import plotly.graph_objects as go
    # Convert duration code to days
    duration_to_date = {'a1w':7, 'b1m': 30, 'c3m': 90,'d6m': 180, 'e1y': 365, 'g5y': 1825 }
    import datetime
    end_date = datetime.datetime.today()
    duration = duration_to_date[duration_code]
    start_date = end_date - datetime.timedelta(duration)
    # Filter out specified veggitable
    mask = df['全名'] == veg_name
    df_single = df[mask]
    # Calculate Year to date value for each entry using YTD_value function
    df_single.loc[:,'YTD_value'] = df_single.apply(YTD_value, args=(df_single,),axis=1)

    # Count y axes range based on selected date
    df_filtered = df_single[(df_single['Date'] < end_date) & (df_single['Date'] > start_date)]
    if df_filtered['平均價(元/公斤)'].max() > df_filtered['YTD_value'].max():
        max = df_filtered['平均價(元/公斤)'].max()
    else:
        max = df_filtered['YTD_value'].max()
    if df_filtered['平均價(元/公斤)'].min() < df_filtered['YTD_value'].min():
        min = df_filtered['平均價(元/公斤)'].min()
    else:
        min = df_filtered['YTD_value'].min()
    margin = (max - min) * 0.2

    # Make graph
    fig = go.Figure(go.Scatter(
        x = df_single['Date'],
        y = df_single['平均價(元/公斤)'],
        line_color='#335333',
        name='平均批發價格',
        showlegend=True
    ))

    fig.add_traces(go.Scatter(
        x = df_single['Date'],
        y = df_single['YTD_value'],
        showlegend=True,
        name='去年當天前後一週平均線',
        mode='lines',
        line=go.scatter.Line(color="lightblue")
    ))
   
    fig.add_traces(go.Scatter(
        x= [df_single['Date'].max()], 
        y= [df_single['平均價(元/公斤)'].iloc[0]],
        mode='markers',
        showlegend=False,
        marker=dict(
            color='red',
            size=5
        )
    ))

    fig.update_layout(
        xaxis_tickformat = '%d %b %Y',
        legend = dict(yanchor = 'top',
        y = 1.3,
        xanchor = 'left',
        x = 0.01),
        template = 'simple_white',
        margin=dict(r=50)
    )
    
    # Update X and Y zoom
    fig.update_xaxes(type="date", range=[start_date, end_date])
    fig.update_yaxes(range=[min-margin, max+margin])
    fig.layout.autosize = True
    return fig

    
def seasonality_price(veg_name):
    import plotly.graph_objects as go
    df_s = df[df['全名']==veg_name] # 篩出要的蔬菜
    df_s.loc[:,'Month'] = pd.DatetimeIndex(df_s['Date']).month # 把月份獨立出來
    df_M = df_s.groupby('Month').mean().reset_index() # 做月平均
    df_M['Seasonality']=(df_M['平均價(元/公斤)']/df_M['平均價(元/公斤)'].mean() -1 )*100 # 計算季節波動
    
    fig = go.Figure(go.Bar(
        x= df_M['Month'],
        y= df_M['Seasonality'],
        marker={'color': '#141044'},
        showlegend = False
    ))
    
    fig.update_layout(
        template = 'simple_white',
        xaxis_title="月份",
        yaxis_title="當月價格比年均價(%)",
        xaxis = dict(
        tickmode = 'linear',
        dtick = 1),
        margin=dict(r=50)
    )

    return fig

def seasonality_volume(veg_name):
    import plotly.graph_objects as go
    df_s = df[df['全名']==veg_name] # 篩出要的蔬菜
    df_s.loc[:,'Month'] = pd.DatetimeIndex(df_s['Date']).month # 把月份獨立出來
    df_M = df_s.groupby('Month').mean().reset_index() # 做月平均
    df_M['Seasonality']=(df_M['成交量(公斤)']/df_M['成交量(公斤)'].mean() -1) *100 # 計算季節波動
    fig = go.Figure(go.Bar(
        x= df_M['Month'],
        y= df_M['Seasonality'],
        marker={'color': '#141044'},
        showlegend = False,
    ))
    fig.update_layout(
        template = 'simple_white',
        xaxis_title="月份",
        yaxis_title="當月交易量比年均交易量(%)",
        xaxis = dict(
            tickmode = 'linear',
            dtick = 1),
            margin=dict(r=50)
        )

    return fig