import datetime as dt
import streamlit as st
import snowflake.connector
import pandas as pdt
import matplotlib.pyplot as plt

st.title('Orders tool')
date = st.date_input("🗓date:", dt.date(2023, 1, 1))
BA = st.text_input("Business Area:")
Division = st.text_input("Division:")
Orders = st.text_input("Orders:")
date_str = str(date)
cnx = snowflake.connector.connect(**st.secrets["snowflake"])
if st.button('Submit'):
    cur = cnx.cursor()
    cur.execute(
        "insert into USERINPUTDB.OR_REV_SCHEMA.Orders_tbl values ('" + date_str + "' , '" + BA + "' , '" + Division + "' , '" + Orders + "' ) ;")
    st.text(' Orders value added !')

if st.button('Show Data'):
    cur = cnx.cursor()
    data = cur.execute("select * from USERINPUTDB.OR_REV_SCHEMA.Orders_tbl").fetchall()
    df = pd.DataFrame(data)
    print(df)
    df.plot(kind='line', x='Date', y='Orders')
    plt.show()
