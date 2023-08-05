#from stock_scraper import StockScraper
from .stock_scraper import getSnpCompanies,getStockContent,getNewsHeadlines
from .data_base import SqlDB
import pandas as pd
from .Sentiment_analysis import sentimentAnalysis

#configuing stockscraper because it is a class
#config_stock = StockScraper()
config_sql = SqlDB()



def tableExitsCheck(table_exists:bool, table_name:str):
        if table_exists == False:
            raise ValueError('Data table doesnt exist... Creating one')
        else:
            print("Database exists")    
            retrieve_table = config_sql.retriveTableInfo(table_name=table_name)

        return retrieve_table

def createDataTable(table_name:str, dt_contents):
        create_table = config_sql.createTable(table_name=table_name, dt_contents=dt_contents)
        retrieve_table = config_sql.retriveTableInfo(table_name=table_name)
        print("Data table:",table_name, "Has been created")

def updateStockInfo(updateFlag:bool, retrieve_table):
        if updateFlag == True:
            stock_list = getSnpCompanies()
            content = getStockContent(tickers=stock_list)
        else:
            stock_list = retrieve_table['ticker']
            content = getStockContent(tickers=stock_list)    
        return content
def pushData(source_dt,new_dt,table_name):
        fresh_dt = config_sql.getNewRows(source_dt=source_dt, new_dt=new_dt)
        config_sql.appendData(table_name=table_name, dt_contents=fresh_dt) 


def stockData(stockContent_name:str ,updateFlag:bool):
    '''
    This function is used to perform stock data activities

    The purpose of this function is to create a stock info database, 
    retrieve the snp 500 companies from wikipedia, get
    the stock name, stock industry stock sector,stock type
    stock region, stock_info for each stock, and populate 
    the database with that data

    Args:
        stockContent_name: The name of the database for the stock contents

        updateFlag: A flag to be used if updating stock content is required or not
    '''
    print("Starting stock details extraction")
    stock_col = ['ticker','stock_name','stock_sector','stock_type','stock_region','stock_info']
    df = pd.DataFrame(columns=stock_col)
    content = df
    table_exists = config_sql.tableExists(table_name=stockContent_name)

    try: 
        tableExitsCheck(table_exists=table_exists, table_name=stockContent_name)
        retrieve_table = config_sql.retriveTableInfo(table_name=stockContent_name)

    except ValueError as e:
        print(e)
        createDataTable(table_name=stockContent_name, dt_contents=content)
        retrieve_table = config_sql.retriveTableInfo(table_name=stockContent_name)

    finally:
        content = updateStockInfo(updateFlag=updateFlag, retrieve_table=retrieve_table)
        pushData(source_dt=retrieve_table, new_dt=content, table_name=stockContent_name)
        # new_dt = config_sql.getNewRows(source_dt=retrieve_table, new_dt=content)
        # config_sql.appendData(table_name=stockContent_name, dt_contents=new_dt)       
    print("Stock details extraction complete")


def stockHeadlineData(stockInfoDatatable_name:str,updateFlag:bool,headlineDatatable_name:str):
        '''
        This function is used to retrieve headlines about the stock 

        The purpose of this function is create a database for headlines, 
        use the stock info database to retrieve headlines about the stock,
        and populate the headlines database

        Args:
            stockInfoDatatable_name: The stock info database name. This gets used to retrieve headlines

            updateFlag: A flag to be used if updating stock content is required or not

            headlineDatatable_name: The stock headline database name 
        '''
        print("Starting headlines extraction")
        config_sql = SqlDB()
        headline_col = ['ticker', 'headline', 'date']
 
        headline_tableExists = config_sql.tableExists(table_name=headlineDatatable_name)
        try:
            tableExitsCheck(table_exists=headline_tableExists, table_name=headlineDatatable_name)
            retrieve_table = config_sql.retriveTableInfo(table_name=headlineDatatable_name)
        except ValueError as e:
            print(e)
            df = pd.DataFrame(columns=headline_col)

            createDataTable(table_name=headlineDatatable_name, dt_contents=df)
            retrieve_table = config_sql.retriveTableInfo(table_name=headlineDatatable_name)

        finally:
            if updateFlag == True:
                
                retrieve_headline_table = config_sql.retriveTableInfo(table_name=headlineDatatable_name)
                retrieve_stock_info = config_sql.retriveTableInfo(table_name=stockInfoDatatable_name)
                dt_tickers = retrieve_stock_info['ticker'].tolist()
                new_dt= getNewsHeadlines(dt_tickers)
                original_dt = retrieve_headline_table

            else:
                retrieve_headline_table = config_sql.retriveTableInfo(table_name=headlineDatatable_name)
                new_dt = retrieve_headline_table
                original_dt = retrieve_headline_table
            append_dt = config_sql.getNewRows(source_dt=original_dt, new_dt=new_dt)

            config_sql.appendData(table_name=headlineDatatable_name, dt_contents=append_dt)
        print("Headlines extraction complete")

#stockHeadlineData(stockInfoDatatable_name = 'stock_content', updateFlag=True, headlineDatatable_name='stock_headlines')

def sentimentData(sentimentDatatable_name:str ,updateFlag:bool, headlineDatatable_name:str):
    '''
    This function is used to perform sentiment analysis activities

    The purpose of this function is to create a sentiment datatbale, 
    use the headlines from the headline datatable to perform sentiment
    analysis and populate the sentiment datatable

    Args: 
        sentimentDatatable_name: The name of the sentiment datatable
        
        updateFlag: A flag to be used if updating stock content is required or not

        headlineData_name: The name of the headline datatable 
    '''
    print("Starting sentiment analysis")
    sentiment_col = ['date','ticker','headline','sentiment']
    content = pd.DataFrame(columns=sentiment_col)
    sentiment_tableExists = config_sql.tableExists(table_name=sentimentDatatable_name)

    try:
        if sentiment_tableExists == False:
            raise ValueError('Data table doesnt exist... Creating one')
        else:
            retrieve_sentiment_table = config_sql.retriveTableInfo(table_name=sentimentDatatable_name)
            print("Datatable already exists")
    except ValueError as e:
        create_table = config_sql.createTable(table_name=sentimentDatatable_name, dt_contents=content)
        retrieve_sentiment_table = config_sql.retriveTableInfo(table_name=sentimentDatatable_name)
        print("Data table:",sentimentDatatable_name, "Created")
    finally:
        if updateFlag == True:
            retrieve_headline_table = config_sql.retriveTableInfo(table_name=headlineDatatable_name)
            tickersList = retrieve_headline_table['ticker'].tolist()
            dt_headlines = retrieve_headline_table['headline'].tolist()
            dt_date = retrieve_headline_table['date'].tolist()
            new_dt=sentimentAnalysis(ticker=tickersList, headlines=dt_headlines, date=dt_date)
            append_dt = config_sql.getNewRows(source_dt=retrieve_sentiment_table, new_dt=new_dt)
            config_sql.appendData(table_name=sentimentDatatable_name, dt_contents=append_dt)

    print("Sentiment analysis complete")
