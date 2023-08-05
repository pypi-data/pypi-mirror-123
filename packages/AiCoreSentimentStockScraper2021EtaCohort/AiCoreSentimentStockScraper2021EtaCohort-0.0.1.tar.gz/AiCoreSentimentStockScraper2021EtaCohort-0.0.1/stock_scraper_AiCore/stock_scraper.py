import pandas as pd 
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
from typing import Optional


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

obj = SentimentIntensityAnalyzer()



def getSnpCompanies() -> Optional[list]:
    '''
    This method scrapes the snp500 stocks from wikidpedia. 

    The purpose of this method is to retrieve data from
    wikipedia as its constantly being updated. 

    Returns: 
        list: A list of ticker symbols 
    '''
    tickers = []
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    snp_df = table[0]
    symbol = snp_df['Symbol']
    for ticker in symbol:
        tickers.append(ticker)
    return tickers



def getStockContent(tickers:list) -> Optional[pd.DataFrame]:
    '''
    This method scrapes stock info on each stock

    The purpose of this method is to use the list of 
    snp500 stocks and scrape stock name, stock sector,
    stock type, stock region ,stock info 

    Args:
        tickers: Stock tickers of the snp500 stocks

    Returns:
        Pandas dataframe: A datatable of stock info in pandas format
    '''
    dict_name = ['ticker','stock_name','stock_sector','stock_type','stock_region','stock_info']
    stock_data = {}
    for i in range(len(dict_name)):
        stock_data[dict_name[i]] = []

    for ticker in tqdm(tickers):
        if "." in ticker:
            ticker = ticker.replace(".","-")
        finviz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}
        url = finviz_url + ticker
        try:
            req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            stock_name = html.find_all('a', {'class':'tab-link'})[12].text
            stock_sector= html.find_all('a', {'class':'tab-link'})[13].text
            stock_type= html.find_all('a', {'class':'tab-link'})[14].text
            stock_region= html.find_all('a', {'class':'tab-link'})[15].text
            stock_info= html.find('td', {'class':'fullview-profile'}).text
        except Exception as e:
            stock_name='Unknown'
            stock_sector='Unknown'
            stock_type='Unknown'
            stock_region='Unknown'
            stock_info='Unknown'
            print(e, url)
        
        finally:
            stock_value = [ticker,stock_name,stock_sector,stock_type,stock_region,stock_info]
            for i in range(len(stock_value)):
                    stock_data[dict_name[i]].append(stock_value[i])


    df = pd.DataFrame.from_dict(stock_data)          
    return df



def getNewsHeadlines(tickers:list) -> Optional[pd.DataFrame]:
    '''
    This method scrapes news headlines of the stocks in the snp500

    The purpose of this method is to use the stock tickers and scrapes 
    the top 100 news headlines related to the stock

    Args:
        tickers: Stock tickers of the snp500 stocks

    Returns:
        Pandas dataframe: A datatable of stock info in pandas format

    '''
    dict_name = ['ticker','headline','date']

    headline_data = {}
    for i in range(len(dict_name)):
        headline_data[dict_name[i]] = []
    
    for ticker in tqdm(tickers):
        if "." in ticker:
            ticker = ticker.replace(".","-")
        try:

            finviz_url = 'https://finviz.com/quote.ashx?t='
            news_tables = {}
            url = finviz_url + ticker
            req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
            resp = urlopen(req)
            html = BeautifulSoup(resp, features="lxml")
            n=100
            news_tables = html.find(id='news-table')
            news_tables[ticker] = news_tables
            df = news_tables[ticker]
            df_tr = df.findAll('tr')
            for i, table_row in enumerate(df_tr):
                article_headline = table_row.a.text
                td_text = table_row.td.text
                article_date = td_text.strip()
                headline_value = [ticker,article_headline,article_date]

                for i in range(len(headline_value)):
                    headline_data[dict_name[i]].append(headline_value[i])
            
                if i == n-1:
                    break
        except Exception as e:
            print(e, ticker)
            headline_value = [ticker,article_headline,article_date]
            for i in range(len(headline_value)):
                headline_data[dict_name[i]].append("unknown")
    df = pd.DataFrame.from_dict(headline_data)    
    return df





def getTwiterData():
    try:
        pass
    
    except Exception as e:
        print(e)


  