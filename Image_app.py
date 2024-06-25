import streamlit as st
import numpy as np
from PIL import Image

st.title("Super Photo Editor 🔥")

def display_figures(img1,img2):
    fig1_left, fig2_right = st.columns(2)
    with fig1_left:
        st.markdown("## Original image")
        st.image(img1)
    with fig2_right:
        st.markdown("## Processed image")
        st.image(img2)

    
image_file = st.sidebar.file_uploader("Upload an image file pls", type= ["jpeg", "png", "tif"])

if image_file is not None:

    input_image = Image.open(image_file)

    effect = st.sidebar.selectbox("select the type of image manipulation", ["Rotate Image", "flip Image", "resize"])

    if effect == "Rotate Image":
        angle = st.sidebar.select_slider('select the angle of rotation', [0,90,180,270,360])
        output_image = input_image.rotate(angle)
        
    if effect == "Flip Image":
        with st.sidebar:
            mirror_choice = st.radio("choose how to flip the image", ["Horizontally", "Vertically"])
            if mirror_choice == "Horizontally":
                output_image = input_image.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                output_image = input_image.transpose(Image.FLIP_TOP_BOTTOM)

    if effect == "Resize":
        scale_factor = st.sidebar.slider('select the pourcentage size', 5,10,6)
        output_image = input_image.resize((input_image.width//scale_factor, input_image.height//scale_factor))

    if st.button("Process That Image"):
        display_figures(input_image, output_image)


    
