import json
import requests
import hashlib
from timeit import default_timer as timer
import webbrowser
import pandas as pd
from pandas import DataFrame
from database import DatabaseConnection

connection = DatabaseConnection()
connection = connection.connect(r"database.db")
connection.execute('''CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sum REAL NOT NULL,
    average REAL NOT NULL,
    minimum REAL NOT NULL,
    maximum REAL NOT NULL
)''')

URL = "https://restcountries.com/v3.1/all"

response = requests.get(url = URL)
countries = response.json()
formatted_countries = []

for country in countries:
    start_time = timer()
    languages = country.get("languages", {})
    languages_values = languages.values()
    language = ""
    if len(languages_values) > 1: 
        value_iterator = iter(languages_values)
        language = next(value_iterator)

    formatted_country = {
        "region" : country.get("region", ""),
        "country" : country.get("name", {}).get("official", ""),
        "language" :  hashlib.sha1(language.encode()).hexdigest(),
        "time" : 1000*(timer() - start_time)
    }

    formatted_countries.append(formatted_country)

def show_dataframe(dataframe: DataFrame)-> None:
    """Write html file, with dataframe table inside, and open the file in browser.
    Args:
        dataframe (DataFrame): Dataframe class with data
    """
    text_file = open("index.html", "w")
    text_file.write(dataframe.to_html())
    webbrowser.open("index.html")

dataframe = pd.DataFrame(formatted_countries)
connection.execute(f'''
    INSERT INTO metrics (sum, average, minimum, maximum) VALUES(
        {dataframe["time"].sum()},
        {dataframe["time"].mean()},
        {dataframe["time"].min()},
        {dataframe["time"].max()}
    )
''')

cursor = connection.execute("SELECT * FROM metrics")
rows = cursor.fetchall()
for row in rows:
    print(row)

with open('data.json', 'w') as convert_file:
    convert_file.write(json.dumps(formatted_countries))
    
show_dataframe(dataframe)
