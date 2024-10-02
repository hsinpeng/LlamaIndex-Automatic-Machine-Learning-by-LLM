import time
import streamlit as st
from classification_worker import classification_model_pipeline, decide_model_type
from cluster_worker import cluster_model_pipeline
from regression_worker import regression_model_pipeline
from visualization_worker import data_visualization_pipeline
from automl.util_general import check_filesize_from_streamlit, read_file_from_streamlit
from st_dev_info import stream_words, developer_info_simple_stream, developer_info_simple_static

APP_TITLE = "LlamaIndex: Naïve Automatic Machine Learning"
AUTHOR = "Sheldon Hsin-Peng Lin"
EMAIL = "hsinpeng168@gmail.com"
GITHUB = "https://github.com/hsinpeng"

st.set_page_config(page_title=APP_TITLE, page_icon=":bar_chart:", layout="wide")

# Introduction section
with st.container():
    st.subheader("Hello user 👋")
    st.title(f":bar_chart: {APP_TITLE}")
    welcome_message = "Just upload your data file, then data analyzing and modeling will be performed automatically!"
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if not st.session_state.initialized:
        st.write(stream_words(welcome_message))
        time.sleep(0.1)
        developer_info_simple_stream(author=AUTHOR, email=EMAIL, github=GITHUB)
        st.session_state.initialized = True
    else:
        st.write(welcome_message)
        developer_info_simple_static(author=AUTHOR, email=EMAIL, github=GITHUB)

# Funtionalities section
with st.container():
    st.divider()
    st.header("Let's Get Started")
    left_column, right_column = st.columns([6, 4])
    with left_column:
        uploaded_file = st.file_uploader("Choose a data file.", accept_multiple_files=False, type=['csv', 'json', 'xls', 'xlsx'])
        if uploaded_file:
            if uploaded_file.getvalue():
                uploaded_file.seek(0)
                if not check_filesize_from_streamlit(uploaded_file):
                    st.error("Size of data file is too large!")
                    st.stop()
                st.session_state.DF_uploaded = read_file_from_streamlit(uploaded_file)
                if st.session_state.DF_uploaded is None:
                    st.session_state.is_file_empty = True
                    st.error("Wrong file type!")
                    st.stop()
                else:
                    st.session_state.is_file_empty = False
            else:
                st.session_state.is_file_empty = True
        
    with right_column:
        MODE = st.selectbox('Select a proper analysis mode', ('Automatic Machine Learning', 'Classification Model', 'Clustering Model', 'Regression Model', 'Data Visualization'))
        st.write(f'Analysis mode: :green[{MODE}]')

    # Proceed Button
    is_proceed_enabled = uploaded_file is not None or uploaded_file is not None and MODE == "Data Visualization"

    # Initialize the 'button_clicked' state
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    if st.button('Start Analysis', disabled=(not is_proceed_enabled) or st.session_state.button_clicked, type="primary"):
        st.session_state.button_clicked = True
    if "is_file_empty" in st.session_state and st.session_state.is_file_empty:
        st.caption('Please upload your data file to continue.')

    # Start Analysis
    if st.session_state.button_clicked:
        with st.container():
            if "DF_uploaded" not in st.session_state:
                st.error("File is empty!")
                st.stop()
            else:
                if MODE == 'Automatic Machine Learning':
                    iDecision = decide_model_type(st.session_state.DF_uploaded)
                    if iDecision == 1:
                        st.subheader('Analysis Mode: Classification Model')
                        classification_model_pipeline(st.session_state.DF_uploaded)
                    elif iDecision == 2:
                        st.subheader('Analysis Mode: Regression Model')           
                        regression_model_pipeline(st.session_state.DF_uploaded)
                    else:
                        st.subheader('Default Mode: Data Visualization')
                        data_visualization_pipeline(st.session_state.DF_uploaded)
                elif MODE == 'Classification Model':
                    classification_model_pipeline(st.session_state.DF_uploaded)
                elif MODE == 'Clustering Model':
                    cluster_model_pipeline(st.session_state.DF_uploaded)
                elif MODE == 'Regression Model':
                    regression_model_pipeline(st.session_state.DF_uploaded)
                elif MODE == 'Data Visualization':
                    data_visualization_pipeline(st.session_state.DF_uploaded)