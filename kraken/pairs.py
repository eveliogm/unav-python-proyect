import datetime as dt
import krakenex
import pandas as pd
import streamlit as st


KEY = "W/qGZGYHY1HiaOf6H/EcpiNKm7CvCm2/6FKMnheoARtek+v6mfvk2Q8Q"
PRIVATE_KEY = "6FytyFCHM93th6CFlAoH5sEoHpcQGslty//Axld1BusMRZsHm/ny9NG2RZE20AenGM47oXTTm5E5jcr38EpSug=="

kraken = krakenex.API(key=KEY, secret=PRIVATE_KEY)
ticks_schema = ["time", "open", "high", "low", "close", "vwap", "volume", "count"]

@st.cache
def get_pairs():
    pairs_res = kraken.query_public('AssetPairs')
    pairs_list = []
    for key in pairs_res["result"].keys():
        base = pairs_res["result"][key]["base"]
        quote = pairs_res["result"][key]["quote"] 
        pairs_list.append([ base, quote, key])
    return pd.DataFrame(pairs_list, columns = ["Coin","Currency","Pair"])

@st.cache
def get_data(pair,since = int(dt.datetime.now().date().strftime("%s")),interval = 15 ):
    
    if not interval in ([1,5,15,30,60,240,1440,10080,21600]):
        raise ValueError(f"Interval: {interval} must be in [1,5,15,30,60,240,1440,10080,21600] minutes")
    

    ret = kraken.query_public('OHLC', data = {'pair': pair, 'since': since, 'interval':interval})
    if len(ret["error"])==0:
        data = pd.DataFrame(ret["result"][pair],columns=ticks_schema)
        data["time"] = pd.to_datetime(data['time'],unit='s')
    else:
        raise ValueError(f"Pair: {pair} cannot be found")
    return data