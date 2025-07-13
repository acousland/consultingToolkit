import streamlit as st

def home_page():
    st.markdown("## Welcome to the Consulting Toolkit")
    st.markdown("_AI-powered pain point analysis tool_")
    
    st.markdown("---")
    
    st.markdown("### Getting Started")
    st.markdown("This toolkit helps you analyze organizational pain points and map them to capabilities. Choose from the available tools below:")
    
    # Create columns for a nice layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 **Pain Point Extraction**")
        st.markdown("Upload and analyze documents to extract specific organizational pain points.")
        if st.button("Go to Pain Point Extraction", key="pain_extraction", use_container_width=True):
            st.session_state.page = "Pain Point Extraction"
            st.rerun()
        
        st.markdown("#### 🎯 **Capability Mapping**")
        st.markdown("Map extracted pain points to organizational capabilities.")
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
    
    st.markdown("### How to Use")
    st.markdown("""
    1. **Start with Pain Point Extraction** - Upload your documents and extract pain points
    2. **Create Themes** - Group related pain points into meaningful themes
    3. **Map to Capabilities** - Connect pain points to organizational capabilities
    4. **Generate Descriptions** - Create detailed capability descriptions
    """)
    
    st.markdown("### Tips")
    st.info("💡 For best results, start with the Pain Point Extraction tool and work through the process sequentially.")
