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
    st.markdown("_Map and analyse organisational applications and technology landscape_")
    
    st.markdown("---")
    
    st.markdown("### Overview")
    st.markdown("""
    The Applications Toolkit provides tools for understanding and mapping your organisation's technology landscape. 
    Use these tools to connect applications with business capabilities and assess technology alignment with strategic objectives.
    """)
    
    st.markdown("---")
    
    # Tool 1: Application to Capability Mapping
    st.markdown("## 🔗 **1. Application to Capability Mapping**")
    st.markdown("""
    **Map applications to organisational capabilities for technology landscape analysis.**
    
    • Upload Excel/CSV files with application and capability data
    • Select ID columns and descriptive text columns
    • AI matches each application to the most relevant business capabilities
    • Configurable batch processing for large application portfolios
    • Results include application IDs mapped to capability IDs with confidence ratings
    • Download comprehensive mapping results for architecture planning
    """)
    if st.button("Go to Application to Capability Mapping", key="app_capability_mapping", use_container_width=True):
        st.session_state.page = "Application to Capability Mapping"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💡 **Suggested Workflow**")
    st.markdown("""
    1. **Application to Capability Mapping** → Connect applications with business capabilities
    2. **Future Tools** → Additional application analysis tools coming soon
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("← Back to Main Menu", key="back_to_main_from_apps", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("🔍 Pain Point Toolkit", key="to_pain_point_toolkit", use_container_width=True):
            st.session_state.page = "Pain Point Toolkit"
            st.rerun()
    with col3:
        if st.button("📝 Capability Toolkit", key="to_capability_toolkit", use_container_width=True):
            st.session_state.page = "Capability Toolkit"
            st.rerun()
    with col4:
        if st.button("📅 Engagement Planning", key="to_engagement_toolkit_apps", use_container_width=True):
            st.session_state.page = "Engagement Planning Toolkit"
            st.rerun()
    
    st.markdown("---")
