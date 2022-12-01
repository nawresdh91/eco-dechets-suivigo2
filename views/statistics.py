from database import Database
import pandas as pd
import streamlit as st


def main():
    df = pd.read_sql("SELECT * FROM fournisseur", Database().connect, index_col="id")
    col1, col2 = st.columns(2)
    st.write(df)

    #with col1:
        #st.text("Stat")

    #with col2:
        #st.write(df)
