import streamlit as st
import pandas as pd
import base64
import PyPDF2

# Retrieve the maximum upload size from the configuration file
max_upload_size_mb = st.get_option("server.maxUploadSize")

# Function to merge CSV files
def merge_csv_files(files):
    dfs = [pd.read_csv(file) for file in files]
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

# Function to merge XLSX files
def merge_xlsx_files(files):
    dfs = [pd.read_excel(file, engine='openpyxl') for file in files]
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

# Function to merge PDF files
def merge_pdf_files(files):
    pdf_merger = PyPDF2.PdfMerger()
    for file in files:
        pdf_merger.append(file)
    merged_pdf = pdf_merger.write('merged_file.pdf')

    # Return the merged PDF file
    return merged_pdf

# Function to merge CSV with Excel
def merge_csv_excel(files):
    # Merge CSV files
    merged_csv = merge_csv_files(files)

    # Merge Excel files
    merged_excel = merge_xlsx_files(files)

    # Combine CSV and Excel dataframes
    merged_df = pd.concat([merged_csv, merged_excel], ignore_index=True)
    return merged_df

# Function to merge PDF with CSV
def merge_pdf_csv(files):
    # Merge PDF files
    merged_pdf = merge_pdf_files(files)

    # Read CSV files into a DataFrame
    dfs = [pd.read_csv(file) for file in files if file.name.endswith('.csv')]
    merged_csv = pd.concat(dfs, ignore_index=True)

    # Convert PDF to DataFrame (placeholder)
    # Implement this part if required
    merged_pdf_df = pd.read_pdf(merged_pdf)

    # Combine PDF and CSV dataframes (placeholder)
    # Implement this part if required
    merged_df = pd.concat([merged_pdf_df, merged_csv], ignore_index=True)
    return merged_csv

# Function to merge PDF with Excel
def merge_pdf_excel(files):
    # Merge PDF files
    merged_pdf = merge_pdf_files(files)

    # Read Excel files into a DataFrame
    dfs = [pd.read_excel(file, engine='openpyxl') for file in files if file.name.endswith(('.xls', '.xlsx'))]
    merged_excel = pd.concat(dfs, ignore_index=True)

    # Convert PDF to DataFrame (placeholder)
    # Implement this part if required
    # merged_pdf_df = pd.read_pdf(merged_pdf)

    # Combine PDF and Excel dataframes (placeholder)
    # Implement this part if required
    # merged_df = pd.concat([merged_pdf_df, merged_excel], ignore_index=True)
    return merged_excel

# Retrieve user uploaded files and perform merging
def merge_files(uploaded_files):
    filenames = [file.name for file in uploaded_files]

    # Identify file types
    file_types = set([filename.split('.')[-1].lower() for filename in filenames])

    # Perform merging based on file types
    if len(file_types) == 1:
        file_type = file_types.pop()
        if file_type == 'csv':
            merged_df = merge_csv_files(uploaded_files)
        elif file_type in ('xls', 'xlsx'):
            merged_df = merge_xlsx_files(uploaded_files)
        elif file_type == 'pdf':
            merged_df = merge_pdf_files(uploaded_files)
        else:
            st.error("Unsupported file type.")
            merged_df = None
    elif len(file_types) == 2:
        if 'csv' in file_types and ('xls' in file_types or 'xlsx' in file_types):
            merged_df = merge_csv_excel(uploaded_files)
        elif 'pdf' in file_types and 'csv' in file_types:
            merged_df = merge_pdf_csv(uploaded_files)
        elif 'pdf' in file_types and ('xls' in file_types or 'xlsx' in file_types):
            merged_df = merge_pdf_excel(uploaded_files)
        else:
            st.error("Unsupported combination of file types.")
            merged_df = None
    else:
        st.error("Unsupported combination of file types.")
        merged_df = None

    return merged_df

# Main function to run Streamlit app
def main():
    st.title("File Merger App")

    # Upload files
    uploaded_files = st.file_uploader("Upload files to merge", accept_multiple_files=True)

    # Perform merging if files uploaded
    if uploaded_files:
        st.write("## Uploaded Files:")
        filenames = [file.name for file in uploaded_files]
        st.write(filenames)
        
        # Merge files
        merged_df = merge_files(uploaded_files)

        # Display merged data
        if merged_df is not None:
            st.write("## Merged Data:")
            st.dataframe(merged_df)

            # Provide download link for CSV
            csv = merged_df.to_csv(index=False).encode()
            b64 = base64.b64encode(csv).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
