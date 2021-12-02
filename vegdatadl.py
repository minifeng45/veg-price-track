import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class vegdatadl:

    def __init__(self, market_name):
        self.market_name = market_name

    def date_scrape(self, selected_date, driver):
        ### Opens a tab of the single market page
        import time
        # 不論使用者找出 chromedriver 路徑
        ## control google chrome
        url = 'http://www.tapmc.com.taipei/Pages/Trans/Price1'
        driver.get(url=url)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="DDL_FV_Code"]').click() # choose vegetable/fruit 
        time.sleep(1)

        if self.market_name == 'all_market':
            driver.find_element_by_xpath('//*[@id="DDL_Category"]').click() # choose single market
            driver.find_element_by_xpath('//*[@id="DDL_Category"]/option[1]').click()

        if self.market_name == 'single_first_market':
            driver.find_element_by_xpath('//*[@id="DDL_Category"]').click() # choose single market
            driver.find_element_by_xpath('//*[@id="DDL_Category"]/option[2]').click() 
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="DDL_Market"]').click() # choose the first market
            driver.find_element_by_xpath('//*[@id="DDL_Market"]/option[1]').click()

        if self.market_name == 'single_second_market':
            driver.find_element_by_xpath('//*[@id="DDL_Category"]').click() # choose single market
            driver.find_element_by_xpath('//*[@id="DDL_Category"]/option[2]').click() 
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="DDL_Market"]').click() # choose the first market
            driver.find_element_by_xpath('//*[@id="DDL_Market"]/option[2]').click()


        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.keys import Keys

        date_box = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_txtDate"]') # 選日期框框
        date_box.clear() # 清除內容
        date_box.send_keys(selected_date) # 填入日期
        date_box.send_keys(Keys.ENTER) # 送出日期
        driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnQuery"]').click() # submit 查詢
        # time.sleep(3)
        try:
            WebDriverWait(driver, 0.3).until(EC.alert_is_present(),
                'Timed out waiting for PA creation ' +
                'confirmation popup to appear.')
            alert = driver.switch_to.alert
            alert.accept()
            print("No data today. Alert accepted")
        except TimeoutException:
            import pandas as pd
            import numpy as np
            import pandas as pd
            df = pd.read_html(driver.page_source)[0] # scrape table
            df.columns = df.columns.droplevel(0) # drop multilevel columns
            df.drop([len(df)-1], inplace = True) # drop misread total
            df.drop([df.columns[-1]], axis=1, inplace=True) # drop last unnamed column
            df['日期'] = selected_date
            return df

    def delete_table(self,selected_date):
        import sqlite3 as lite
        import os 
        db_dir = os.getcwd()
        try:
            conn = lite.connect(os.path.join(db_dir,f'{self.market_name}_vegtrack.db'))
            cur = conn.cursor()
            cur.execute(f'DROP TABLE IF EXISTS "{selected_date}"')
            print(f'Table {selected_date} has been drop')
        except IndentationError: 
            print('terminal in wrong directory')


    def df2sql(self, df, selected_date):
        import sqlite3 as lite
        import os 
        db_dir = os.getcwd()
        
        try:
            conn = lite.connect(os.path.join(db_dir,f'{self.market_name}_vegtrack.db'))
            
        except IndentationError:
            print('terminal in wrong directory')
        try:
            df.to_sql(selected_date, conn)
            print(f'Table "{selected_date}" insertion succeed' )
        except:
            try:
                df.to_sql(selected_date, conn, if_exists= 'replace')
                print(f'Table "{selected_date}" already exists and replace by new input' )
            except AttributeError:
                pass
    
    def sql2df(self, selected_date):
        import sqlite3 as lite
        import pandas as pd 
        import os 
        import numpy as np 
        db_dir = os.getcwd()
        try:
            conn = lite.connect(os.path.join(db_dir,f'{self.market_name}_vegtrack.db'))
            df = pd.read_sql_query(f'SELECT * FROM "{selected_date}"', conn)
            # data cleaning
            # Clean up the data
            # Replace nan in variety
            df['品種'] = df['品種'].replace(np.nan, '單一品種')
            df['品名'] = df['品名'].replace('蕃茄','番茄')
            # Convert messy date into datetime object
            df[['Year','date_']] = df['日期'].astype('str').str.split('/', n=1, expand=True)
            df['Year'] = df['Year'].astype('int') + 1911
            df['Date'] = (df['Year'].astype('str') +'/'+ df['date_']).astype('datetime64[ns]')
            df.drop(columns=['日期', 'Year', 'date_'], inplace = True)
            # Make a dict for getting whole name from code
            df['全名'] = df['品名'] + "(" + df['品種'] + ")"

        except IndentationError:
            print('terminal in wrong directory')

        return df

    def date2ROC(self,period, ending_date = None):
        '''
        Transfer a period of time from AD to ROC
        '''
        import datetime
        if ending_date == None: # if there is no input starting date then its today
            end = datetime.datetime.today()
        else:
            end = datetime.datetime.strptime(ending_date, '%Y/%m/%d') # make it in to datetime object
        
        start = (end - datetime.timedelta(days=period)).strftime("%Y/%m/%d") # make it in to datetime object
        days = (end - start).days # calculate delta
        date_list = [(end - datetime.timedelta(days=x)).strftime("%Y/%m/%d") for x in range(days)] # generate date list for iterating download
        date_list_ROC = [str(int(x[0:4])-1911) + x[4:] for x in date_list]
        return date_list_ROC


