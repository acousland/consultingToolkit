import streamlit as st

def capability_toolkit_page():
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
            st.markdown("**📝 Capability Toolkit**")
    
    st.markdown("---")
    
    st.markdown("# 📝 Capability Toolkit")
    st.markdown("_Design and refine organisational capabilities_")
    
    st.markdown("---")
    
    st.markdown("### Overview")
    st.markdown("""
    The Capability Toolkit focuses on designing and refining organisational capability frameworks. 
    Use these tools to create professional, consistent capability descriptions that integrate seamlessly with your strategic planning processes.
    """)
    
    st.markdown("---")
    
    # Tool 1: Capability Description
    st.markdown("## 📝 **1. Capability Description Generation**")
    st.markdown("""
    **Generate professional capability descriptions using AI-powered writing.**
    
    • Upload capability names and existing descriptions
    • AI creates polished, single-sentence capability descriptions
    • Australian English with active voice and professional tone
    • Consistent style with varied, sophisticated vocabulary
    • Track capability IDs for easy integration with other systems
    • Export professionally formatted descriptions as Excel
    """)
    if st.button("Go to Capability Description Generation", key="capability_desc", use_container_width=True):
        st.session_state.page = "Capability Description Generation"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💡 **Suggested Workflow**")
    st.markdown("""
    1. **Capability Description Generation** → Create professional capability framework descriptions
    2. **Integrate with Pain Point Toolkit** → Map capabilities to organisational challenges
    3. **Export and Apply** → Use refined descriptions in strategic planning documents
    """)
    
    st.markdown("### 🔗 **Integration with Pain Point Toolkit**")
    st.markdown("""
    **Best Results:** Use the Capability Toolkit in conjunction with the Pain Point Toolkit:
    
    • Create capability descriptions here, then use them in **Capability Mapping**
    • Ensure your capability framework aligns with identified organisational challenges
    • Maintain consistent terminology across both toolkits for seamless integration
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("← Back to Main Menu", key="back_to_main_from_capability", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("🔍 Pain Point Toolkit", key="to_pain_point_toolkit", use_container_width=True):
            st.session_state.page = "Pain Point Toolkit"
            st.rerun()
    with col3:
        if st.button("🏗️ Applications Toolkit", key="to_applications_toolkit", use_container_width=True):
            st.session_state.page = "Applications Toolkit"
            st.rerun()
    with col4:
        if st.button("📅 Engagement Planning", key="to_engagement_toolkit_cap", use_container_width=True):
            st.session_state.page = "Engagement Planning Toolkit"
            st.rerun()
    
    st.markdown("---")
