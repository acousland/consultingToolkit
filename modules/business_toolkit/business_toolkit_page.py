import streamlit as st
from navigation import render_breadcrumbs

def business_toolkit_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🏢 Business Toolkit", None)])
    
    st.markdown("# 🏢 Business Toolkit")

    st.markdown("""
    The Business Toolkit combines comprehensive workflows for analyzing organizational challenges and designing capability frameworks. 
    Use these tools to transform raw qualitative data into actionable strategic insights and create professional capability descriptions.
    """)
    
    st.markdown("---")
    
    # Tool Selection
    st.markdown("## 🛠️ Available Tools")
    
    # Tool 1: Pain Point Extraction
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 1. 🔍 Pain Point Extraction")
            st.markdown("""
            Extract organisational pain points from text data with AI analysis.
            
            • Upload text data from surveys, interviews, or feedback forms
            • AI identifies and extracts specific pain points and challenges
            • Chunked processing to handle large text volumes
            • Results include pain point descriptions and context
            • Download extracted pain points as Excel for further analysis
            
            **Perfect for:** Consultants analysing qualitative feedback, survey responses, 
            and stakeholder interview data to identify organisational challenges.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_pain_extraction", use_container_width=True, type="primary"):
                st.session_state.page = "Pain Point Extraction"
                st.rerun()
    
    st.markdown("---")
    
    # Tool 2: Theme & Perspective Mapping
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 2. 🗂️ Theme & Perspective Mapping")
            st.markdown("""
            Categorise pain points into predefined themes and organisational perspectives.
            
            • Upload extracted pain points with ID tracking
            • AI maps pain points to predefined themes and perspectives
            • Configurable themes including Technology, Process, Culture, and Strategy
            • Multiple perspectives: People, Process, Technology, External factors
            • Batch processing for large datasets
            • Download categorised results with theme and perspective assignments
            
            **Perfect for:** Strategy consultants and change managers organising pain points 
            into actionable categories for targeted intervention planning.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_theme_creation", use_container_width=True, type="primary"):
                st.session_state.page = "Pain Point Theme Creation"
                st.rerun()
    
    st.markdown("---")
    
    # Tool 3: Pain Point Impact Estimation
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 3. 📊 Pain Point Impact Estimation")
            st.markdown("""
            Assess the business impact of identified pain points using AI analysis.
            
            • Upload pain points with descriptive information
            • AI evaluates impact across multiple business dimensions
            • Considers revenue, operations, customer satisfaction, and compliance factors
            • Impact levels: High, Medium, Low with detailed reasoning
            • Optional business context for more accurate assessments
            • Download comprehensive impact assessment results as Excel
            
            **Perfect for:** Business analysts and project managers prioritising pain points 
            based on potential business impact and strategic importance.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_impact_estimation", use_container_width=True, type="primary"):
                st.session_state.page = "Pain Point Impact Estimation"
                st.rerun()
    
    st.markdown("---")
    
    # Tool 4: Capability Mapping
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 4. 🎯 Capability Mapping")
            st.markdown("""
            Map pain points to organisational capabilities for strategic planning.
            
            • Upload separate spreadsheets for pain points and capabilities
            • Select ID columns and multiple descriptive text columns
            • AI matches each pain point to the most appropriate capability
            • Batch processing with configurable batch sizes for performance
            • Results include pain point IDs mapped to capability IDs
            • Download mapping table for integration with strategic planning tools
            
            **Perfect for:** Enterprise architects and strategy consultants connecting 
            organisational challenges with required capabilities for transformation planning.
            """)
        
        with col2:
            if st.button("Launch Tool", key="launch_capability_mapping", use_container_width=True, type="primary"):
                st.session_state.page = "Pain Point to Capability Mapping"
                st.rerun()
    
    st.markdown("---")
    
    # Tool 5: Capability Description Generation
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 5. 📝 Capability Description Generation")
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