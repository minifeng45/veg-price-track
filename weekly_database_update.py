#### update the website at Saturday morning or monday night
import vegdatadl as vl
from selenium import webdriver
from tqdm import tqdm
import os 
import sqlite3 as lite
import pandas as pd 
import numpy as np

def date2ROC(period, ending_date = None):
    '''
    Transfer a period of time from AD to ROC
    '''
    import datetime
    if ending_date == None: # if there is no input starting date then its today
        end = datetime.datetime.today()
    else:
        end = datetime.datetime.strptime(ending_date, '%Y/%m/%d') # make it in to datetime object
    
    start = (end - datetime.timedelta(days=period)) # make it in to datetime object
    days = (end - start).days # calculate delta
    date_list = [(end - datetime.timedelta(days=x)).strftime("%Y/%m/%d") for x in range(days)] # generate date list for iterating download
    date_list_ROC = [str(int(x[0:4])-1911) + x[4:] for x in date_list]
    return date_list_ROC

date_list_ROC = date2ROC(14)

## control google chrome
driver = webdriver.Chrome(executable_path= os.path.join(os.getcwd(),'chromedriver')) # set path to your directory which contains chromedriver
conn = lite.connect(os.path.join(os.getcwd(),'Web',"bulk_database.db"))


df_new = pd.DataFrame()
for day in tqdm(date_list_ROC):
    try:
        fc = vl.vegdatadl('single_first_market')
        raw_df = fc.date_scrape(day,driver)
        raw_df['品種'] = raw_df['品種'].replace(np.nan, '單一品種')
        raw_df['品名'] = raw_df['品名'].replace('蕃茄','番茄')
        # Convert messy date into datetime object
        raw_df[['Year','date_']] = raw_df['日期'].astype('str').str.split('/', n=1, expand=True)
        raw_df['Year'] = raw_df['Year'].astype('int') + 1911
        raw_df['Date'] = (raw_df['Year'].astype('str') +'/'+ raw_df['date_']).astype('datetime64[ns]')
        raw_df.drop(columns=['日期', 'Year', 'date_'], inplace = True)
        # Make a dict for getting whole name from code
        raw_df['全名'] = raw_df['品名'] + "(" + raw_df['品種'] + ")"
        df_new = df_new.append(raw_df)

    except TypeError: 
        pass
# drop duplicate rows
df_new.to_sql('single_first_market', conn, index = False, if_exists= "append")

df = pd.read_sql_query(f'SELECT Date,全名, 品名代號,"平均價(元/公斤)","成交量(公斤)" FROM single_first_market WHERE date(Date) > date("now","-5 years")', conn)
df = df.drop_duplicates()
df = df[df['全名'] != "其他(單一品種)"]
df.to_sql('single_first_market', conn, index = False, if_exists= "replace")