import pandas as pd
import numpy as np
import sys
import os

sys.path.append('./Web')
from dataclean import dataclean
# end dat got from yesterday
df = dataclean()
dE = pd.Timestamp.today()

# get the informs of when is the last update
update_day = dE.strftime('%Y-%m-%d')

### compare average price of thiw week vs. last week
dS = dE - pd.DateOffset(days=7)
dS1 = dE - pd.DateOffset(days=15)

# get this week dataframe
dat = df[(df['Date'] < dE )& (df['Date'] >= dS)].groupby(['全名']).mean()

# join and rename with last week dataframe
dat = dat.join(df[(df['Date'] < dS )& (df['Date'] >= dS1)].groupby(['全名']).mean().rename(columns=lambda x: x.__add__('_wb')))

# select high volume vegetables
dat[(dat["成交量(公斤)"] > 1e3)&(dat["成交量(公斤)_wb"] > 1e3)]

# make crucial indicators
dat["price_diff"] = dat["平均價(元/公斤)"] - dat["平均價(元/公斤)_wb"]
dat["return_rate"] = (dat["平均價(元/公斤)"] - dat["平均價(元/公斤)_wb"])/dat["平均價(元/公斤)_wb"]

# drop uncomparable rows
dat =  dat.dropna()
loser = dat.sort_values(by=['return_rate'], ascending=True)
gainer = dat.sort_values(by=['return_rate'], ascending=False)



loser_list = []
gainer_list = []
general_list = []
for i in range(len(dat)):
    loser_list.append([loser.index.values[i], np.round(loser["price_diff"][i],2) ,f'{np.round(loser["return_rate"][i]*100,2)}%'])
    gainer_list.append([gainer.index.values[i], np.round(gainer["price_diff"][i],2) ,f'{np.round(gainer["return_rate"][i]*100,2)}%'])
    general_list.append([dat.index.values[i], np.round(dat["price_diff"][i],2) ,f'{np.round(dat["return_rate"][i]*100,2)}%'])

topgainer_list = []
toploser_list = []

# list 9 elements to show at front page 
for i in range(9):
    topgainer_list.append([gainer.index.values[i], f'{np.round(gainer["return_rate"][i]*100,2)}%'])
    toploser_list.append([loser.index.values[i], f'{np.round(loser["return_rate"][i]*100,2)}%'])



## TY1W
dn_lasty = dE - pd.DateOffset(days=358)
ds_lasty = dE - pd.DateOffset(days=372)

# get this week dataframe
dat_TY1W = df[(df['Date'] <= dE) & (df['Date'] >= dS)].groupby(['全名']).mean()

# join and rename with last week dataframe
dat_TY1W = dat_TY1W.join(df[(df['Date'] <= dn_lasty )& (df['Date'] >= ds_lasty)].groupby(['全名']).mean().rename(columns=lambda x: x.__add__('_yb')))

# select high volume vegetables
dat_TY1W[(dat_TY1W["成交量(公斤)"] > 1e3)&(dat_TY1W["成交量(公斤)_yb"] > 1e3)]

# make crucial indicators
dat_TY1W["price_diff"] = dat_TY1W["平均價(元/公斤)"] - dat_TY1W["平均價(元/公斤)_yb"]
dat_TY1W["return_rate"] = (dat_TY1W["平均價(元/公斤)"] - dat_TY1W["平均價(元/公斤)_yb"])/dat_TY1W["平均價(元/公斤)_yb"]



yloser = dat_TY1W.dropna().sort_values(by = ["return_rate"], ascending=True)
ygainer= dat_TY1W.dropna().sort_values(by = ["return_rate"], ascending=False)

yloser_list = []
ygainer_list = []
ygeneral_list = []
for i in range(len(yloser)):
    yloser_list.append([yloser.index.values[i], np.round(yloser["price_diff"][i],2), f'{np.round(yloser["return_rate"][i]*100,2)}%'])
    ygainer_list.append([ygainer.index.values[i], np.round(ygainer["price_diff"][i],2), f'{np.round(ygainer["return_rate"][i]*100,2)}%'])
    ygeneral_list.append([dat_TY1W.index.values[i], np.round(dat_TY1W["price_diff"][i],2), f'{np.round(dat_TY1W["return_rate"][i]*100,2)}%'])

ytopgainer_list = []
ytoploser_list = []
# list 9 elements to show at front page 
for i in range(9):
    ytopgainer_list.append([ygainer.index.values[i], f'{np.round(ygainer["return_rate"][i]*100,2)}%'])
    ytoploser_list.append([yloser.index.values[i], f'{np.round(yloser["return_rate"][i]*100,2)}%'])
