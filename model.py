# import os
# import io
# import re
# import streamlit as st
# from google.cloud import vision
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from PIL import Image, ImageEnhance, ImageFilter

# # Set the scope for the Vision API
# SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# # Authenticate using OAuth for Google Cloud Vision API
# def authenticate_via_oauth():
#     creds = None
#     if os.path.exists('token.json'):
#         from google.oauth2.credentials import Credentials
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 r'A:\Christ University\Sudheer\Hackathon\credentials.json', SCOPES)
#             creds = flow.run_local_server(port=8080)
        
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     return creds

# # Preprocess the image
# def preprocess_image(image):
#     # Enhance contrast and sharpness
#     enhancer = ImageEnhance.Contrast(image)
#     image = enhancer.enhance(2.0)

#     enhancer = ImageEnhance.Sharpness(image)
#     image = enhancer.enhance(2.0)

#     # Convert to grayscale
#     image = image.convert('L')

#     # Apply Gaussian blur to reduce noise
#     image = image.filter(ImageFilter.GaussianBlur(radius=1))

#     return image

# # Detect text using Google Vision API
# def detect_text(client, image):
#     # Convert image to bytes for Google Vision API
#     image_byte_array = io.BytesIO()
#     image.save(image_byte_array, format='PNG')
#     content = image_byte_array.getvalue()

#     image = vision.Image(content=content)
    
#     # Perform document text detection
#     response = client.document_text_detection(
#         image=image,
#         image_context={"language_hints": ["kn"]}  # Kannada language hint
#     )

#     return response

# # Extract the recognized text
# def extract_text(response):
#     full_text = response.full_text_annotation.text
#     cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
#     return cleaned_text

# # Main function to handle the OCR
# def google_vision_ocr(image):
#     creds = authenticate_via_oauth()
#     client = vision.ImageAnnotatorClient(credentials=creds)
    
#     # Preprocess the image for better OCR accuracy
#     preprocessed_image = preprocess_image(image)
    
#     # Detect text from the preprocessed image
#     response = detect_text(client, preprocessed_image)
    
#     # Extract text from the response
#     recognized_text = extract_text(response)
    
#     return recognized_text

# # Streamlit app starts here
# def main():
#     st.title("Image to Text Converter")

#     # Step 1: Allow user to upload a JPG or PNG image
#     uploaded_file = st.file_uploader("Choose a JPEG or PNG file", type=["jpg", "jpeg", "png"])
    
#     if uploaded_file is not None:
#         # Open and display the uploaded image
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Image", use_column_width=True)

#         # Step 2: Extract text using OCR
#         st.write("Performing OCR on the uploaded image...")
#         recognized_text = google_vision_ocr(image)
#         st.write("Recognized Text:")
#         st.text(recognized_text)

#         # Step 3: Save the text to a .txt file using UTF-8 encoding
#         txt_file = "recognized_text.txt"
#         with open(txt_file, "w", encoding="utf-8") as f:
#             f.write(recognized_text)

#         # Step 4: Allow the user to download the .txt file
#         with open(txt_file, "rb") as file:
#             btn = st.download_button(
#                 label="Download Recognized Text",
#                 data=file,
#                 file_name="recognized_text.txt",
#                 mime="text/plain"
#             )

# if __name__ == "__main__":
#     main()




















import os
import io
import re
import streamlit as st
from google.cloud import vision
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from PIL import Image, ImageEnhance, ImageFilter

# Set the scope for the Vision API
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Authenticate using OAuth for Google Cloud Vision API
def authenticate_via_oauth():
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# Preprocess the image
def preprocess_image(image):
    # Enhance contrast and sharpness
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    # Convert to grayscale
    image = image.convert('L')

    # Apply Gaussian blur to reduce noise
    image = image.filter(ImageFilter.GaussianBlur(radius=1))

    return image

# Detect text using Google Vision API
def detect_text(client, image):
    # Convert image to bytes for Google Vision API
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='PNG')
    content = image_byte_array.getvalue()

    image = vision.Image(content=content)
    
    # Perform document text detection
    response = client.document_text_detection(
        image=image,
        image_context={"language_hints": ["kn"]}  # Kannada language hint
    )

    return response

# Extract the recognized text
def extract_text(response):
    full_text = response.full_text_annotation.text

    # Format the text while maintaining spacing and newlines
    formatted_text = "\n".join(line.strip() for line in full_text.splitlines() if line.strip())

    return formatted_text

# Perform OCR on a single image
def google_vision_ocr(client, image):
    # Preprocess the image for better OCR accuracy
    preprocessed_image = preprocess_image(image)
    
    # Detect text from the preprocessed image
    response = detect_text(client, preprocessed_image)
    
    # Extract text from the response
    recognized_text = extract_text(response)
    
    return recognized_text

# Search for keywords or phrases in the text
def search_text(text, search_query):
    # Convert both text and query to lowercase for case-insensitive search
    text_lower = text.lower()
    query_lower = search_query.lower()
    
    # Find all occurrences of the search query
    matches = list(re.finditer(re.escape(query_lower), text_lower))
    
    return matches

# Streamlit app starts here
def main():
    st.title("Handwritten Corpus Search System")

    # Authenticate and create Vision API client
    creds = authenticate_via_oauth()
    client = vision.ImageAnnotatorClient(credentials=creds)

    # Step 1: Allow user to upload multiple JPG or PNG images
    uploaded_files = st.file_uploader("Choose JPEG or PNG files", 
                                      type=["jpg", "jpeg", "png"], 
                                      accept_multiple_files=True,
                                      key="document_uploader")
    
    if uploaded_files:
        # Create a dictionary to store recognized text for each file
        corpus = {}

        # Create columns for image preview
        cols = st.columns(3)  # Adjust the number of columns as needed
        col_index = 0

        for uploaded_file in uploaded_files:
            # Open the uploaded image
            image = Image.open(uploaded_file)
            
            # Preview the image
            with cols[col_index]:
                st.image(image, caption=uploaded_file.name, use_column_width=True)
                col_index = (col_index + 1) % 3  # Cycle through columns
            
            # Perform OCR on the image
            st.write(f"Performing OCR on {uploaded_file.name}...")
            recognized_text = google_vision_ocr(client, image)

            # Store the recognized text in the corpus dictionary
            corpus[uploaded_file.name] = recognized_text
            
            # Display recognized text in a transparent container
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 5px;">
                        <h5>Recognized Text from {uploaded_file.name}:</h5>
                        <pre style="white-space: pre-wrap; word-break: break-word;">{recognized_text}</pre>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

        # Display summary of processed files
        st.write(f"Processed {len(corpus)} files.")

        # Step 2: Save the entire corpus to a single .txt file
        corpus_text = "\n\n".join([f"--- {filename} ---\n{text}" for filename, text in corpus.items()])
        corpus_file = "handwritten_corpus.txt"
        with open(corpus_file, "w", encoding="utf-8") as f:
            f.write(corpus_text)

        # Allow the user to download the corpus .txt file
        with open(corpus_file, "rb") as file:
            st.download_button(
                label="Download Entire Corpus",
                data=file,
                file_name="handwritten_corpus.txt",
                mime="text/plain",
                key="download_corpus"
            )

        # Step 3: Implement keyword search functionality
        st.write("Search for keywords or phrases across the entire corpus:")
        search_query = st.text_input("Enter your search query:", key="search_input")
        
        if search_query:
            all_matches = []
            for filename, text in corpus.items():
                matches = search_text(text, search_query)
                all_matches.extend([(filename, match) for match in matches])
            
            if all_matches:
                st.write(f"Found {len(all_matches)} matches for '{search_query}' across {len(set(match[0] for match in all_matches))} documents:")
                for i, (filename, match) in enumerate(all_matches, 1):
                    start = max(0, match.start() - 20)
                    end = min(len(corpus[filename]), match.end() + 20)
                    context = corpus[filename][start:end]
                    
                    # Highlight the search query in red
                    highlighted_context = (
                        context[:match.start() - start] +
                        f'<span style="color: red;">{context[match.start() - start:match.end() - start]}</span>' +
                        context[match.end() - start:]
                    )
                    
                    st.markdown(f"{i}. In {filename}: ...{highlighted_context}...", unsafe_allow_html=True)

                # Step 4: Visualize search results
                st.write("Document-wise search result distribution:")
                doc_counts = {filename: sum(1 for m in all_matches if m[0] == filename) for filename in corpus.keys()}
                st.bar_chart(doc_counts)
            else:
                st.write(f"No matches found for '{search_query}' in any document.")

if __name__ == "__main__":
    main()
























# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
# import os

# # Set the TESSDATA_PREFIX environment variable
# os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# # Set the Tesseract OCR executable path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def preprocess_image(image_path):
#     """Preprocess the image to enhance OCR accuracy."""
#     image = Image.open(image_path)

#     # Convert to grayscale
#     image = image.convert('L')

#     # Apply adaptive thresholding
#     image = image.point(lambda x: 0 if x < 128 else 255, '1')

#     # Enhance contrast
#     enhancer = ImageEnhance.Contrast(image.convert('RGB'))  # Convert to RGB for enhancement
#     image = enhancer.enhance(2.0)

#     # Resize the image if it's small
#     width, height = image.size
#     if width < 1000 or height < 1000:
#         scale_factor = 1000 / min(width, height)
#         new_width = int(width * scale_factor)
#         new_height = int(height * scale_factor)
#         image = image.resize((new_width, new_height), Image.LANCZOS)

#     return image

# # Load and preprocess the image
# image_path = r'A:\Christ University\Sudheer\Hackathon\OIP.jpg'  # Replace with your image path
# processed_image = preprocess_image(image_path)

# # Use Tesseract to extract text
# recognized_text = pytesseract.image_to_string(processed_image, lang='kan')  # Use 'kan' for Kannada

# print("Recognized Text:")
# print(recognized_text)
