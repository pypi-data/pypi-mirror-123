import pandas as pd
import requests
# Returns the first 20 ticker and their details in a pandas dataframe


# Technical
def HorizontalSupportResistance():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=110&s=ta_p_horizontal&o=-&ar=180"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df


def SidewaysHighVolume():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=110&s=ta_p_channel&o=-volume"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df


def SidewaysChannel():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://finviz.com/screener.ashx?v=110&s=ta_p_channel"
    response = requests.get(url, headers=headers).text
    df = pd.read_html(response)[-2]
    df.columns = df.iloc[0]
    df = df[1:]
    df.drop("No.", axis=1, inplace=True)
    return df
