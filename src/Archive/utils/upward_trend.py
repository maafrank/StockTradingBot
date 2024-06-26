import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

light_green = '\033[92m'
light_blue = '\033[94m'
reset = '\033[0m'
stocks = {
    'ABNB': 0, 'ALGN': 0, 'AMD': 0, 'CEG': 0, 'AMZN': 0,
    'AMGN': 0, 'AEP': 0, 'ADI': 0, 'ANSS': 0, 'AAPL': 0,
    'AMAT': 0, 'GEHC': 0, 'ASML': 0, 'TEAM': 0, 'ADSK': 0,
    'ATVI': 0, 'ADP': 0, 'AZN': 0, 'BKR': 0, 'AVGO': 0,
    'BIIB': 0, 'BKNG': 0, 'CDNS': 0, 'ADBE': 0, 'CHTR': 0,
    'CPRT': 0, 'CSGP': 0, 'CRWD': 0, 'CTAS': 0, 'CSCO': 0,
    'CMCSA': 0, 'COST': 0, 'CSX': 0, 'CTSH': 0, 'DDOG': 0,
    'DXCM': 0, 'FANG': 0, 'DLTR': 0, 'EA': 0, 'EBAY': 0,
    'ENPH': 0, 'ON': 0, 'EXC': 0, 'FAST': 0, 'GFS': 0,
    'META': 0, 'FI': 0, 'FTNT': 0, 'GILD': 0, 'GOOG': 0,
    'GOOGL': 0, 'HON': 0, 'ILMN': 0, 'INTC': 0, 'INTU': 0,
    'ISRG': 0, 'MRVL': 0, 'IDXX': 0, 'JD': 0, 'KDP': 0,
    'KLAC': 0, 'KHC': 0, 'LRCX': 0, 'LCID': 0, 'LULU': 0,
    'MELI': 0, 'MAR': 0, 'MCHP': 0, 'MDLZ': 0, 'MRNA': 0,
    'MNST': 0, 'MSFT': 0, 'MU': 0, 'NFLX': 0, 'NVDA': 0,
    'NXPI': 0, 'ODFL': 0, 'ORLY': 0, 'PCAR': 0, 'PANW': 0,
    'PAYX': 0, 'PDD': 0, 'PLTR': 0, 'PYPL': 0, 'PEP': 0, 'QCOM': 0,
    'REGN': 0, 'ROST': 0, 'SIRI': 0, 'SGEN': 0, 'SBUX': 0,
    'SNPS': 0, 'TSLA': 0, 'TXN': 0, 'TMUS': 0, 'VRSK': 0,
    'VRTX': 0, 'WBA': 0, 'WBD': 0, 'WDAY': 0, 'XEL': 0,
    'ZM': 0, 'ZS': 0,
}
def find_upward(stocks=stocks):
    for stock_symbol in stocks.keys():
        count = 0
        if ma(stock_symbol, window=5): stocks[stock_symbol] +=1
        if rsi(stock_symbol, period=14, rsi_threshold=50): stocks[stock_symbol] += 1
        if macd(stock_symbol): stocks[stock_symbol] += 1
        if roc(stock_symbol, period=5): stocks[stock_symbol] += 1
        if adx(stock_symbol, period=14, adx_threshold=25): stocks[stock_symbol] += 1
        if obv(stock_symbol, window=5): stocks[stock_symbol] += 1
        if ichimoku(stock_symbol): stocks[stock_symbol] += 1
        if fibonacci(stock_symbol, fibonacci_levels=[0.236, 0.382, 0.618]): stocks[stock_symbol] += 1
        if chaikin(stock_symbol, window=3): stocks[stock_symbol] += 1
        if parabolic_sar(stock_symbol): stocks[stock_symbol] += 1
        print(f"{stock_symbol=}, {stocks[stock_symbol]=}")
    stocks = dict(sorted(stocks.items(), key=lambda item: item[1], reverse=True))
    print(stocks)
    for key, value in stocks.items():
        # Fetch historical stock data using yfinance
        stock_data = yf.Ticker(key)
        stock_data = stock_data.history(period="1d", interval="1m")
            
        # Extract the open and close prices for today
        open_price = stock_data['Open'][0]
        close_price = stock_data['Close'][-1]

        # Calculate the percentage gain or loss
        percentage_change = ((close_price - open_price) / open_price) * 100
        if percentage_change > 0:
            print(f"{key=} {value=} {open_price=:.4f} {close_price=:.4f} {light_green}{percentage_change=:.4f}{reset}")
        else:
            print(f"{key=} {value=} {open_price=:.4f} {close_price=:.4f} {light_blue}{percentage_change=:.4f}{reset}")
    return stocks


def ma(stock_symbol, window=5):
    """
    Check if a stock is in an upward trend based on historical prices using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        window (int): The number of periods to calculate the moving average (default is 5).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < window:
        raise ValueError("Not enough data points for the chosen window size.")

    # Calculate the moving average using the last 'window' data points
    moving_average = stock_data['Close'].rolling(window=window).mean().iloc[-1]

    # Check if the last closing price is above the moving average
    last_close = stock_data['Close'].iloc[-1]
    return last_close > moving_average

def rsi(stock_symbol, period=14, rsi_threshold=50):
    """
    Check if a stock is in an upward trend based on the RSI indicator using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        period (int): The time period to calculate the RSI (default is 14).
        rsi_threshold (float): The RSI threshold to define an upward trend (default is 50).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < period:
        raise ValueError("Not enough data points for the chosen RSI period.")

    # Calculate the price change for each day
    price_diff = stock_data['Close'].diff()

    # Calculate the gains and losses for each day
    gains = price_diff.where(price_diff > 0, 0)
    losses = -price_diff.where(price_diff < 0, 0)

    # Calculate the average gains and losses over the RSI period
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()

    # Calculate the RSI using the average gains and losses
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))

    # Check if the last RSI value is above the threshold
    last_rsi = rsi.iloc[-1]
    return last_rsi > rsi_threshold

def macd(stock_symbol):
    """
    Check if a stock is in an upward trend based on the MACD indicator using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < 26:
        raise ValueError("Not enough data points for the chosen MACD period.")

    # Calculate the 12-day and 26-day exponential moving averages
    ema_12 = stock_data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = stock_data['Close'].ewm(span=26, adjust=False).mean()

    # Calculate the MACD line and the signal line (9-day EMA of the MACD line)
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    # Check if the MACD line crosses above the signal line (MACD bullish crossover)
    is_crossover = (macd_line.iloc[-1] > signal_line.iloc[-1]) and (macd_line.iloc[-2] <= signal_line.iloc[-2])
    return is_crossover

def roc(stock_symbol, period=5):
    """
    Check if a stock is in an upward trend based on the Rate of Change (ROC) indicator using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        period (int): The time period to calculate the ROC (default is 5).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < period:
        raise ValueError("Not enough data points for the chosen ROC period.")

    # Calculate the Rate of Change (ROC) over the specified period
    roc = 100 * (stock_data['Close'].pct_change(periods=period).iloc[-1])

    # Check if the ROC value is positive (indicating an upward trend)
    return roc > 0

def adx(stock_symbol, period=14, adx_threshold=25):
    """
    Check if a stock is in an upward trend based on the Average Directional Index (ADX) using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        period (int): The time period to calculate the ADX (default is 14).
        adx_threshold (float): The ADX threshold to define a strengthening trend (default is 25).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < period + 1:
        raise ValueError("Not enough data points for the chosen ADX period.")

    # Calculate the True Range (TR) for each day
    high_low_diff = stock_data['High'] - stock_data['Low']
    high_close_diff = np.abs(stock_data['High'] - stock_data['Close'].shift())
    low_close_diff = np.abs(stock_data['Low'] - stock_data['Close'].shift())
    true_range = pd.concat([high_low_diff, high_close_diff, low_close_diff], axis=1).max(axis=1)

    # Calculate the Directional Movement (+DM and -DM) for each day
    positive_directional_movement = (stock_data['High'] - stock_data['High'].shift()).apply(lambda x: x if x > 0 else 0)
    negative_directional_movement = (stock_data['Low'].shift() - stock_data['Low']).apply(lambda x: x if x > 0 else 0)

    # Calculate the smoothed True Range, +DM, and -DM over the ADX period
    smoothed_true_range = true_range.rolling(window=period).mean()
    smoothed_positive_directional_movement = positive_directional_movement.rolling(window=period).mean()
    smoothed_negative_directional_movement = negative_directional_movement.rolling(window=period).mean()

    # Calculate the Directional Movement Index (DMI) and the Average True Range (ATR)
    dmi = 100 * (np.abs(smoothed_positive_directional_movement - smoothed_negative_directional_movement) / (smoothed_positive_directional_movement + smoothed_negative_directional_movement))
    atr = smoothed_true_range.rolling(window=period).mean()

    # Calculate the Average Directional Index (ADX)
    dx = 100 * (atr.rolling(window=period).mean() / (dmi + atr))
    adx = dx.rolling(window=period).mean()

    # Check if the ADX value is rising and above the threshold (indicating a strengthening trend)
    return adx.iloc[-1] > adx.iloc[-2] and adx.iloc[-1] > adx_threshold

def obv(stock_symbol, window=5):
    """
    Check if a stock is in an upward trend based on the On-Balance Volume (OBV) using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        window (int): The number of periods to calculate the OBV (default is 5).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < window + 1:
        raise ValueError("Not enough data points for the chosen OBV window.")

    # Calculate the On-Balance Volume (OBV) over the specified window
    obv = stock_data['Volume'].diff(periods=window).apply(lambda x: x if x > 0 else 0).cumsum()

    # Check if the OBV value is rising over the past week
    return obv.iloc[-1] > obv.iloc[-2]

def ichimoku(stock_symbol):
    """
    Check if a stock is in an upward trend based on the Ichimoku Cloud using yfinance data.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data using yfinance
    stock_data = yf.download(stock_symbol, progress=False)

    if len(stock_data) < 52:
        raise ValueError("Not enough data points for the Ichimoku Cloud calculation.")

    # Calculate the Ichimoku Cloud components
    conversion_line = (stock_data['High'].rolling(window=9).max() + stock_data['Low'].rolling(window=9).min()) / 2
    base_line = (stock_data['High'].rolling(window=26).max() + stock_data['Low'].rolling(window=26).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (stock_data['High'].rolling(window=52).max() + stock_data['Low'].rolling(window=52).min()) / 2
    lagging_span = stock_data['Close'].shift(-26)

    # Check if the price is above the cloud and the cloud is green (positive)
    is_price_above_cloud = stock_data['Close'].iloc[-1] > leading_span_a.iloc[-1] and stock_data['Close'].iloc[-1] > leading_span_b.iloc[-1]
    is_cloud_green = leading_span_a.iloc[-1] > leading_span_b.iloc[-1]

    return is_price_above_cloud and is_cloud_green

def fibonacci(stock_symbol, fibonacci_levels=[0.236, 0.382, 0.618]):
    """
    Check if a stock is in an upward trend based on Fibonacci Retracement Levels using yfinance data for the past week.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        fibonacci_levels (list): List of Fibonacci retracement levels to check (default is [0.236, 0.382, 0.618]).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data for the past week using yfinance
    stock_data = yf.download(stock_symbol, period='1wk', progress=False)

    if len(stock_data) < 5:
        raise ValueError("Not enough data points for the past week for Fibonacci Retracement Levels.")

    # Calculate the price range over the past week
    price_range = stock_data['High'].iloc[-1] - stock_data['Low'].iloc[-1]

    # Calculate the Fibonacci retracement levels
    fibonacci_support_levels = []
    for level in fibonacci_levels:
        retracement_price = stock_data['High'].iloc[-1] - (price_range * level)
        fibonacci_support_levels.append(retracement_price)

    # Check if the current price is above any of the Fibonacci support levels
    current_price = stock_data['Close'].iloc[-1]
    return any(current_price > level for level in fibonacci_support_levels)

def chaikin(stock_symbol, window=3):
    """
    Check if a stock is in an upward trend based on the Chaikin Oscillator using yfinance data for the past week.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.
        window (int): The number of periods to calculate the Chaikin Oscillator (default is 3).

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data for the past week using yfinance
    stock_data = yf.download(stock_symbol, period='1wk', progress=False)

    if len(stock_data) < window + 1:
        raise ValueError("Not enough data points for the past week for the Chaikin Oscillator.")

    # Calculate the Money Flow Multiplier (MFM)
    typical_price = (stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 3
    money_flow = typical_price * stock_data['Volume']
    mfm = ((typical_price - stock_data['Low']) - (stock_data['High'] - typical_price)) / (stock_data['High'] - stock_data['Low'])
    mfm = mfm * money_flow

    # Calculate the Accumulation/Distribution Line (ADL)
    adl = mfm.cumsum()

    # Calculate the Chaikin Oscillator
    chaikin_oscillator = adl.rolling(window=window).mean() - adl.rolling(window=window).mean().shift(window)

    # Check if the Chaikin Oscillator value is positive (indicating an upward trend)
    return chaikin_oscillator.iloc[-1] > 0

def parabolic_sar(stock_symbol):
    """
    Check if a stock is in an upward trend based on the Parabolic SAR using yfinance data for the past week.

    Parameters:
        stock_symbol (str): The stock symbol, e.g., 'AAPL' for Apple Inc.

    Returns:
        bool: True if the stock is in an upward trend, False otherwise.
    """
    # Fetch historical stock data for the past week using yfinance
    stock_data = yf.download(stock_symbol, period='1wk', progress=False)

    if len(stock_data) < 5:
        raise ValueError("Not enough data points for the past week for the Parabolic SAR.")

    # Initialize Parabolic SAR values
    af = 0.02  # Acceleration factor
    max_af = 0.20  # Maximum acceleration factor
    sar = stock_data['Low'].iloc[-1]  # Initial SAR value

    trend_up = True  # Flag to indicate if the trend is upward

    # Calculate the Parabolic SAR for the past week
    for i in range(1, len(stock_data)):
        prev_sar = sar

        if trend_up:
            if stock_data['Low'].iloc[i] > prev_sar:
                sar = prev_sar + af * (stock_data['High'].iloc[i] - prev_sar)
                sar = min(sar, stock_data['Low'].iloc[i - 1], stock_data['Low'].iloc[i - 2])
            else:
                trend_up = False
                sar = stock_data['High'].iloc[i - 1]
        else:
            if stock_data['High'].iloc[i] < prev_sar:
                sar = prev_sar + af * (stock_data['Low'].iloc[i] - prev_sar)
                sar = max(sar, stock_data['High'].iloc[i - 1], stock_data['High'].iloc[i - 2])
            else:
                trend_up = True
                sar = stock_data['Low'].iloc[i - 1]

        af = min(af + 0.02, max_af)  # Increase acceleration factor within the limit

    # Check if the current price is above the Parabolic SAR
    current_price = stock_data['Close'].iloc[-1]
    return current_price > sar
