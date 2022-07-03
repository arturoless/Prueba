from multiprocessing import connection
import unittest
import pandas as pd
import json 
import requests

from database import DatabaseConnection

class TestCountries(unittest.TestCase):
    """Class to test countries format."""
    
    def test_status_code(self):
        """Test if request is successfull"""
        URL = "https://restcountries.com/v3.1/all"
        response = requests.get(url = URL)
        self.assertEqual(response.status_code, 200)
    
    def test_format(self):
        """Test if request is response has the appropriated format"""
        URL = "https://restcountries.com/v3.1/all"
        response = requests.get(url = URL)
        countries = response.json()
        country = countries[0]
        self.assertIsNotNone(country.get("region", None))
        self.assertIsNotNone(country.get("name", None))
        self.assertIsNotNone(country.get("name", None).get("official", None))
        self.assertIsNotNone(country.get("languages", None))
        

class TestMetrics(unittest.TestCase):
    """Class to test metrics calculations."""
    
    def setUp(self):
        """Method to define init data from a json file."""
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

class TestDatabase(unittest.TestCase):
    """Class to test database connection class"""

    def test_singleton_pattern(self):
        """Test the instance to check singleton pattern"""
        first_instance = DatabaseConnection()
        second_instance = DatabaseConnection()
        self.assertEqual(first_instance, second_instance)
    
    def test_succesfull_connection(self):
        """Test the connection when correct url is given"""
        database_connection = DatabaseConnection()
        connection = database_connection.connect(r"database.db")
        self.assertIsNotNone(connection)
    