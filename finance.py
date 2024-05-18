import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import time
import psycopg2
from psycopg2 import sql

def fetch_stock_prices(symbol, api_key):
    ts = TimeSeries(key=api_key, output_format='pandas')
    try:
        data, meta_data = ts.get_intraday(symbol=symbol, interval='5min', outputsize='compact')
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

#storing data in postgres
def storing_data_posgres(data,symbol):
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        database="stock_data",
        password="1234"
    )
    cur=conn.cursor()

    for index,row in data.iterrows():
        query=sql.SQL("INSERT INTO stock_price(symbol,timestamps,price)VALUES(%s,%s,%s)")
        cur.execute(query,(symbol,index,row['4. close']))

    conn.commit()
    cur.close()
    conn.close()

#function to plot graph 
def plotstocks(data,symbol):
    fig,ax=plt.subplots()
    ax.plot(data.index, data['4. close'], label=f'{symbol} close price')
    ax.set_xlabel('Time')
    ax.set_ylabel("Price(USD)")
    ax.set_title(f"Real time Data for {symbol}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)


#main function that executes the showcasing of realtime data 
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

                storing_data_posgres(data,symbol)

                st.write("Data table:")
                st.write(data)
            time.sleep(300)
    
if __name__ == "__main__":
    main()

