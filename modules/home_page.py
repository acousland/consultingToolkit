import streamlit as st

def home_page():
    st.markdown("# Welcome to the Consulting Toolkit")
    st.markdown("_Tools for making your consulting life easier_")
    
    st.markdown("---")
    
    st.markdown("## Getting Started")
    st.markdown("""
    This consulting toolkit is organised into two specialised toolkits, each designed to address specific aspects 
    of organisational analysis and capability development. Choose the toolkit that matches your current consulting needs.
    """)
    
    st.markdown("---")
    
    # Two large toolkit buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        # Pain Point Toolkit Overview
        st.markdown("## 🔍 **Pain Point Toolkit**")
        st.markdown("_Identify, categorise, and map organisational challenges_")
        
        st.markdown("""
        **Perfect for:** Consultants analysing organisational challenges, extracting insights from qualitative data, 
        and connecting problems to solution capabilities.
        
        **Tools included:**
        • Pain Point Extraction
        • Theme & Perspective Mapping  
        • Capability Mapping
        
        **Typical workflow:** Extract → Categorise → Map to Capabilities
        """)
        
        if st.button("Enter Pain Point Toolkit", key="enter_pain_point_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Pain Point Toolkit"
            st.rerun()
    
    with col2:
        # Capability Toolkit Overview
        st.markdown("## 📝 **Capability Toolkit**")
        st.markdown("_Design and refine organisational capabilities_")
        
        st.markdown("""
        **Perfect for:** Consultants building capability frameworks, refining capability descriptions, 
        and ensuring consistent professional language across strategic documents.
        
        **Tools included:**
        • Capability Description Generation
        
        **Typical workflow:** Generate Professional Descriptions → Integrate with Strategic Planning
        """)
        
        if st.button("Enter Capability Toolkit", key="enter_capability_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Capability Toolkit"
            st.rerun()
    
    st.markdown("---")
