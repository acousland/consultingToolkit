import streamlit as st

def applications_toolkit_page():
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
            st.markdown("**🏗️ Applications Toolkit**")
    
    st.markdown("---")
    
    st.markdown("# 🏗️ Applications Toolkit")

    st.markdown("""
    The Applications Toolkit provides tools for understanding and mapping your organisation's technology landscape. 
    Use these tools to connect applications with business capabilities and assess technology alignment with strategic objectives.
    """)
    
    st.markdown("---")
    
    # Tool Selection
    st.markdown("## 🛠️ Available Tools")
    
    # Tool 1: Application to Capability Mapping
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 1. 🔗 Application to Capability Mapping")
            st.markdown("""
            Map applications to organisational capabilities for technology landscape analysis.
            
            • Upload Excel/CSV files with application and capability data
            • Select ID columns and descriptive text columns
            • AI matches each application to the most relevant business capabilities
            • Configurable batch processing for large application portfolios
            • Results include application IDs mapped to capability IDs with confidence ratings
            • Download comprehensive mapping results for architecture planning
            
            **Perfect for:** Technology architects, enterprise architects, and consultants conducting 
            application portfolio analysis and capability mapping exercises.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_app_capability_mapping", use_container_width=True, type="primary"):
                st.session_state.page = "Application to Capability Mapping"
                st.rerun()
    
    st.markdown("---")
    
