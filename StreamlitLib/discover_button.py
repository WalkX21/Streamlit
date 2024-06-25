import streamlit as st
import pandas as pd

st.button('Click here man')

sample_data = { "Mammals": ["CAT", "DOG", "BAT", "FOX", "PIG"], "Birds": ["parrot", "Eagle", "Duck", "Pegeon", "Vulture"]}

df = pd.DataFrame(sample_data)

st.dataframe(df)

if st.button("click here to show mammels"):
    st.dataframe(df['Mammals'])

if st.button("click here to show birds"):
    st.dataframe(df['Birds'])

