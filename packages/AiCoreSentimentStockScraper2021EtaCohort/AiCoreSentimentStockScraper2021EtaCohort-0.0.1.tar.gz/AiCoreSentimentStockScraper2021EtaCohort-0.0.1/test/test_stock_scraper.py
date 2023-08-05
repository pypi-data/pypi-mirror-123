import unittest
import pandas as pd

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from stock_scraper_AiCore import stock_scraper

class StockScraperTestCase(unittest.TestCase):

    def test_snpCompanies(self):
        actual_value = type(stock_scraper.getSnpCompanies())
        expected_values = list

        self.assertEqual(expected_values, actual_value)

    def test_StockContent(self):
        tickers = ['TSLA', 'MSFT']
        actual_value = type(stock_scraper.getStockContent(tickers=tickers))
        expected_values = pd.DataFrame

        self.assertEqual(expected_values, actual_value)
    
    def test_NewsHeadlines(self):
        tickers = ['TSLA', 'MSFT']
        actual_value = type(stock_scraper.getNewsHeadlines(tickers=tickers))
        expected_values = pd.DataFrame

        self.assertEqual(expected_values, actual_value)

