import datetime as dt
import streamlit as st
import snowflake.connector

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
        st.text('Submitted !')


if st.button('Show Data'):
    cur = cnx.cursor()
    data = cur.execute("select * from USERINPUTDB.OR_REV_SCHEMA.Orders_tbl").fetchall()
    df = st.dataframe(data)
