def dataclean():
    import pandas as pd
    import sqlite3 as lite
    conn = lite.connect('bulk_database.db')
    # select the recent 5-year data

    df = pd.read_sql_query(f'SELECT Date,全名,品名代號,"平均價(元/公斤)","成交量(公斤)" FROM single_first_market WHERE date(Date) > date("now","-5 years")', conn)
    # drop duplicate rows
    df = df.drop_duplicates()
    df = df[df['全名'] != "其他(單一品種)"]
    df['全名'] = df['全名'].replace('洋菇(盒)(盒裝)','洋菇-盒裝').str.rstrip('(單一品種)')
    df['全名'] = df['全名'].str.replace("(",'-',regex=True).str.replace('-其他','',regex=True).str.replace('其他菇類菇類','其他菇類',regex=True)
    # make price as float 
    df['平均價(元/公斤)'] = df['平均價(元/公斤)'].astype(float)
    df['成交量(公斤)'] = df['成交量(公斤)'].astype(float)
    # set date as datetime
    df['Date'] = df['Date'].astype('datetime64[ns]')
    df  = df.sort_values('Date',ascending=False).reset_index().drop("index",axis=1)
    return df