import unittest
import pandas as pd


if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from stock_scraper_AiCore.data_base import SqlDB

class DataBaseTestCase(unittest.TestCase):
    def test_tableExists(self):
        self.config_sql = SqlDB()
        self.dataTables = ['stock_content','stock_headlines','stock_sentiment']


        for dataTable in self.dataTables:
            actual_value = self.config_sql.tableExists(table_name=str(dataTable))
            self.assertIsInstance(actual_value, bool)
    
    def test_retriveTableInfo(self):
        self.config_sql = SqlDB()
        self.dataTables = ['a']
        expected_values = pd.DataFrame

        for dataTable in self.dataTables:
            actual_value = type(self.config_sql.retriveTableInfo(table_name=str(dataTable)))
            self.assertEqual(actual_value,expected_values)

    def test_createTable(self):
        self.config_sql = SqlDB()
        self.dataTables = ['a','b','c']
        self.content = pd.DataFrame({'a':[0], 'b':[0],'c':[0]})
        expected_values = bool
        
        for dataTable in self.dataTables:
            tableExists = self.config_sql.tableExists(table_name=str(dataTable))
            if tableExists == True:
                self.config_sql.deleteTable(table_name=str(dataTable))
            creat_db = self.config_sql.createTable(table_name=str(dataTable),dt_contents=self.content)
            actual_value = type(self.config_sql.tableExists(table_name=str(dataTable)))
            self.assertEqual(actual_value,expected_values)
    
    def test_appendData(self):
        self.config_sql = SqlDB()
        self.dataTables = ['a','b','c']
        self.content = pd.DataFrame({'a':[1,2], 'b':[3,4],'c':[5,6]})
        expected_values = pd.DataFrame

        for dataTable in self.dataTables:
            self.config_sql.appendData(table_name=str(dataTable),dt_contents=self.content)
            actual_value = type(self.config_sql.retriveTableInfo(table_name=dataTable))
            self.assertEqual(actual_value,expected_values)


    def test_getNewRows(self):
        config_sql = SqlDB()
        self.new_dt = pd.DataFrame({'a':[1,2], 'b':[3,4],'c':[5,6]})
        self.source_dt = pd.DataFrame({'a':[1,2], 'b':[3,4]})
        expected_values = pd.DataFrame
        actual_value= type(config_sql.getNewRows(new_dt=self.new_dt,source_dt=self.source_dt))
        self.assertEqual(actual_value,expected_values)

        




