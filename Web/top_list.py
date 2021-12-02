import pandas as pd
import numpy as np
import sys
import os

sys.path.append('./Web')
import dataclean
# end dat got from yesterday
df = dataclean.dataclean()
dE = pd.Timestamp.today()
update_day = dE.strftime('%Y-%m-%d')
dS = dE - pd.DateOffset(days=7)
dS1 = dE - pd.DateOffset(days=15)


dWn = df[df['Date'] < dE][df['Date'] >= dS].groupby(['全名']).mean()
dWl = df[df['Date'] < dS][df['Date'] >= dS1].groupby(['全名']).mean()
import matplotlib.pyplot as plt
dWn = dWn[dWn["成交量(公斤)"] > 1e3]
dWl = dWl[dWl["成交量(公斤)"] > 1e3]


def return_rate(new, old):
    return (new - old)/old
dat = return_rate(dWn["平均價(元/公斤)"],dWl["平均價(元/公斤)"])

dat =  dat.dropna()
loser = dat.sort_values(ascending=True)*100 
gainer= dat.sort_values(ascending=False)*100 

loser_list = []
gainer_list = []
general_list = []
for i in range(len(dat)):
    loser_list.append([loser.index.values[i], f'{np.round(loser.values[i])}%'])
    gainer_list.append([gainer.index.values[i], f'{np.round(gainer.values[i])}%'])
    general_list.append([dat.index.values[i], f'{np.round(dat.values[i]*100)}%'])

topgainer_list = []
toploser_list = []

# list 9 elements to show at front page 
for i in range(9):
    topgainer_list.append([gainer.iloc[:].index.values[i],f'{(np.round(gainer.values,1)[i])}%'])
    toploser_list.append([loser.iloc[:].index.values[i], f'{(np.round(loser.values,1)[i])}%'])



## TY1W
dn_lasty = dE - pd.DateOffset(days=358)
ds_lasty = dE - pd.DateOffset(days=372)

d_lasty = df[df['Date'] <= dn_lasty][df['Date'] >= ds_lasty].groupby(['全名']).mean()
dWn = df[df['Date'] <= dE][df['Date'] >= dS].groupby(['全名']).mean()

ty1w = return_rate(dWn["平均價(元/公斤)"],d_lasty["平均價(元/公斤)"])

yloser = ty1w.dropna().sort_values(ascending=True)*100 
ygainer= ty1w.dropna().sort_values(ascending=False)*100 

yloser_list = []
ygainer_list = []
for i in range(len(yloser)):
    yloser_list.append([yloser.index.values[i], f'{np.round(yloser.values[i])}%'])
    ygainer_list.append([ygainer.index.values[i], f'{np.round(ygainer.values[i])}%'])

ytopgainer_list = []
ytoploser_list = []

# list 9 elements to show at front page 
for i in range(9):
    ytopgainer_list.append([ygainer.iloc[:].index.values[i],f'{(np.round(ygainer.values,1)[i])}%'])
    ytoploser_list.append([yloser.iloc[:].index.values[i], f'{(np.round(yloser.values,1)[i])}%'])