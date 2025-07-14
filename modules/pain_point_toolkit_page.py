import streamlit as st

def pain_point_toolkit_page():
    # Breadcrumb navigation as a single line with clickable elements
    breadcrumb_container = st.container()
    
    with breadcrumb_container:
        col1, col2, col3 = st.columns([1.2, 0.2, 4])
        
        with col1:
            if st.button("🏠 Home", key="breadcrumb_home", help="Go to Home"):
                st.session_state.page = "Home"
                st.rerun()
        
        with col2:
            st.markdown("**›**")
        
        with col3:
            st.markdown("**🔍 Pain Point Toolkit**")
    
    st.markdown("---")
    
    st.markdown("# 🔍 Pain Point Toolkit")
    st.markdown("_Identify, categorise, and map organisational challenges_")
    
    st.markdown("---")
    
    st.markdown("### Overview")
    st.markdown("""
    The Pain Point Toolkit provides a comprehensive workflow for extracting, categorising, and mapping organisational challenges. 
    Use these tools in sequence to transform raw qualitative data into actionable insights for strategic planning.
    """)
    
    st.markdown("---")
    
    # Tool 1: Pain Point Extraction
    st.markdown("## 🔍 **1. Pain Point Extraction**")
    st.markdown("""
    **Extract organisational pain points from text data with AI analysis.**
    
    • Upload Excel/CSV files with qualitative data
    • Select multiple columns for comprehensive analysis  
    • AI processes data in chunks to handle large datasets
    • Returns clean, single-sentence pain points ready for analysis
    • Download results as Excel for further processing
    """)
    if st.button("Go to Pain Point Extraction", key="pain_extraction", use_container_width=True):
        st.session_state.page = "Pain Point Extraction"
        st.rerun()
    
    st.markdown("---")
    
    # Tool 2: Theme Creation  
    st.markdown("## 🗂️ **2. Theme & Perspective Mapping**")
    st.markdown("""
    **Categorise pain points into predefined themes and organisational perspectives.**
    
    • Upload pain points with ID and description columns
    • AI maps each pain point to 20 predefined themes (e.g., Technology Limitations, Manual Processes)
    • AI assigns organisational perspectives (Process, People, Technology, etc.)
    • Batch processing for efficient analysis of large datasets
    • Distribution analytics show theme and perspective breakdowns
    • Download comprehensive mapping results as Excel
    """)
    if st.button("Go to Theme & Perspective Mapping", key="theme_creation", use_container_width=True):
        st.session_state.page = "Pain Point Theme Creation"
        st.rerun()
    
    st.markdown("---")
    
    # Tool 3: Capability Mapping
    st.markdown("## 🎯 **3. Capability Mapping**")
    st.markdown("""
    **Map pain points to organisational capabilities for strategic planning.**
    
    • Upload separate spreadsheets for pain points and capabilities
    • Select ID columns and multiple descriptive text columns
    • AI matches each pain point to the most appropriate capability
    • Batch processing with configurable batch sizes for performance
    • Results include pain point IDs mapped to capability IDs
    • Download mapping table for integration with strategic planning tools
    """)
    if st.button("Go to Capability Mapping", key="capability_mapping", use_container_width=True):
        st.session_state.page = "Pain Point to Capability Mapping"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💡 **Suggested Workflow**")
    st.markdown("""
    1. **Pain Point Extraction** → Extract challenges from qualitative data
    2. **Theme & Perspective Mapping** → Categorise and understand patterns
    3. **Capability Mapping** → Connect pain points with required capabilities
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Main Menu", key="back_to_main_from_pain", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("Go to Capability Toolkit →", key="to_capability_toolkit", use_container_width=True):
            st.session_state.page = "Capability Toolkit"
            st.rerun()
    
    st.markdown("---")
