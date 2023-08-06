import pandas


def SMA(df, period):
    """
    ------------------------------------------------
    Given a pandas dataframe, this function
    calculates and adds simple moving average.
    ------------------------------------------------
    Parameters:
        - period: periods of data for SMA calculation
    ------------------------------------------------
    Returns: (None)
    """
    df['{}MA'.format(period)] = df['{}'.format(
        '4. close')].rolling(period).mean()
    return


def RSI(df, period):
    """
    ------------------------------------------------
    Given a pandas dataframe, this function
    calculates and adds relative strength index.
    ------------------------------------------------
    Parameters:
        - period: periods of data for RSI calculation
    ------------------------------------------------
    Returns: (None)
    """
    # converts all close prices str -> float
    df['4. close'] = df['4. close'].astype(float)
    delta = df['4. close'].diff()  # diff of the current - previous
    up = delta.clip(lower=0)  # if its lower than 0, clip to 0
    down = -1*delta.clip(upper=0)  # neg to pos, upper than 0 clip
    rsi_period = period-1  # period= period + 1 cause index from 0
    ema_up = up.ewm(com=rsi_period, adjust=False).mean()
    ema_down = down.ewm(com=rsi_period, adjust=False).mean()
    rs = ema_up/ema_down
    df['RSI'] = 100 - (100/(1+rs))  # gets added as a float
    return


def EMA(df, period):
    """
    ------------------------------------------------
    Given a pandas dataframe, this function
    calculates and adds expotential moving average.
    ------------------------------------------------
    Parameters:
        - period: periods of data for EMA calculation
    ------------------------------------------------
    Returns: (None)
    """
    df['{}EMA'.format(period)] = df['4. close'].ewm(
        span=period, adjust=False).mean()
    return


def MACD(df):  # Moving Average Convergence Divergence
    """
    ------------------------------------------------
    Given a pandas dataframe, this function
    calculates and adds Moving Average Convergence 
    Divergence.
    ------------------------------------------------
    Parameters:
        - period: periods of data for MACD calculation
    ------------------------------------------------
    Returns: (None)
    """
    # 12 EMA - 26 EMA
    ema12 = df['4. close'].ewm(span=12, adjust=False).mean()
    ema26 = df['4. close'].ewm(span=26, adjust=False).mean()
    macd_calc = ema12 - ema26
    df['MACD'] = macd_calc
    signal = macd_calc.ewm(span=9, adjust=False).mean()
    df['MACDEMA'] = signal
    return


def BOLBANDS(df, period):
    """
    ------------------------------------------------
    Given a pandas dataframe, this function
    calculates and adds the Boll. Bands 
    ------------------------------------------------
    Parameters:
        - period: periods of data for BOLBANDS calculation
    ------------------------------------------------
    Returns: (None)
    """
    df['ma_20'] = df['4. close'].rolling(period).mean()  # moving average
    df['std'] = df['4. close'].rolling(period).std()  # standard deviation
    df['upper_bolband'] = df['ma_20'] + (2*df['std'])
    df['lower_bolband'] = df['ma_20'] - (2*df['std'])
    return
