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
    
    # Tool 2: Application Categorization
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 2. 📊 Application Categorisation")
            st.markdown("""
            Automatically categorise your software portfolio into Application, Technology, or Platform classifications.
            
            • Upload Excel/CSV files with application portfolio data
            • Select ID columns and descriptive text columns
            • AI categorises each item using enterprise architecture principles
            • Configurable batch processing for large portfolios
            • Clear definitions for Application, Technology, and Platform categories
            • Download structured categorisation results for portfolio analysis
            
            **Perfect for:** Enterprise architects, technology portfolio managers, and consultants conducting 
            application portfolio assessments and technology landscape analysis.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_app_categorization", use_container_width=True, type="primary"):
                st.session_state.page = "Application Categorisation"
                st.rerun()
    
    st.markdown("---")
    
    # Tool 3: Individual Application to Capability Mapping
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 3. 🎯 Individual Application to Capability Mapping")
            st.markdown("""
            Map a single application to your capability framework with detailed AI analysis.
            
            • Upload your capability framework Excel file
            • Select capability ID and description columns
            • Enter application name and detailed description
            • AI provides capability mappings with confidence levels
            • Detailed analysis with primary, secondary, and potential capability matches
            • No download required - results displayed immediately on page
            
            **Perfect for:** Solution architects, business analysts, and consultants conducting 
            individual application assessments and targeted capability analysis.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_individual_app_mapping", use_container_width=True, type="primary"):
                st.session_state.page = "Individual Application to Capability Mapping"
                st.rerun()
    
    st.markdown("---")
    
    # Cross-navigation to other toolkits
    st.markdown("## 🔗 Explore Other Toolkits")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Pain Point Toolkit", key="nav_pain_point", use_container_width=True):
            st.session_state.page = "Pain Point Toolkit"
            st.rerun()
    
    with col2:
        if st.button("📝 Capability Toolkit", key="nav_capability", use_container_width=True):
            st.session_state.page = "Capability Toolkit"
            st.rerun()
    
    with col3:
        if st.button("📅 Engagement Planning Toolkit", key="nav_engagement", use_container_width=True):
            st.session_state.page = "Engagement Planning Toolkit"
            st.rerun()
    
    with col4:
        if st.button("🎯 Strategy & Motivations Toolkit", key="nav_strategy", use_container_width=True):
            st.session_state.page = "Strategy and Motivations Toolkit"
            st.rerun()
    
