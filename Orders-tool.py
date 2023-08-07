import datetime as dt
import streamlit as st
import snowflake.connector
import pandas as pd
import streamlit.components.v1 as components

st.title('🧾 Orders tool 🧾')

date_, BA_, Division_, Orders_, submit_ = st.columns(5, gap="small")

with date_:
    date = st.date_input("📅 Date:", dt.date(2023, 1, 1))
with BA_:
    BA = st.selectbox("🏛️ Business Area:", ("EL", "MO", "PA", "RA"))
# BA = st.text_input("Business Area:")
with Division_:
    if BA == "EL":
        Division = st.selectbox("🏛️ Division:", ("ELDS", "ELIP", "ELSE", "ELSB", "ELSP"))
    elif BA == "PA":
        Division = st.selectbox("🏛️ Division:", ("PAEN", "PAPI", "PAMP", "PAMA"))
    elif BA == "MO":
        Division = st.selectbox("🏛️ Division:", ("MODP", "MOLM", "MOLMG", "MONM", "MOMS", "MOSD", "MOT"))
    elif BA == "RA":
        Division = st.selectbox("🏛️ Division:", ("RARO", "RAMA"))

# Division = st.text_input("Division:")
with Orders_:
    Orders = st.text_input("💲 Orders:")

date_str = str(date)
cnx = snowflake.connector.connect(**st.secrets["snowflake"])

with submit_:
    if st.button('Submit'):
        cur = cnx.cursor()
        cur.execute(
            "insert into USERINPUTDB.OR_REV_SCHEMA.Orders_tbl values ('" + date_str + "' , '" + BA + "' , '" + Division + "' , '" + Orders + "' ) ;")
        st.success('Success !')

Raw_data, Orders_ba, Orders_mnth, Orders_div, pbi, Mfcast = st.tabs(
    ["Raw data", "Orders by BA", "Orders by Month", "Orders by Division", "Power BI", "Manual Forecast"])

with Raw_data:
    cur = cnx.cursor()
    data = cur.execute("select * from USERINPUTDB.OR_REV_SCHEMA.Orders_tbl")
    df = pd.DataFrame(data, columns=['Date', 'BA', 'Division', 'Orders'])
    st.table(df)

with Orders_ba:
    cur = cnx.cursor()
    data = cur.execute("select BA,sum(Orders) from USERINPUTDB.OR_REV_SCHEMA.ORDERS_TBL group by BA;")
    df = pd.DataFrame(data, columns=['BA', 'Orders'])
    st.bar_chart(data=df, x='BA', y='Orders', use_container_width=True)

with Orders_mnth:
    cur = cnx.cursor()
    data = cur.execute(
        "select month(DATE_::DATE) as monthn, monthname(DATE_::DATE) as month_,sum(Orders) from USERINPUTDB.OR_REV_SCHEMA.ORDERS_TBL group by monthn,month_ order by monthn;")
    df = pd.DataFrame(data, columns=['monthn', 'month_', 'Orders'])
    st.line_chart(data=df, x='month_', y='Orders', use_container_width=True)

with Orders_div:
    cur = cnx.cursor()
    data = cur.execute("select DIVISION,sum(Orders) from USERINPUTDB.OR_REV_SCHEMA.ORDERS_TBL group by DIVISION;")
    df = pd.DataFrame(data, columns=['Division', 'Orders'])
    st.bar_chart(data=df, x='Division', y='Orders', use_container_width=True)

with pbi:
    components.iframe(
        "https://app.powerbi.com/reportEmbed?reportId=ef33ff8c-5730-42d4-8ca6-840df4d54990&autoAuth=true&ctid=372ee9e0-9ce0-4033-a64a-c07073a91ecd",
        width=800, height=500)

with Mfcast:

    cur = cnx.cursor()
    new_qtr = st.text_input("New Qtr:")
    if st.button('Add'):
        cur.execute("insert into USERINPUTDB.OR_REV_SCHEMA.MFORECAST_TBL (QTR) values ('" + new_qtr + "');  ")
    data = cur.execute("select * from USERINPUTDB.OR_REV_SCHEMA.MFCAST_VW;")
    df = pd.DataFrame(data, columns=['Qtr', 'OrFcast'])
    tbl = st.data_editor(df)

    if st.button('Save'):
        for i in range(len(tbl)):
            cur.execute("update USERINPUTDB.OR_REV_SCHEMA.MFORECAST_TBL set ORDERS_FCAST = '" + str(
                tbl.OrFcast.loc[i]) + "' where QTR = '" + str(tbl.Qtr.loc[i]) + "' ;")
        st.success('Saved !')
    st.line_chart(data=df, x='Qtr', y='OrFcast', use_container_width=True)
#    st.text(str(tbl.OrFcast.loc[0]))
#    st.line_chart(data=tbl, x='Qtr', y='OrFcast', use_container_width=True)
