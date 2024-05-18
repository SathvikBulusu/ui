import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import time


def fetch_stock_prices(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    try:
        data, meta_data = ts.get_intraday(symbol=symbol, interval='30min', outputsize='compact')
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


def plotstocks(data,symbol):
    fig,ax=plt.subplots()
    ax.plot(data.index, data['4. close'], label=f'{symbol} close price')
    ax.set_xlabel('Time')
    ax.set_ylabel("Price(USD)")
    ax.set_title(f"Real time Data for {symbol}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)




def main ():
    st.title("Real time streaming data of intraday")
    
    api_key= st.text_input("enter your aplha vantage api key : ")
    symbol = st.text_input("enter your company's stock name to know the price :")

    if api_key and symbol:
        while True:
            data=fetch_stock_prices(symbol,api_key)
            if data is not None:
                st.subheader(f"Real-time data {symbol}")

                st.write("largest data point :")
                st.write(data.head(1))

                plotstocks(data,symbol)

                st.write("Data table:")
                st.write(data)
            time.sleep(1800)

if __name__ == "__main__":
    main()

