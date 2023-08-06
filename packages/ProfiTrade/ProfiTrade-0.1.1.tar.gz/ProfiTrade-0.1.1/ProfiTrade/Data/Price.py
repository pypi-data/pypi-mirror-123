# For AlphaVantage API (GET Requests return a JSON object)
import requests
import json
import pandas as pd  # main dataframe built on python
import random  # for selecting a random key from the inputed list of keys

class Crypto:
    """
    -------------------------------------------------------
    Init: 
        - coin: Cryptocurrency (e.x. btc)
        - fiat: The fiat currency of your choice (e.x. usd)
        - balance: Your initial balance no commas (10000) 
        - key: Alpha vantage key in a [List]
    -------------------------------------------------------
    Functions:
        - historical: This function is used to obtain 
                    historical price data
        - current:    This function is used to obtain or add
                    current price data to a pandas dataframe
    -------------------------------------------------------
    """

    def __init__(self, coin, fiat, balance, key):
        self.fiat, self.coin, self.balance, self.key = fiat.upper(
        ), coin.upper(), balance, key[random.randint(0, len(key)-1)]  # could be optimized (future version)
        return

    def historical(self, outputsize, interval):
        """
        ------------------------------------------------
        This function takes the interval and outputsize
        as parameters. Using the alpha vantage API, it 
        returns a df with historical price data.
        ------------------------------------------------
        Parameters:
            - interval: 1, 5, 15, 30, 60 (mins)
            - outputsize: compact (latest 100), full 
        ------------------------------------------------
        Returns:
            - df: A pandas dataframe with the open, 
                  high, low, close and volume.
        """
        url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={}&market={}&interval={}min&outputsize={}&apikey={}'.format(
            self.coin, self.fiat, interval, outputsize, self.key) # create the custom request URL
        intraday = requests.get(url).json() # send get request and convert the response to json

        # cleaning and sorting the data frame data
        df = pd.DataFrame.from_dict(
            intraday['Time Series Crypto ({}min)'.format(interval)], orient='index')  # parse the time series dict to the dataframe
        df = df.loc[::-1]  # invert the dataframe
        df.reset_index(inplace=True)  # convert index to a column because time is given as an index rather than col
        df = df.rename(columns={'index': 'time'})  # rename the index to time
        df['4. close'] = df['4. close'].astype(
            float)  # convert close prices to a float for faster arithmetic processes
        return df

    def current(self, df, toAppend):
        """
        ------------------------------------------------
        If toAppend is set true, the function takes in
        a pandas dataframe and appends the current 
        price data. Else, when toAppend is false, using 
        the alpha vantage API, it returns a df 
        with the current crypto exchange rate.
        ------------------------------------------------
        Parameters:
            - df: a pandas dataframe with time, open,
                  high, low, close and volume.
            - toAppend: (bool) True or False. If true,
                        price data is appended to df.
        ------------------------------------------------
        Returns:
            - df: A pandas dataframe with the current 
                  price data.
        """
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}'.format(
            self.coin, self.fiat, self.key)
        data = requests.get(url).json() # convert the response to JSON

        if toAppend == True:
            # convert it to  a dictionary that can be added to the dataframe
            data, price, time, bid, ask = data['Realtime Currency Exchange Rate'], data[
                '5. Exchange Rate'], data['6. Last Refreshed'], data['8. Bid Price'], data['9. Ask Price'] # set data in vars
            # create new dictionary with same format as historical df data
            exchange = {'time': time, '1. open': ask, '2. high': bid,
                        '3. low': None, '4. close': price, '5. volume': None} # asign vars in a dictionary
            # add it to the df
            df = df.append(exchange, ignore_index=True)
            df['4. close'] = df['4. close'].astype(
                float)  # convert close price data type to float
        else:
            df = data # else, assign the raw to data as df and return it
        return df


class Stock:
    """
    -------------------------------------------------------------------------
    Init: 
        - ticker: Stock ticker of your choice
        - balance: Your initial balance no commas (10000) 
        - key: Alpha vantage key in a [List]
    -------------------------------------------------------------------------
    Functions:
        - historicalIntraday:         This function is used to obtain 
                                    historical intraday price data.
        - historicalIntradayExtended: This function is used to obtain or add
                                    extended price data to a pandas dataframe.
        - historicalDaily:            This function is used to obtain historical
                                    daily price data.
    -------------------------------------------------------------------------
    """

    def __init__(self, ticker, balance, key):
        self.ticker, self.balance, self.key = ticker.upper(), balance, key[random.randint(
            0, len(key)-1)]  # could be optimized (future version) 

    def historicalIntraday(self, interval, outputsize):
        """
        ------------------------------------------------
        This function takes the interval and outputsize
        as parameters, using the alpha vantage API, it 
        returns a df with historical intraday price data
        ------------------------------------------------
        Parameters:
            - interval: 1, 5, 15, 30, 60 (mins)
            - outputsize: compact (latest 100), full 
        ------------------------------------------------
        Returns:
            - df: A pandas dataframe with the open, 
                  high, low, close and volume.
        """
        ticker = self.ticker
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}min&outputsize={}&apikey={}".format(
            ticker.upper(), interval, outputsize, self.key)
        response = requests.get(url)  # add error handling code (try else)
        intraday = response.json()

        # adding to a DF
        df = pd.DataFrame.from_dict(intraday['Time Series ({}min)'.format(
            str(interval))], orient='index')  # parse the time series dict to the dataframe
        df = df.loc[::-1]  # invert the dataframe
        df.reset_index(inplace=True)  # convert index to a column
        df = df.rename(columns={'index': 'time'})  # rename the index to time
        df['4. close'] = df['4. close'].astype(
            float)  # convert close prices to a float
        return df

    def historicalIntradayExtended(self, interval):
        """
        ------------------------------------------------
        This function takes the interval as parameters, 
        using the alpha vantage API, it returns a df 
        with extended historical intraday price data.
        ------------------------------------------------
        Parameters:
            - interval: 1, 5, 15, 30, 60 (mins)
        ------------------------------------------------
        Returns:
            - df: A csv file with the open, high, low, 
                  close and volume
        """
        ticker = self.ticker.upper()
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={}&interval={}min&slice=year1month12&apikey={}".format(
            ticker.upper(), interval, self.key)
        df = pd.read_csv(url)
        return df

    def historicalDaily(self, outputsize):
        """
        ------------------------------------------------
        This function takes the outputsize as parameters, 
        using the alpha vantage API, it returns a df with
        historical daily price data.
        ------------------------------------------------
        Parameters:
            - outputsize: compact (latest 100), full 
        ------------------------------------------------
        Returns:
            - df: A csv file with the open, high, low, 
                  close and volume
        """
        ticker = self.ticker
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize={}&apikey={}".format(
            ticker.upper(), outputsize, self.key)
        response = requests.get(url)
        intraday = response.json()
        # adding to a new DF
        # parse the time series dict to the dataframe
        df = pd.DataFrame.from_dict(
            intraday['Time Series (Daily)'], orient='index')
        df = df.loc[::-1]  # invert the dataframe
        df.reset_index(inplace=True)  # convert index to a column
        df = df.rename(columns={'index': 'time'})  # rename the index to time
        df['4. close'] = df['4. close'].astype(
            float)  # convert close prices to a float
        return df
