import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import krakenex
import pandas as pd
from kraken.pairs import *
from graphs.stock_graphs import stock_graphs
from stats.gri import *
from stats.ma import *

## Use all containers width 
st.set_page_config(layout="wide")

#######################################
### 1. STATE VARIABLES ################
#######################################

##### 1.1. useful functions
def update_bool(key:str):
    st.session_state[key] = not(st.session_state[key])

def init_state(key):
    if key not in st.session_state:
        st.session_state[key] = False

##### 1.2. INITIALIZE ALL 

if "creator" not in st.session_state:
    st.session_state["creator"] = stock_graphs()
if "data" not in st.session_state:
    st.session_state["data"] = ""

init_state("rsi_prev")
init_state("ma_prev")
init_state("Visualize")

#######################################
### 2. PAGE SETUP #####################
#######################################

##### 2.1. Titles  
st.title("Cryptocurrency Price Visualizer")
st.sidebar.write(""" ## Cryptocurrency Price Visualizer """)


pairs_df = get_pairs()
today = dt.datetime.now().date().strftime('%d/%m/%Y')

##### 2.2. Date Button 
origin = st.sidebar.date_input("origin",dt.datetime.strptime(today, '%d/%m/%Y'))

since = int(origin.strftime("%s"))
##### 2.2. Interval Button 
interval = st.sidebar.selectbox("Interval:",[1,5,15,30,60,240,1440,10080,21600]) 

##### 2.2. Crypto Buttons  
crypto_name = st.sidebar.selectbox("Select Cryptcurrency",pairs_df["Coin"].drop_duplicates().to_list())
currency_name = st.sidebar.selectbox("Select Local Currency",pairs_df["Currency"].drop_duplicates().to_list())

##### 2.2. Visualize Button
st.sidebar.button("Visualize",key = "click_visualize")

if st.session_state["click_visualize"]:
    update_bool("Visualize")

##### 2.3. Distribute buttons
col1, col2 = st.columns([1,1])

if st.session_state["Visualize"]:
    st.markdown(f"<h2 style='text-align: center; color: grey;'>Ploting the graph between {crypto_name} and {currency_name}.</h2>", unsafe_allow_html=True)
    # st.write( f'Ploting the graph between {crypto_name} and {currency_name}.')
    with col1:
        st.selectbox("Rsi:",["None","below"], disabled = not(st.session_state["Visualize"]), key = "b_rsi") 
    with col2:
        st.selectbox("Ma:",["None","on","below"],disabled = not(st.session_state["Visualize"]), key = "b_ma") 

    ### Delete rsi and restablish prev state
    if st.session_state["rsi_prev"] and  (st.session_state["b_rsi"] == "None"):
        st.session_state["creator"].delete_indicator("rsi")
        st.session_state["rsi_prev"] = False

    ### Delete ma and restablish prev state    
    if st.session_state["ma_prev"] and  (st.session_state["b_ma"] == "None"):
        st.session_state["creator"].delete_indicator("ma")
        st.session_state["ma_prev"] = False

    ### Generate stock graph and save in cache   
    if st.session_state["b_rsi"] == "None" and st.session_state["b_ma"] == "None" and st.session_state["click_visualize"]:
        pair_str = pairs_df[(pairs_df["Coin"]==crypto_name) & (pairs_df["Currency"]==currency_name)].reset_index()["Pair"][0]
        st.session_state["data"] = get_data(pair_str,since,interval)
        st.session_state["creator"].add_stock(st.session_state["data"],"simple")

    ### Generate rsi graph and save in cache   
    if st.session_state["b_rsi"] != "None":
        s_rsi = rsi(st.session_state["data"]["close"])
        df_rsi = pd.DataFrame(s_rsi)
        st.session_state["creator"].add_rsi(df_rsi)
        st.session_state["rsi_prev"] = True

    ### Generate ma graph and save in cache   
    if  st.session_state["b_ma"] != "None":
        s_ma = media_movil(st.session_state["data"],14)
        df_ma= pd.DataFrame(s_ma)
        st.session_state["creator"].add_ma(df_ma,st.session_state["b_ma"])
        st.session_state["ma_prev"] = True

    ### Update graphs and and plot
    fig = st.session_state["creator"].update_graph()
    st.plotly_chart(fig,use_container_width=True)

