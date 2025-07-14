import streamlit as st

def engagement_planning_toolkit_page():
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
            st.markdown("**📅 Engagement Planning Toolkit**")
    
    st.markdown("---")
    
    # Toolkit Overview
    st.markdown("# 📅 Engagement Planning Toolkit")
  
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
   