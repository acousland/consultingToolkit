import streamlit as st

def capability_mapping_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_mapping"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point to Capability Mapping")
    st.info("This tab will allow you to map extracted pain points to organisational capabilities. (Feature coming soon)")
