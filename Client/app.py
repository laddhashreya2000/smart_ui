import streamlit as st

st.title('Smart UI')

st.write('Developed by Tezan, Shreya and Rishabh')

uploaded_file = st.file_uploader("Choose a image file")


def imgshow(uploaded_file):
  if uploaded_file is not None:
	  image= uploaded_file.read()
	  img = st.image(image, caption='Train image', use_column_width=False)

imgshow(uploaded_file)

st.button("Submit")	  










# image=CV2.imread("1.png")
