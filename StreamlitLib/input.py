import streamlit as st
import pandas as pd 

st.markdown('## Single-line Input')
text_input= st.text_input("exemple de mammifaire stp")
st.write (text_input)

st.markdown("Multi-Line Input")
text_area = st.text_area("give 3 birds")
st.write(text_area)

# tests to understand

# name=st.text_input("What's your name?")
# age=st.number_input("how old are you", min_value= 0, max_value= 99, value = 0)
# dude = {
#     'name':name,
#     'age':age
# }

# df =pd.DataFrame.from_dict(dude)
# st.dataframe(df)