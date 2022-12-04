import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import krakenex
import pandas as pd
from kraken.pairs import *
from graphs.stock_graphs import stock_graphs
from stats.gri import *
st.title("Cryptocurrency Price Visualizer")

st.sidebar.write(""" ## Cryptocurrency Price Visualizer """)

# today = dt.datetime.now().date().strftime('%d/%m/%Y')
# origin = st.date_input("origin",dt.datetime.strptime(today, '%d/%m/%Y'))

pairs_df = get_pairs()

crypto_name = st.sidebar.selectbox("Select Cryptcurrency",pairs_df["Coin"].drop_duplicates().to_list())
currency_name = st.sidebar.selectbox("Select Local Currency",pairs_df["Currency"].drop_duplicates().to_list())

today = dt.datetime.now().date().strftime('%d/%m/%Y')
origin = st.sidebar.date_input("origin",dt.datetime.strptime(today, '%d/%m/%Y'))
since = int(origin.strftime("%s"))
interval = st.sidebar.selectbox("Interval:",[1,5,15,30,60,240,1440,10080,21600]) 

rsi_b = st.button("rsi")

creator = stock_graphs()

if st.sidebar.button("Visualize") or rsi_b:

    rsi_b = st.selectbox("Rsi:",["None","on","below"]) 
    ma_b = st.selectbox("Ma:",["None","on","below"]) 
    pair_str = pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)].reset_index()["Pair"][0]
    data = get_data(pair_str,since,interval)
    st.write(f"Ploting the graph between {crypto_name} and {currency_name}.")
    creator.add_stock(data,"simple")

    if rsi_b != "None":
        s_rsi = rsi(data["close"])
        df_rsi = pd.DataFrame(s_rsi)
        creator.add_rsi(df_rsi,rsi_b)
   
    # fig = slide_plot(data,crypto_name)

    fig = creator.update_graph()
    st.plotly_chart(fig)
    s = data['close'].tail(1) 
    st.write(f"The closing price for the {crypto_name} is {s} ")