import streamlit as st

sample_data = [3.10, 7.23, -3.89,5.98,-9.43]
col1, col2, col3 = st.columns(3)

col1.subheader("Line chart")
col1.line_chart(sample_data)

col2.subheader('Area')
col2.area_chart(sample_data)

col3.write(sample_data)