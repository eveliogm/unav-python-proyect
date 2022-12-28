import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import krakenex
import pandas as pd
from kraken.pairs import *
from graphs.stock_graphs import stock_graphs
from stats.gri import *
from stats.ma import *

def update_bool(key:str):
    st.session_state[key] = not(st.session_state[key])

def init_state(key):
    if key not in st.session_state:
        st.session_state[key] = False


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

if "creator" not in st.session_state:
    st.session_state["creator"] = stock_graphs()
if "data" not in st.session_state:
    st.session_state["data"] = ""
init_state("rsi_prev")
init_state("ma_prev")
# rsi_b = st.selectbox("Rsi:",["None","on","below"]) 
# ma_b = st.selectbox("Ma:",["None","on","below"]) 

# TODO: Incluir los datos dentro de las clase para no tener que actualizarlo siempre (probar a ver si funciona).  
# TODO: Incluir el calculo de rsi dentro de las clase para no tener que actualizarlo siempre hay que añadirle el tag de cache.  

init_state("Visualize")

st.sidebar.button("Visualize",key = "click_visualize")

if st.session_state["click_visualize"]:
    update_bool("Visualize")

if st.session_state["Visualize"]:
    st.write(f"Ploting the graph between {crypto_name} and {currency_name}.")

    st.selectbox("Rsi:",["None","below"],key = "b_rsi") 
    st.selectbox("Ma:",["None","on","below"], key = "b_ma") 

    if st.session_state["rsi_prev"] and  (st.session_state["b_rsi"] == "None"):
        st.session_state["creator"].delete_indicator("rsi")
        st.session_state["rsi_prev"] = False
    
    if st.session_state["ma_prev"] and  (st.session_state["b_ma"] == "None"):
        st.session_state["creator"].delete_indicator("ma")
        st.session_state["ma_prev"] = False

    if st.session_state["b_rsi"] == "None" and st.session_state["b_ma"] == "None" and st.session_state["click_visualize"]:
        pair_str = pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)].reset_index()["Pair"][0]
        st.session_state["data"] = get_data(pair_str,since,interval)
        st.write(f"Ploting the graph between {crypto_name} and {currency_name}.")
        st.session_state["creator"].add_stock(st.session_state["data"],"simple")


    if st.session_state["b_rsi"] != "None":
        s_rsi = rsi(st.session_state["data"]["close"])
        df_rsi = pd.DataFrame(s_rsi)
        st.session_state["creator"].add_rsi(df_rsi)
        fig = st.session_state["creator"].update_graph()
        st.plotly_chart(fig)
        st.session_state["rsi_prev"] = True

    if  st.session_state["b_ma"] != "None":
        s_ma = media_movil(st.session_state["data"],14)
        df_ma= pd.DataFrame(s_ma)
        st.session_state["creator"].add_ma(df_ma,st.session_state["b_ma"])
        fig = st.session_state["creator"].update_graph()
        st.plotly_chart(fig)
        st.session_state["ma_prev"] = True

    fig = st.session_state["creator"].update_graph()
    st.plotly_chart(fig)

