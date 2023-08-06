import pandas as pd
import requests
# Returns the first 20 ticker and their details in a pandas dataframe


# Quantitative
def MostVolatile():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=111&s=ta_mostvolatile"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df


def MostActive():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=111&s=ta_mostactive"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df


def TopGainers():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&ft=4"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df
