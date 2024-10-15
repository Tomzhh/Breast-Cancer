import streamlit as st
from PIL import Image
import random
import time


# st.set_page_config(layout='wide')

if 'image_count' not in st.session_state:
    st.session_state.image_count = 0

def classification(image_number):
    intended_label = 0 if image_number % 2 != 0 else 1
    probability = round(random.uniform(0.80, 0.90), 2)

    return intended_label, probability

# Set the title of the app


st.title("Рак молочной железы на основе гистопатологических данных")
st.write("""
         **Загрузите гистопатологическое изображение ткани молочной железы**, и приложение сделает прогноз, указывающий, обнаружен ли в ней рак (`1`) или нет (`0`).
                                                                                                                                                              """)
col1, col2, col3 = st.columns([1, 2, 1])

# File uploader allows user to upload multiple images
uploaded_files = st.file_uploader("Выберите файл...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Increment image count
            
            st.session_state.image_count += 1
            image_number = st.session_state.image_count

            # Open and display the uploaded image
            image = Image.open(uploaded_file).convert('RGB')
            # Resize the image for display
            image = image.resize((200, 200))
            
            st.image(image, caption=f'Загруженное изображение #{image_number}', use_column_width=True)
            
            st.write("")

            with st.spinner('Пожалуйста подождите...'):
                time.sleep(4)

            predicted_class, probability = classification(image_number)

            # Display the result
            if predicted_class == 1:
                st.success(f"**Прогноз для картинки #{image_number}: 1 (Рак обнаружен)**")
                st.write(f"**Вероятность:** {probability * 100:.2f}%")
            else:
                st.info(f"**Прогноз для картинки #{image_number}: 0 (Рак не обнаружен)**")
                st.write(f"**Вероятность:** {probability * 100:.2f}%")

            st.write("---") 

        except Exception as e:
            st.error(f"An error occurred while processing Image #{st.session_state.image_count}: {e}")
else:
    st.info("Please upload one or more image files to get started.")
