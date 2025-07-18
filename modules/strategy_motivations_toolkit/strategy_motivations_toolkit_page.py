import streamlit as st
from navigation import render_breadcrumbs

def strategy_motivations_toolkit_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🎯 Strategy and Motivations Toolkit", None)])
    
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
    
    # Tool 2: Initiatives to Strategy Generator
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 2. 📈 Tactics to Strategies Generator")
            st.markdown("""
            Transform tactical initiatives into coherent strategic activities and execution approaches.
            
            • Upload tactical initiatives and projects data from Excel spreadsheets
            • Select initiative ID and multiple description columns
            • AI analyses patterns and identifies strategic activities that tactics deliver
            • Configurable number of strategic activities (3-8 activities)
            • Detailed strategic descriptions, success factors, and risk considerations
            • Download comprehensive strategic analysis with tactics-to-strategies mapping
            
            **Perfect for:** Strategy consultants, transformation leaders, and senior executives 
            developing strategic execution frameworks from existing tactical initiatives and projects.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_initiatives_strategy_generator", use_container_width=True, type="primary"):
                st.session_state.page = "Tactics to Strategies Generator"
                st.rerun()
    
    st.markdown("---")
    