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

steps to create credentials.json file:
Step 1: Create a Google Cloud Project
Visit the Google Cloud Console: Go to Google Cloud Console.
Sign in: Use your Google account to sign in.
Create a New Project:
Click on the project dropdown at the top of the page.
Click on "New Project."
Enter a name for your project and click "Create."
Step 2: Enable the Google Vision API
Navigate to the API Library:
In the left sidebar, click on "APIs & Services" and then select "Library."
Search for the Vision API:
In the library, search for "Vision API."
Enable the API:
Click on "Cloud Vision API" from the search results.
Click the "Enable" button.
Step 3: Create Service Account Credentials
Navigate to Service Accounts:
In the left sidebar, go to "APIs & Services" and then "Credentials."
Create a Service Account:
Click on "Create credentials" and select "Service account."
Enter a name for the service account and click "Create."
Set Permissions (Optional):
You can assign roles to your service account. For basic access, you might assign it the "Viewer" role, but for Vision API usage, consider "Cloud Vision API User."
Click "Continue."
Create Key:
In the service account details, click on "Keys."
Click on "Add Key" and select "JSON." This will download the credentials.json file to your computer.
Step 4: Store the credentials.json File
Move the credentials.json file to the appropriate directory in your project, as referenced in your code 

Set Up Google Cloud Vision API

Place your credentials.json file in the project directory.
Authenticate using OAuth by running:
python -c "from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/cloud-platform']); flow.run_local_server(port=8080)"


After Completing all the setup process run the app using:
python -m streamlit run filename.py


 
