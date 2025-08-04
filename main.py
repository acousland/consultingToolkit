import openai
import streamlit as st
import pandas as pd
from app_config import model
from navigation import PAGE_ROUTES

# Configure Streamlit page settings - must be first Streamlit command
st.set_page_config(
    page_title="Consulting Toolkit",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ensure the OpenAI API key is configured only once
if not openai.api_key:
    openai.api_key = st.secrets.get("OPENAI_API_KEY")

# Initialise session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown("# Consulting Toolkit", unsafe_allow_html=False, help=None)

# Hide the sidebar completely
st.markdown(
    """
<style>
    .css-1d391kg {display: none}
    .st-emotion-cache-1d391kg {display: none}
    [data-testid="stSidebar"] {display: none}
    [data-testid="collapsedControl"] {display: none}
</style>
""",
    unsafe_allow_html=True,
)

# Page routing based on session state only
route_func = PAGE_ROUTES.get(st.session_state.page)
if route_func is None:
    route_func = PAGE_ROUTES["Home"]
route_func()
