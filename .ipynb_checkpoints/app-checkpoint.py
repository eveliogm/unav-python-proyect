import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import krakenex
import pandas as pd

st.title("Cryptocurrency Price Visualizer")

st.sidebar.write(""" ## Cryptocurrency Price Visualizer """)


# KEY = "W/qGZGYHY1HiaOf6H/EcpiNKm7CvCm2/6FKMnheoARtek+v6mfvk2Q8Q"
# PRIVATE_KEY = "6FytyFCHM93th6CFlAoH5sEoHpcQGslty//Axld1BusMRZsHm/ny9NG2RZE20AenGM47oXTTm5E5jcr38EpSug=="

kraken = krakenex.API(key=KEY, secret=PRIVATE_KEY)
origin = dt.datetime.strptime('19/11/2022', '%d/%m/%Y')
since = int(origin.strftime("%s"))
interval = 15
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

pairs_df = get_pairs()

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


crypto_name = st.sidebar.selectbox("Select Cryptcurrency",pairs_df["Coin"].drop_duplicates().to_list())
currency_name = st.sidebar.selectbox("Select Local Currency",pairs_df["Currency"].drop_duplicates().to_list())

print(pairs_df.head())
print(crypto_name)
print((pairs_df["Coin"]==crypto_name).any())
print((pairs_df["Currency"]==currency_name).any())
print(pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)].reset_index()["Pair"][0])
# pair_str = pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)]["Pair"][0]

if st.sidebar.button("Visualize"):
    pair_str = pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)].reset_index()["Pair"][0]
    data = get_data(pair_str,since,interval)
    st.write(f"Ploting the graph between {crypto_name} and {currency_name}.")

    fig = plt.figure(figsize=(8,6))
    plt.title(f"{crypto_name} Coin Price Visualizer")
    plt.xlabel("Year")
    plt.ylabel(f"Price in {currency_name}")
    plt.plot(data['close'],color='green')
    st.pyplot(fig)
    s = data['close'].tail(1) 
    st.write(f"The closing price for the {crypto_name} is {s} ")