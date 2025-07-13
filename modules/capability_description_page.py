import streamlit as st

def capability_description_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_description"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Capability Description Generation Page")
    st.info("This page will allow you to generate descriptions for a set of capabilities. (Feature coming soon)")
