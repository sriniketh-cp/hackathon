mport os
import re
import cv2
import numpy as np
import streamlit as st
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import vision
import fitz  # PyMuPDF for PDF to image conversion (alternative to poppler)

# Set the scope for the Vision API
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def authenticate_via_oauth():
    """Authenticate to the Google Vision API using OAuth 2.0."""
    creds = None

    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\My Code\kanada LLM\credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def preprocess_image(image):
    """Preprocess the image to enhance OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)  # Use a smaller kernel for small text
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # Smaller structuring element for finer details
    dilated = cv2.dilate(binary, kernel, iterations=1)

    return dilated

def detect_text(client, image):
    """Detect text in the image using Google Cloud Vision API."""
    _, buffer = cv2.imencode('.png', image)
    content = buffer.tobytes()
    
    image = vision.Image(content=content)
    response = client.document_text_detection(
        image=image,
        image_context={"language_hints": ["kn"]}  # Add lat/long for context if needed
    )

    return response

def extract_text(response):
    """Extract text from the API response, preserving formatting.""" 
    full_text = response.full_text_annotation.text
    cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
    return cleaned_text

def google_vision_ocr(image):
    """Perform OCR using Google Cloud Vision API with optimizations."""
    creds = authenticate_via_oauth()
    client = vision.ImageAnnotatorClient(credentials=creds)
    
    preprocessed_image = preprocess_image(image)
    response = detect_text(client, preprocessed_image)
    recognized_text = extract_text(response)
    
    return recognized_text

def process_pdf(pdf_bytes):
    """Convert PDF pages to images using PyMuPDF and perform OCR."""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""
    
    # Convert each page to an image and perform OCR
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        
        # Use Google Vision API for text recognition
        text = google_vision_ocr(img_np)
        full_text += text + "\n\n"

    return full_text

# Streamlit UI
st.title("Handwritten Text Recognition and Image Search")

# State to store the search query
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Allow both images and PDFs for the recognized text section
uploaded_file = st.file_uploader("Upload an image or PDF for handwritten text", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    # If the file is a PDF, process it separately
    if uploaded_file.type == "application/pdf":
        pdf_bytes = uploaded_file.read()
        recognized_text = process_pdf(pdf_bytes)
    else:
        # If it's an image, process the image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        recognized_text = google_vision_ocr(image)

    st.subheader("Recognized Text:")
    st.write(recognized_text)

    # Search functionality
    search_query = st.text_input("Enter a keyword or phrase to search:", value=st.session_state.search_query)
    
    if search_query:
        st.session_state.search_query = search_query  # Save search query in session state

        if search_query in recognized_text:
            st.success(f"'{search_query}' found in the text!")
            highlighted_text = recognized_text.replace(search_query, f"<span style='color:red'>{search_query}</span>")
            st.markdown(f"Highlighted Text: {highlighted_text}", unsafe_allow_html=True)
        else:
            st.error(f"'{search_query}' not found in the text.")

# Image Search Functionality
search_image_file = st.file_uploader("Upload another image or PDF to search for the recognized text", type=["jpg", "jpeg", "png", "pdf"])

if search_image_file is not None and st.session_state.search_query:
    if search_image_file.type == "application/pdf":
        search_pdf_bytes = search_image_file.read()
        search_recognized_text = process_pdf(search_pdf_bytes)
    else:
        search_image = cv2.imdecode(np.frombuffer(search_image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        search_recognized_text = google_vision_ocr(search_image)
    
    st.subheader("Recognized Text from Search File:")
    st.write(search_recognized_text)

    if st.session_state.search_query in search_recognized_text:
        st.success(f"'{st.session_state.search_query}' found in the search file!")
        highlighted_recognized_text = recognized_text.replace(st.session_state.search_query, f"<span style='color:red'>{st.session_state.search_query}</span>")
        st.markdown(f"Highlighted Text from Original Image: {highlighted_recognized_text}", unsafe_allow_html=True)
    else:
        st.error(f"'{st.session_state.search_query}' not found in the search file.")
