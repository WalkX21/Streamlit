import streamlit as st
import pandas as pd

df = pd.DataFrame({"solide": ["pierre", "plastic", "verre"], "Liquide": [1,3,8]})

st.dataframe(df)

st.download_button("Download data", df.to_csv(index=False), file_name='data.csv')

