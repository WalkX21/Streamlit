import streamlit as st

st.multiselect("which of these are birds", ["Fox", "Eagle", "Bat", "Dove"]) #on choisie plusieur info

slider_int = st.slider("select an integer", min_value=0, max_value=100,value=25)# on commence sur le 25 et puis on peut bouger
st.write(slider_int, type(slider_int))

