import streamlit as st

def engagement_planning_toolkit_page():
    # Breadcrumb navigation as a single line with clickable elements
    breadcrumb_container = st.container()
    
    with breadcrumb_container:
        col1, col2, col3, col4, col5 = st.columns([1, 0.3, 1, 0.3, 1])
        
        with col1:
            if st.button("🏠 Home", key="nav_home_ep", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
        
        with col2:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>→</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div style='background-color: #e6f3ff; padding: 8px; border-radius: 4px; text-align: center;'><strong>📅 Engagement Planning Toolkit</strong></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Toolkit Overview
    st.markdown("# 📅 Engagement Planning Toolkit")
    st.markdown("**Plan and structure client engagements with precision and professionalism**")
    
    st.markdown("""
    The Engagement Planning Toolkit helps consultants design comprehensive engagement approaches, 
    plan meaningful touchpoints, and structure effective client communication strategies. Whether you're 
    planning a discovery phase, stakeholder engagement sequence, or ongoing project communications, 
    these tools provide the framework for successful client interactions.
    """)
    
    st.markdown("---")
    
    # Tool Selection
    st.markdown("## 🛠️ Available Tools")
    
    # Tool 1: Engagement Touchpoint Planning
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 1. 📞 Engagement Touchpoint Planning")
            st.markdown("""
            Plan and structure client touchpoints throughout your engagement. Define communication 
            cadences, stakeholder interactions, and milestone check-ins to ensure consistent 
            client engagement and project success.
            
            **Perfect for:** Engagement managers, project leads, and consultants planning client 
            communication strategies and stakeholder management approaches.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_touchpoint_planning", use_container_width=True, type="primary"):
                st.session_state.page = "Engagement Touchpoint Planning"
                st.rerun()
    
    st.markdown("---")
    
    # Cross-navigation to other toolkits
    st.markdown("## 🔗 Explore Other Toolkits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Pain Point Toolkit", key="nav_to_pain_point_ep", use_container_width=True):
            st.session_state.page = "Pain Point Toolkit"
            st.rerun()
    
    with col2:
        if st.button("📝 Capability Toolkit", key="nav_to_capability_ep", use_container_width=True):
            st.session_state.page = "Capability Toolkit"
            st.rerun()
    
    with col3:
        if st.button("🏗️ Applications Toolkit", key="nav_to_applications_ep", use_container_width=True):
            st.session_state.page = "Applications Toolkit"
            st.rerun()
