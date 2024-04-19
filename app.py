import streamlit as st 
import pandas as pd 

st.write(""" # Just a UI  
         
         This app just showcases files """)

st.sidebar.header('User Input Parameters')

def user_input_features():

    num_files = 6 
    uploaded_datasets=[]
    accept_file_types = ['csv', 'xls', 'xlsx']
    up_files = st.sidebar.file_uploader("Upload up to 6 files", accept_multiple_files=True, type=['csv', 'xls', 'xlsx'])

    if up_files is not None:
        if len(up_files) > num_files:
            st.sidebar.error(f"Maximum file capacity reached. You have selected {len(up_files)} files.")
            up_files = up_files[:num_files]

        for up_file in up_files:
            if up_file is not None:
                filename = up_file.name
                file_extension = filename.split('.')[-1].lower()
                if file_extension not in accept_file_types:
                    st.sidebar.error(f"File '{filename}' is not supported. Upload accepted file types: {', '.join(accept_file_types)}")
                else:
                    if file_extension == 'csv':
                        df = pd.read_csv(up_file)
                    elif file_extension in ['xls', 'xlsx']:
                        df = pd.read_excel(up_file)
                    uploaded_datasets.append((filename,df))

    return uploaded_datasets

uploaded_datasets = user_input_features()

for filename,df in uploaded_datasets:
    st.write(f"##{filename}")
    st.dataframe(df)
