import streamlit as st

#This is the first item of text our application will have.It will be displayed at the top of the application
st.title('Exploring Streamlit')
#for any major section of our application
st.header("Display Header")
# for smaller section within each major section
st.subheader("Display Sub Header")
#General text within our application body
st.text("Display with st.text()")
# For special formatting requirements
st.markdown("`pip install streamlit`")
# to display the Captions of items displayed in our applications.
st.caption("Streamlit caption options")
#will display whatever we specify in the parentheses based on the type of thing it is
st.write("run Streamlit using the commnande `streamlit Hello`")

#Latex method to display matematical equation
st.latex(r"s \left ( t \right ) = ut + \dfrac{1}{2} at^2")