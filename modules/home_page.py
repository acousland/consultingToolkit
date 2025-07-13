import streamlit as st

def home_page():
    st.markdown("## Welcome to the Consulting Toolkit")
    st.markdown("_Tools for making your consulting life easier_")
    
    st.markdown("---")
    
    st.markdown("### Getting Started")
    st.markdown("This toolkit helps you analyze organisational pain points and map them to capabilities. Choose from the available tools below:")
    
    # Create columns for a nice layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 **Pain Point Extraction**")
        st.markdown("Upload and analyze documents to extract specific organisational pain points.")
        if st.button("Go to Pain Point Extraction", key="pain_extraction", use_container_width=True):
            st.session_state.page = "Pain Point Extraction"
            st.rerun()
        
        st.markdown("#### 🎯 **Capability Mapping**")
        st.markdown("Map extracted pain points to organisational capabilities.")
        if st.button("Go to Capability Mapping", key="capability_mapping", use_container_width=True):
            st.session_state.page = "Pain Point to Capability Mapping"
            st.rerun()
    
    with col2:
        st.markdown("#### 📋 **Theme Creation**")
        st.markdown("Generate themes from your extracted pain points.")
        if st.button("Go to Theme Creation", key="theme_creation", use_container_width=True):
            st.session_state.page = "Pain Point Theme Creation"
            st.rerun()
        
        st.markdown("#### 📝 **Capability Descriptions**")
        st.markdown("Generate detailed descriptions for organizational capabilities.")
        if st.button("Go to Capability Descriptions", key="capability_desc", use_container_width=True):
            st.session_state.page = "Capability Description Generation"
            st.rerun()
    
    st.markdown("---")
