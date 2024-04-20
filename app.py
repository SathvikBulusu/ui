import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build  
from googleapiclient.http import MediaIoBaseUpload  # Import MediaIoBaseUpload
import io  # Import io module for byte I/O support
import pandas as pd 


creds = service_account.Credentials.from_service_account_file(r'D:\bots.json',scopes=['https://www.googleapis.com/auth/drive'])

drive_service = build('drive','v3',credentials=creds)

# Retrieve the maximum upload size from the configuration file
max_upload_size_mb = st.get_option("server.maxUploadSize")

st.write(""" # Just a UI  
         
         This app just showcases files """)

st.sidebar.header('User Input Parameters')

def user_input_features():

    accept_file_types = ['csv', 'xls', 'xlsx']
    total_size_mb = 0  # Variable to track total size of uploaded files

    up_files = st.sidebar.file_uploader("Upload up to 6 files", accept_multiple_files=True, type=['csv', 'xls', 'xlsx'])

    uploaded_files_metadata = []  # List to store uploaded file metadata

    if up_files is not None:
        for up_file in up_files:
            if up_file is not None:
                filename = up_file.name
                file_extension = filename.split('.')[-1].lower()
                if file_extension not in accept_file_types:
                    st.sidebar.warning(f"File '{filename}' is not supported. Upload accepted file types: {', '.join(accept_file_types)}")
                else:
                    file_size_mb = len(up_file.getvalue()) / (1024 * 1024)  # Calculate file size in MB
                    total_size_mb += file_size_mb  # Update total size
                    if total_size_mb > max_upload_size_mb:
                        st.sidebar.warning(f"Maximum total size of uploaded files reached. You have exceeded {max_upload_size_mb} MB.")
                        break

                    # Create a media upload object for the file content
                    media = MediaIoBaseUpload(io.BytesIO(up_file.getvalue()), mimetype=up_file.type, resumable=True)

                    # Upload file to Google Drive
                    file_metadata = {
                        'name': filename,
                        # 'parents': [folder_id],  # Optionally specify folder ID if you want to save files in a specific folder
                    }
                    media = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                    # Store file metadata
                    uploaded_files_metadata.append({
                        'name': filename,
                        'id': media.get('id')
                    })

    return uploaded_files_metadata

uploaded_files_metadata = user_input_features()

# Display uploaded file names and their corresponding Google Drive IDs
if uploaded_files_metadata:
    st.write("## Uploaded Files:")
    for file_metadata in uploaded_files_metadata:
        st.write(f"Name: {file_metadata['name']}, ID: {file_metadata['id']}")
