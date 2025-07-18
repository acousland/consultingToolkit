import streamlit as st
from navigation import render_breadcrumbs

def capability_toolkit_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("📝 Capability Toolkit", None)])
    
    st.markdown("# 📝 Capability Toolkit")

    st.markdown("""
    The Capability Toolkit focuses on designing and refining organisational capability frameworks. 
    Use these tools to create professional, consistent capability descriptions that integrate seamlessly with your strategic planning processes.
    """)
    
    st.markdown("---")
    
    # Tool Selection
    st.markdown("## 🛠️ Available Tools")
    
    # Tool 1: Capability Description Generation
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 1. 📝 Capability Description Generation")
            st.markdown("""
            Generate professional capability descriptions using AI-powered writing.
            
            • Upload capability names and existing descriptions
            • AI creates polished, single-sentence capability descriptions
            • Australian English with active voice and professional tone
            • Consistent style with varied, sophisticated vocabulary
            • Track capability IDs for easy integration with other systems
            • Export professionally formatted descriptions as Excel
            
            **Perfect for:** Strategy consultants, business analysts, and capability architects 
            developing professional capability frameworks and strategic documentation.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_capability_desc", use_container_width=True, type="primary"):
                st.session_state.page = "Capability Description Generation"
                st.rerun()
    
    st.markdown("---")
    