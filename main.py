
import openai
import streamlit as st
import pandas as pd
import math
from modules.home_page import home_page
from modules.pain_point_toolkit_page import pain_point_toolkit_page
from modules.capability_toolkit_page import capability_toolkit_page
from modules.pain_point_extraction_page import pain_point_extraction_page
from modules.capability_mapping_page import capability_mapping_page
from modules.theme_creation_page import theme_creation_page
from modules.capability_description_page import capability_description_page
from app_config import model


if openai.api_key not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialise session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

st.markdown("# Consulting Toolkit", unsafe_allow_html=False, help=None)

# Hide the sidebar completely
st.markdown("""
<style>
    .css-1d391kg {display: none}
    .st-emotion-cache-1d391kg {display: none}
    [data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
</style>
""", unsafe_allow_html=True)

# Page routing based on session state only
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Pain Point Toolkit":
    pain_point_toolkit_page()
elif st.session_state.page == "Capability Toolkit":
    capability_toolkit_page()
elif st.session_state.page == "Pain Point Extraction":
    pain_point_extraction_page()
elif st.session_state.page == "Pain Point Theme Creation":
    theme_creation_page()
elif st.session_state.page == "Pain Point to Capability Mapping":
    capability_mapping_page()
elif st.session_state.page == "Capability Description Generation":
    capability_description_page()