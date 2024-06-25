import streamlit as st

integer_number = st.number_input("Enter an integer", min_value= 0, max_value= 100, value = 0)
st.write(integer_number, type(integer_number))

float_number = st.number_input('enter a value', min_value= 0.0, max_value=100.00, value= 12.45)
st.write(float_number, type(float_number))