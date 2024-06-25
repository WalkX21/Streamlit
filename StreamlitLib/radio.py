import streamlit as st

st.radio("which of these is not a mammal?",["Dog", "Cat", "Eagle", "Pig"]) # reponse unique comme sur kahoot (pas plusieurs)

st.selectbox("which of these is a mammal ?", ["pigeon", "Dove", "Fox", "Vulture"]) #meilleur affichage de choix mais encore une fois, choix unique

st.select_slider("which of these is not a bird?", ["Ostrich", "flamingo", 'Bat', 'Pigeon']) #c'edst un slider, ideal pour des valeurs