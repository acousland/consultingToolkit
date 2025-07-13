import streamlit as st

def theme_creation_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_theme"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point theme creation")
    st.info("This tab will allow you to generate pain point themes (Feature coming soon)")
