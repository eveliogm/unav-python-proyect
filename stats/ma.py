import pandas as pd
def media_movil(df, n):
    '''It takes a dataframe and a number as input, and returns a dataframe with a new column called
    'media_movil' that contains the moving average of the 'close' column
    
    Parameters
    ----------
    df
        the dataframe
    n
        The number of periods to calculate the moving average over.
    
    Returns
    -------
        The moving average of the close price.
    
    '''
    df['media_movil'] = df.close.rolling(n, min_periods=1).mean()
    return  df['media_movil'] 