Overview
This application allows users to upload images of handwritten Kannada text and perform Optical Character Recognition (OCR) using the Google Cloud Vision API. Users can also search for specific keywords or phrases within the recognized text.

These are the commads to be run by the user before running the application

Prerequisites
python 3.7 or later should be installed in the system
pip also should be installed-pip comes by default after 3.4 when python is installed
A Google Cloud account with the Vision API enabled.
OAuth 2.0 credentials (client secret JSON file) downloaded from your Google Cloud Console.

This is for windows
Clone the Repository
git clone <repository_url>
cd <repository_directory>

Create a Virtual Environment (Optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

install nesscary packages
pip install google-cloud-vision google-auth google-auth-oauthlib streamlit pillow

alternative commads to setup packages:
pip install streamlit
pip install google-cloud-vision
pip install opencv-python
pip install Pillow
pip install matplotlib


Set Up Google Cloud Vision API

Place your credentials.json file in the project directory.
Authenticate using OAuth by running:
python -c "from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/cloud-platform']); flow.run_local_server(port=8080)"


After Completing all the setup process run the app using:
python -m streamlit run filename.py


 
