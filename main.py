# This is a sample Python script.
import pandas as pd
import krakenex
from pykrakenapi import KrakenAPI
import matplotlib.pyplot as plt
api = krakenex.API()
k = KrakenAPI(api)
ans=True
def descarga_datos_y_grafica(moneda):
 global df
 df, eth = k.get_ohlc_data(moneda, interval=60, ascending=True)
 df['time'] = pd.to_datetime(df['time'], utc=True, unit='s')
 print(df)
 df.plot(x='time', y='close', kind="line", figsize=(10, 5))
 plt.show()
def media_movil(df, n):
 df['media_movil'] = df.close.rolling(n, min_periods=1).mean()
 df.plot(x='time', y='media_movil', kind="line", figsize=(10, 5))
 plt.show()

def media_movil_y_cot(df):
 df.plot(x="time", y=["close", "media_movil"], kind="line", figsize=(10, 5))
 plt.show()
while ans:
    print ("""
    1.Ethereum
    2.Tether
    3.Ninguna
    """)
    ans=input("¿Que cripto desea graficar? ")

    if ans=="1":
        descarga_datos_y_grafica("ETHUSD")
        media_movil(df, 60)
        media_movil_y_cot(df)
    elif ans=="2":
        descarga_datos_y_grafica("USDTUSD")
    elif ans=="3":
        break
    elif ans !="":
        print("\n Not Valid Choice Try again")

