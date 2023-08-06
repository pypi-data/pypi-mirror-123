import unittest
import pandas as pd

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from stock_scraper_AiCore import process
stockContent_name = 'testing_stockData'
headline_name = 'testing_headlineData'
sentiment_name = 'testing_sentimentData'
class ProcessTestCase(unittest.TestCase):


    def test_stockData(self):
        process.stockData(stockContent_name=stockContent_name, updateFlag=True)
        actual_value = type(process.tableExitsCheck(table_exists=True, table_name=stockContent_name))
        expected_values = pd.DataFrame

        self.assertEqual(expected_values, actual_value)
    
    def test_stockHeadlineData(self):
        process.stockHeadlineData(stockInfoDatatable_name=stockContent_name,updateFlag=True,headlineDatatable_name=headline_name)
        actual_value = type(process.tableExitsCheck(table_exists=True, table_name=headline_name))
        expected_values = pd.DataFrame

        self.assertEqual(expected_values, actual_value)
    
    def test_sentimentData(self):
        process.sentimentData(sentimentDatatable_name=sentiment_name,updateFlag=True,headlineDatatable_name=headline_name)
        actual_value = type(process.tableExitsCheck(table_exists=True, table_name=headline_name))
        expected_values = pd.DataFrame

        self.assertEqual(expected_values, actual_value)

