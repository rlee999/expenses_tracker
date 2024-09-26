import streamlit as st

st.title("Import page")
st.write("Used to import transactions from a csv file (GoodBudget, CommBank) into the main master_AT.csv")

master_AT = st.file_uploader('Upload master_AT')

to_upload = st.file_uploader('Upload transactions to import as csv file')