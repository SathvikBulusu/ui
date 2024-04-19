import streamlit as st 
import pandas as pd 

# Retrieve the maximum upload size from the configuration file
max_upload_size_mb = st.get_option("server.maxUploadSize")

st.write(""" # Just a UI  
         
         This app just showcases files """)

st.sidebar.header('User Input Parameters')

def user_input_features():

    accept_file_types = ['csv', 'xls', 'xlsx']
    total_size_mb = 0  # Variable to track total size of uploaded files

    up_files = st.sidebar.file_uploader("Upload up to 6 files", accept_multiple_files=True, type=['csv', 'xls', 'xlsx'])

    uploaded_file_names = []  # List to store uploaded file names

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
                    uploaded_file_names.append(filename)  # Store filename

    return uploaded_file_names

uploaded_file_names = user_input_features()

# Display uploaded file names
if uploaded_file_names:
    st.write("## Uploaded Files:")
    for filename in uploaded_file_names:
        st.write(filename)
