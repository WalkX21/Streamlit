import streamlit as st

with st.form("Order"):
    st.write("Order details")

    fruit = st.select_slider('select a fruit', ['banana', 'apple', 'mango'])

    quantity = st.number_input("select the number of fruits")

    city = st.text_input('type your city pls')

    submitted = st.form_submit_button('Submit')

    if submitted:
        st.write("you have ordered {} {}(s) to be picked up at the {} branch".format(quantity, fruit ,city))

    st.write('These values, {} {} and {} that were set inside the from area, accessible outside the form'.format(quantity, fruit, city))

# print(fruit)