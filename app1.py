
import streamlit as st
import torch
from PIL import Image, ImageOps
import numpy as np
from torchvision import transforms
import os

# Define your model architecture (if loading state_dict)
import torch.nn as nn
import torch.nn.functional as F


# Function to load the model
@st.cache_resource
def load_model(checkpoint_path='model_final3.h5'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model('model_final3.h5', compile=False)
    try:
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        st.write("Loaded state_dict successfully.")
    except:
        model = torch.load(checkpoint_path, map_location=device)
        st.write("Loaded entire model successfully.")
    model.to(device)
    model.eval()
    return model, device

# Image preprocessing
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Adjust based on your model's input size
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],  # ImageNet mean
                             [0.229, 0.224, 0.225])  # ImageNet std
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

# Streamlit App
def main():
    st.title("Breast Cancer Detection using Histopathology Images")
    st.write("""
             Upload a histopathology image of breast tissue, and the model will predict whether it indicates cancer (`1`) or no cancer (`0`).
             """)
    
    # File uploader allows user to upload images
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")
        
        # Preprocess the image
        input_tensor = preprocess_image(image)
        
        # Load the model
        model, device = load_model('breast_cancer_model.pth')  # Update the path if necessary
        
        # Move tensor to device
        input_tensor = input_tensor.to(device)
        
        # Make prediction
        with torch.no_grad():
            output = model(input_tensor)
            probability = output.item()
            predicted_class = int(probability > 0.5)
        
        # Display the result
        if predicted_class == 1:
            st.success("Prediction: **1** (Cancer Detected)")
        else:
            st.success("Prediction: **0** (No Cancer Detected)")
        
        # Display the probability
        st.write(f"Confidence Probability: **{probability*100:.2f}%**")
        
if __name__ == "__main__":
    main()
