import streamlit as st

def strategy_motivations_toolkit_page():
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
            st.markdown("**🎯 Strategy and Motivations Toolkit**")
    
    st.markdown("---")
    
    # Toolkit Overview
    st.markdown("# 🎯 Strategy and Motivations Toolkit")
    st.markdown("**Connect strategic initiatives with organisational capabilities and motivations**")
    
    st.markdown("""
    The Strategy and Motivations Toolkit helps consultants bridge the gap between high-level strategic 
    objectives and practical implementation through capability mapping. Whether you're analysing strategic 
    initiatives, understanding organisational motivations, or connecting strategy to execution capabilities, 
    these tools provide the framework for strategic alignment and implementation planning.
    """)
    
    st.markdown("---")
    
    # Tool Selection
    st.markdown("## 🛠️ Available Tools")
    
    # Tool 1: Strategy to Capability Mapping
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 1. 🎯 Strategy to Capability Mapping")
            st.markdown("""
            Map strategic initiatives and objectives to required organisational capabilities.
            
            • Upload strategic initiatives and capability frameworks
            • AI matches strategic objectives to supporting capabilities
            • Identify capability gaps for strategic implementation
            • Batch processing for large strategic portfolios
            • Results include strategy IDs mapped to capability requirements
            • Download comprehensive mapping for strategic planning integration
            
            **Perfect for:** Strategy consultants, business architects, and transformation leaders 
            connecting high-level strategy with execution capabilities and implementation planning.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_strategy_capability_mapping", use_container_width=True, type="primary"):
                st.session_state.page = "Strategy to Capability Mapping"
                st.rerun()
    
    st.markdown("---")
    