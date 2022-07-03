import unittest
import pandas as pd
import json 

class TestMetrics(unittest.TestCase):
    """Class to test metrics calculations."""
    
    def setUp(self):
        """Method to init data from a json file."""
        with open('test_data.json') as file:
            self.__data = json.load(file)
        self.__dataframe = pd.DataFrame(self.__data)

    def test_sum(self):
        """Test the sum of all time values"""
        total_sum = sum(row['time'] for row in self.__data)
        self.assertEqual(self.__dataframe["time"].sum(), total_sum)
    
    def test_average(self):
        """Test the average of all time values"""
        total_sum = sum(row['time'] for row in self.__data)
        average = total_sum/len(self.__data)
        self.assertEqual(self.__dataframe["time"].mean(), average)

    def test_minimum(self):
        """Test the minimum of all time values"""
        self.assertEqual(self.__dataframe["time"].min(), min(row['time'] for row in self.__data))

    def test_maximum(self):
        """Test the maximum of all time values"""
        self.assertEqual(self.__dataframe["time"].max(), max(row['time'] for row in self.__data))
