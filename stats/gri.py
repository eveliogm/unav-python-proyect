import pandas as pd
import numpy as np

def rsi_single(df,col,n): 
    """
    Calculate rsi for a column in a pandas dataframe
  
    Parameters:
    df (pandas.DataFrame): dataframe that contains the column with numeric values to be calculated 
    col (str): Column name in df that contins all numerics values. 
  
    Returns:
    float: rsi value is between 0 to 100
    """
    delta = df[col].diff()
    n = diff.shape[0]
    delta_pos = diff[diff > 0].sum()/n
    delta_neg = diff[diff < 0].sum()/n
    if diff_neg:
        rs = diff_pos / abs(diff_neg)
        rsi = 100.0-(100.0)/(1.0 + rs)
    else:
        rsi = 100.0
    return rsi

def rsi(data: pd.Series, win = 14 , ma = "EWMA") -> pd.Series:
    """
    Calculate rsi for a column in a pandas dataframe. 
    SMA calculates the average of price data, while EMA gives more weight to current data.
  
    Parameters:
    over (pandas.Series): dataframe that contains the column with numeric values to be calculated 
    w (int): Window of the rsi calculation
  
    Returns:
    float: rsi value is between 0 to 100
    """
    if  ma == "EWMA":
        fn_roll = lambda s: s.ewm(com=(win-1), adjust=True, min_periods = win).mean()
    elif ma == "EMA":
        fn_roll = lambda s: s.ewm(span = win,min_periods = win).mean()
    elif ma == "SMA":
        fn_roll = lambda s: s.rolling(win).mean()
    elif ma == "RMA":
        fn_roll = lambda s: s.ewm(alpha=1 / win).mean()
    else:
        raise ValueError(f"MA type: {ma} is not a valid method. Try EMA, SMA, RMA or EWMA")
    
    # Calculate diferences over every record from the previous one
    delta = data.diff()

    # Copy series. For ups and downs clip it value to 0 if negatives or positive respectively
    up, down = delta.copy(), delta.copy()
    
    up[up < 0] = 0
    down[down > 0] = 0
    down *= -1
    
    win_up = fn_roll(up) 
    win_down =  fn_roll(down)
  
    rs = win_up / win_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    
    # if win_down == 0 --> RS --> inf and rsi = 100
    # if win_up == 0 --> RS --> 0 and rsi = 0
    rsi[:] = np.select([win_down == 0, win_up == 0, True], [100.0, 0.0, rsi])
    rsi.name = 'rsi'

    # Assert that rsi (from win value in data (taking into account the first nan from diff) is
    # between 0 and 100. 
    check_rsi = rsi[win:]
    assert ((0 <= check_rsi) & (check_rsi <= 100)).all()
    
    return rsi