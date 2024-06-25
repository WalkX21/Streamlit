import streamlit as st

st.title('First "real" website')

st.subheader('About us')
st.write('### Frist Name: Bennani')
st.markdown('### Name : mohammed')

st.subheader('different types of medias can be displayed, like: ')


st.image("https://griddb-pro.azureedge.net/en/wp-content/uploads/2021/08/streamlit-1160x650.png") #method displays images.  st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.write('## Images:')

#st.image("https://sb.ecobnb.net/app/uploads/sites/3/2021/09/Progetto-senza-titolo-5.jpg.webp") #method displays images.  st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.image("assets/music.png", caption="The keys, by Matt Duncan", use_column_width="auto") #method displays images.  st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.markdown('audio of this banger')
st.audio("https://bit.ly/rainaws3")   # displays audio.  st.audio(data, format="audio/wav", start_time=0)
st.markdown("## Videos:")

st.video("https://www.youtube.com/watch?v=yG0RhKFTonw") # displays video. st.video(data, format="video/mp4", start_time=0)


