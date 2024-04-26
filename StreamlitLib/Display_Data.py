import streamlit as st
import pandas as pd
import numpy as np

st.markdown('### Metric Example ')
# Display a metric in big bold font, with an optional indicator of how the metric changed.
st.metric(label='Temperature', value="70 °F",delta='-1,2 °F')

st.metric(label="Gas price",value=4,delta=-0.5,delta_color='inverse')

st.metric(label='Active developers',value=123,delta=-12,delta_color='off')

st.markdown("### Json Example ")
#Display object or string as a pretty-printed JSON string
st.json({
    'foo':'bar',
    'bar':'boz',
    'stuff':[
        'stuff1',
        'stuff2',
        'stuff3',
        'stuff5',
    ],
})

sample_data ={'Cities':["New York","San Jose","Casablanca","Paris","London"]}
df=pd.DataFrame(sample_data)
st.markdown("### DATAFRAME EXEMPLE ")
st.dataframe(df)

df=pd.DataFrame(
    np.random.randn(10,20),
    columns=('col %d' % i for i in range(20))
)

#you can also pass a Pandas Styler object to change the style of the renderd DataFrame
st.dataframe(df.style.highlight_max(axis=0))

st.markdown("### TABLE EXAMPLE ")
st.table(df)