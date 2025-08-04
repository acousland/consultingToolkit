import streamlit as st
from navigation import render_breadcrumbs

def data_information_toolkit_page():
    """Data, Information, and AI Toolkit page with various data modeling, analysis, and AI tools."""
    
    # Breadcrumbs
    render_breadcrumbs([("Home", "Home"), ("Data, Information, and AI Toolkit", None)])
    
    st.markdown("## Data, Information, and AI Toolkit")
    st.markdown("Comprehensive tools for data modeling, analysis, information architecture, and AI solutions.")
    
    # Introduction section
    st.markdown("""
    This toolkit provides essential tools for data consultants, data architects, AI specialists, and business analysts 
    working on data strategy, information architecture, data modeling, and AI implementation initiatives.
    """)
    
    st.markdown("---")
    
    # Tool selection
    st.markdown("### Available Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 **Conceptual Data Model Generator**")
        st.markdown("_Generate comprehensive conceptual data models for business domains_")
        
        st.markdown("""
        **Perfect for:** Creating high-level data models that capture business entities, 
        relationships, and key attributes for strategic data initiatives.
        
        **Key features:**
        • Entity identification and definition
        • Relationship mapping
        • Data dictionary generation
        • Business rules documentation
        """)
        
        if st.button("Launch Conceptual Data Model Generator", key="conceptual_data_model", use_container_width=True, type="primary"):
            st.session_state.page = "Conceptual Data Model Generator"
            st.rerun()
    
    with col2:
        st.markdown("#### 🔗 **Data-Application Mapping**")
        st.markdown("_Map data entities to applications and determine system relationships_")
        
        st.markdown("""
        **Perfect for:** Understanding which data assets reside in which systems and 
        their role as system of entry or system of record.
        
        **Key features:**
        • Data entity to application mapping
        • System of entry vs system of record analysis
        • Batch processing for large datasets
        • Detailed relationship reasoning
        """)
        
        if st.button("Launch Data-Application Mapping", key="data_app_mapping", use_container_width=True, type="primary"):
            st.session_state.page = "Data-Application Mapping"
            st.rerun()
    
    # Second row of tools
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🤖 **AI Use Case Customiser**")
        st.markdown("_Evaluate and rank AI use cases for your specific company context_")
        
        st.markdown("""
        **Perfect for:** Assessing AI opportunities, prioritizing use cases based on company context, 
        and creating customized AI implementation roadmaps.
        
        **Key features:**
        • Company context integration
        • AI use case scoring (1-100)
        • Parallel processing for efficiency
        • Ranked recommendations
        """)
        
        if st.button("Launch AI Use Case Customiser", key="ai_use_case_customiser", use_container_width=True, type="primary"):
            st.session_state.page = "AI Use Case Customiser"
            st.rerun()
    
    with col4:
        st.markdown("#### ⚖️ **Use Case Ethics Review**")
        st.markdown("_Comprehensive ethical analysis of use cases from multiple philosophical perspectives_")
        
        st.markdown("""
        **Perfect for:** Evaluating the ethical implications of any use case, ensuring responsible 
        implementation, and building stakeholder confidence.
        
        **Key features:**
        • Deontological (rule-based) analysis
        • Utilitarian cost-benefit evaluation
        • Social contract assessment
        • Virtue ethics review
        """)
        
        if st.button("Launch Use Case Ethics Review", key="use_case_ethics_review", use_container_width=True, type="primary"):
            st.session_state.page = "Use Case Ethics Review"
            st.rerun()
    
    # Future tools row
    st.markdown("---")
    st.markdown("### Coming Soon")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 🔄 **More Tools Coming Soon**")
        st.markdown("_Additional data, information, and AI tools will be added here_")
        
        st.markdown("""
        **Future tools may include:**
        • Data Quality Assessment
        • Information Flow Mapping
        • Data Governance Framework
        • AI Risk Assessment
        """)
    
    with col6:
        st.markdown("#### 💡 **Suggest a Tool**")
        st.markdown("_Have ideas for new tools in this toolkit?_")
        
        st.markdown("""
        **We're always looking to expand:**
        • Contact us with your suggestions
        • Tools for data strategy
        • AI implementation guidance
        • Information architecture aids
        """)
    
    st.markdown("---")
    
    # Quick navigation back to home
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state.page = "Home"
        st.rerun()
