import streamlit as st 
import pandas as pd 
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Retrieve the maximum upload size from the configuration file
max_upload_size_mb = st.get_option("server.maxUploadSize")


selected = option_menu(
        menu_title=None,
        options=["Merge","Statistics"],
        icons=["clipboard-data-fill","bar-chart-fill","envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    
styles={
        "container": {"padding": "0!important", "background-color": "#FF69B4"},
        "icon": {"color": "purple", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "pink"},
    },
)

def user_input_features():

    accept_file_types = ['csv', 'xls', 'xlsx','ods','pdf']
    total_size_mb = 0  # Variable to track total size of uploaded files

    up_files = st.file_uploader("Upload up to 6 files", accept_multiple_files=True, type=['csv', 'xls', 'xlsx','ods','pdf'])

    uploaded_file_names = []  # List to store uploaded file names

    if up_files is not None:
        for up_file in up_files:
            if up_file is not None:
                filename = up_file.name
                file_extension = filename.split('.')[-1].lower()
                if file_extension not in accept_file_types:
                    st.warning(f"File '{filename}' is not supported. Upload accepted file types: {', '.join(accept_file_types)}")
                else:
                    file_size_mb = len(up_file.getvalue()) / (1024 * 1024)  # Calculate file size in MB
                    total_size_mb += file_size_mb  # Update total size
                    if total_size_mb > max_upload_size_mb:
                        st.warning(f"Maximum total size of uploaded files reached. You have exceeded {max_upload_size_mb} MB.")
                        break
                    uploaded_file_names.append({"Filename": filename, "File size (MB)": file_size_mb, "File type": file_extension})  # Store filename

    return uploaded_file_names

if selected == "Statistics":
        st.title(f"you have chosen to do {selected}")
elif selected == "Merge":
        uploaded_file_names = user_input_features()
        if uploaded_file_names:
            st.write("## Uploaded Files:")
            files_df=pd.DataFrame(uploaded_file_names)
            gd=GridOptionsBuilder.from_dataframe(files_df)
            gd.configure_selection(selection_mode='multiple',use_checkbox=True)
            gf=gd.build()

            #building a table using aggrid 
            g_t = AgGrid(files_df,height=250,gridOptions=gf,update_mode=GridUpdateMode.SELECTION_CHANGED)
            st.write('###selected')
            selected_row = g_t["selected rows"]
            st.dataframe(selected_row)

        ## the conditional statements for the requirements
            if len(uploaded_file_names) ==1:
                 st.error("Merge is not possible")
            else:
                 uploaded_file_names = set (files_df['File type'])
                 unsupported_types=set(files_df['File type']).intersection({'xls','ods','xlsv'})
                 if unsupported_types :
                      st.warning(f"Merging is not supported for files cause {','.join(unsupported_types)}")
                 else:
                    merge_button = st.button("Merge files")
                
             

      