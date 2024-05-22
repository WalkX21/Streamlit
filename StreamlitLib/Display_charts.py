import streamlit as st
import numpy as np
import graphviz as graphviz
import pandas as pd
df = np.random.randn(7, 7)
st.markdown('displaying data using charts')
st.dataframe(df)
st.markdown("line charts")
st.line_chart(df)

st.markdown('area chart')
st.area_chart(df)

st.markdown('bar chart')
st.bar_chart(df)

st.markdown('gephaviz demo')
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
    }
''')

# graphviz, permet§ de creer un diagramme en python, 
# les fleches dans le codes sont desd fleches dans l'output, 
# le premier stipulé est le premier affché dans l'output,on peut specifier des reliages quand tu veux

st.markdown('## map things')
df = pd.DataFrame( #dataframe = tableau, premier parametre = lignes puis colones
    np.random.randn(2, 2) / [50, 50] + [33, 7], # a mettre a casa
    columns=(['lat','lon'])

)

st.map(df)