import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Specifying it on the First Line of your code is advisable 
st.set_page_config(page_title='EDA - Apple Stock Prices',
                   page_icon='https://cdn.freebiesupply.com/images/large/2x/apple-logo-transparent.png',
                   layout="wide")  


"""
[![Star](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://gitHub.com/devangdayal/Medium)
&nbsp[![Follow](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/devangdayal)
&nbsp[![Follow](https://img.shields.io/twitter/follow/devangdayal?style=social)](https://www.twitter.com/devangdayal)

# Apple Stock Price Visualisation WebApp

    """
st.markdown('---')
# Sidebar Configuration
st.sidebar.image('https://cdn.freebiesupply.com/images/large/2x/apple-logo-transparent.png', width=200)
st.sidebar.markdown('# Apple Stock Price Visualiser')
st.sidebar.markdown('Stock Data varies from 1980-2022')
st.sidebar.markdown('You can visualise the Apple \'s Stock Prices Trend and Pattern over the given span.') 


st.sidebar.markdown('---')
st.sidebar.write('Developed by Devang Dayal')
st.sidebar.write('Contact here @[devangdayal](https://github.com/devangdayal)')

# Dataset Importing and Index Processing

@st.cache(allow_output_mutation=True) # We include this so as to decrease the loading time of the Web App
def data_ret():
    data = pd.read_csv('Apple_stock_history.csv')
    data['Date'] = pd.to_datetime(data['Date'],format='%Y/%m/%d')
    data.reset_index(drop=True,inplace=True)
    data.set_index('Date',inplace=True)
    return data

df = data_ret()

# Let us display the Raw Data into our Web App
st.subheader('Glimpse of Dataset')
st.dataframe(df.head())

# Let us display the basic statistical information of our dataset
st.subheader('Statistical Info of the Dataset')
st.write(df.describe())


st.markdown("** You can select specific time duration **")
df_sliced = df

col1, col2 = st.columns(2)

with col1:
    st.write('Select the Initial Date')
    init_dt = st.date_input('Initial Date',min_value= datetime.date(1980, 12, 12),max_value=datetime.date(2022,1,3),value=datetime.date(1980,12,12))

with col2:    
    st.write('Select the Final Date')
    final_dt = st.date_input('Final Date',min_value=datetime.date(1980,12,12),max_value=datetime.date(2022,1,3),value=datetime.date(2022,1,3))

if(init_dt != None or final_dt != None):
    if(init_dt <final_dt):
        df_sliced = df[init_dt:final_dt]
    else:
        st.warning("Entered the Date in Correct Order")
        
st.subheader("Apple Stock Price Open & Close Value (1980-2022)")
df_open_close = df_sliced[['Open','Close']]


# Select the Chart type you want to visualise
option_oc = st.selectbox('What Visual Chart You want to Visualise ?',('Line Chart','Line Area Chart','Bar Chart'))


if option_oc == 'Line Chart':
    st.line_chart(df_open_close)
elif option_oc == 'Line Area Chart':
    st.area_chart(df_open_close)
elif option_oc == 'Bar Chart':
    st.bar_chart(df_open_close)
else:
    st.area_chart(df_open_close)

# Volume of Stock Traded 
st.subheader("Volumne of Apple Stock Traded in 1980-2022")
st.markdown("\n\n")
st.bar_chart(df_sliced['Volume'])


# Market Cap
df_sliced['Market Cap'] = df_sliced['Open'] * df_sliced['Volume']
st.subheader("Market Value of Apple Stock Traded in 1980-2022")
st.markdown("\n\n")
st.bar_chart(df_sliced['Market Cap'])


# Highs and Lows of Apple Stocks 
st.subheader("High & Low Values of Apple Stock Traded in 1980-2022")
st.markdown("\n\n")

# Select the Chart type you want to visualise
option_hl = st.selectbox('Select Visual Chart You want to Visualise ?',('Line Area Chart','Bar Chart','Line Chart'))

if option_hl == 'Line Chart':
    st.line_chart(df_sliced[['High','Low']])
elif option_hl == 'Line Area Chart':
    st.area_chart(df_sliced[['High','Low']])
elif option_hl == 'Bar Chart':
    st.bar_chart(df_sliced[['High','Low']])
else:
    st.area_chart(df_sliced[['High','Low']])

# Moving Average over 50 days and 200 days
st.subheader('Moving Average of Open and Closing Values of Stock')
mvavg_len = st.slider('Select the Window Size (in days) of Moving Average',min_value=0,max_value=250,value=50)
mvg_oc =  df_sliced[['Open','Close']].rolling(50).mean()
st.line_chart(mvg_oc)

