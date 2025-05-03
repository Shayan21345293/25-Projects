import streamlit as st
from PIL import Image, ImageFilter
import io

st.title("Photo Manipulation by SHAYAN ALI")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)

    # Resize option
    width = st.slider("Select image width (px)", 100, 800, image.width if image.width < 800 else 800)
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio)
    image = image.resize((width, height))

    st.image(image, caption="Uploaded Image", width=100)

    effect = st.selectbox("Choose an effect", ["None", "Grayscale", "Blur", "Rotate"])
    
    if effect == "Grayscale":
        image = image.convert("L")
    elif effect == "Blur":
        image = image.filter(ImageFilter.BLUR)
    elif effect == "Rotate":
        angle = st.slider("Rotation angle", 0, 360)
        image = image.rotate(angle)

    st.image(image, caption=f"Image with {effect} effect", width=200)

    # Add download button
    buf = io.BytesIO()
    # Save as PNG for compatibility
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="manipulated_image.png",
        mime="image/png"
    )