import os
import re
import cv2
import numpy as np
import streamlit as st
import easyocr
import fitz  # PyMuPDF for PDF to image conversion
from PIL import Image

def preprocess_image(image):
    """Preprocess the image to enhance OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(binary, kernel, iterations=1)
    return dilated

def easyocr_recognize(image, reader):
    """Perform OCR using EasyOCR."""
    results = reader.readtext(image)
    return " ".join([result[1] for result in results])

def process_large_image(image, reader, chunk_size=1000):
    """Process large images by splitting them into chunks."""
    height, width = image.shape[:2]
    texts = []
    
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            chunk = image[y:y+chunk_size, x:x+chunk_size]
            text = easyocr_recognize(chunk, reader)
            texts.append(text)
    
    return " ".join(texts)

def process_pdf(pdf_bytes, reader):
    """Convert PDF pages to images using PyMuPDF and perform OCR."""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)
        
        preprocessed_image = preprocess_image(img_np)
        text = process_large_image(preprocessed_image, reader)
        full_text += text + "\n\n"

    return full_text

# Streamlit UI
st.title("Handwritten Text Recognition and Image Search")

# Initialize EasyOCR reader
@st.cache_resource
def load_easyocr():
    return easyocr.Reader(['en'])  # Add 'kn' for Kannada support

reader = load_easyocr()

# State to store the search query
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Allow both images and PDFs for the recognized text section
uploaded_file = st.file_uploader("Upload an image or PDF for handwritten text", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_bytes = uploaded_file.read()
        recognized_text = process_pdf(pdf_bytes, reader)
    else:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        preprocessed_image = preprocess_image(image)
        recognized_text = process_large_image(preprocessed_image, reader)

    st.subheader("Recognized Text:")
    st.write(recognized_text)

    # Search functionality
    search_query = st.text_input("Enter a keyword or phrase to search:", value=st.session_state.search_query)
    
    if search_query:
        st.session_state.search_query = search_query

        if search_query.lower() in recognized_text.lower():
            st.success(f"'{search_query}' found in the text!")
            highlighted_text = re.sub(f'(?i){re.escape(search_query)}', lambda m: f"<span style='color:red'>{m.group()}</span>", recognized_text)
            st.markdown(f"Highlighted Text: {highlighted_text}", unsafe_allow_html=True)
        else:
            st.error(f"'{search_query}' not found in the text.")

# Image Search Functionality
search_image_file = st.file_uploader("Upload another image or PDF to search for the recognized text", type=["jpg", "jpeg", "png", "pdf"])

if search_image_file is not None and st.session_state.search_query:
    if search_image_file.type == "application/pdf":
        search_pdf_bytes = search_image_file.read()
        search_recognized_text = process_pdf(search_pdf_bytes, reader)
    else:
        search_image = cv2.imdecode(np.frombuffer(search_image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        preprocessed_search_image = preprocess_image(search_image)
        search_recognized_text = process_large_image(preprocessed_search_image, reader)
    
    st.subheader("Recognized Text from Search File:")
    st.write(search_recognized_text)

    if st.session_state.search_query.lower() in search_recognized_text.lower():
        st.success(f"'{st.session_state.search_query}' found in the search file!")
        highlighted_search_text = re.sub(f'(?i){re.escape(st.session_state.search_query)}', lambda m: f"<span style='color:red'>{m.group()}</span>", search_recognized_text)
        st.markdown(f"Highlighted Text from Search File: {highlighted_search_text}", unsafe_allow_html=True)
    else:
        st.error(f"'{st.session_state.search_query}' not found in the search file.")
