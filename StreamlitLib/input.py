import streamlit as st

st.markdown('## Single-line Input')
text_input= st.text_input("exemple de mammifaire stp")
st.write (text_input)

st.markdown("Multi-Line Input")
text_area = st.text_area("give 3 birds")
st.write(text_area)