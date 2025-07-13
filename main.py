
import openai
import streamlit as st
import pandas as pd
import math
from modules.home_page import home_page
from modules.pain_point_extraction_page import pain_point_extraction_page
from modules.capability_mapping_page import capability_mapping_page
from modules.theme_creation_page import theme_creation_page
from modules.capability_description_page import capability_description_page
from app_config import prompt, model, output_parser


if openai.api_key not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

st.markdown("# Consulting Toolkit", unsafe_allow_html=False, help=None)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "Home",
        "Pain Point Extraction",
        "Pain Point Theme Creation", 
        "Pain Point to Capability Mapping",
        "Capability Description Generation"
    ],
    index=["Home", "Pain Point Extraction", "Pain Point Theme Creation", 
           "Pain Point to Capability Mapping", "Capability Description Generation"].index(st.session_state.page)
)

# Update session state when dropdown changes
if page != st.session_state.page:
    st.session_state.page = page

# Page routing
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Pain Point Extraction":
    pain_point_extraction_page()
elif st.session_state.page == "Pain Point Theme Creation":
    theme_creation_page()
elif st.session_state.page == "Pain Point to Capability Mapping":
    capability_mapping_page()
elif st.session_state.page == "Capability Description Generation":
    capability_description_page()