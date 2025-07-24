import streamlit as st
from navigation import render_breadcrumbs

def data_information_toolkit_page():
    """Data and Information Toolkit page with various data modeling and analysis tools."""
    
    # Breadcrumbs
    render_breadcrumbs([("Home", "Home"), ("Data and Information Toolkit", None)])
    
    st.markdown("## Data and Information Toolkit")
    st.markdown("Comprehensive tools for data modeling, analysis, and information architecture.")
    
    # Introduction section
    st.markdown("""
    This toolkit provides essential tools for data consultants, data architects, and business analysts 
    working on data strategy, information architecture, and data modeling initiatives.
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
    
    # Future tools row
    st.markdown("---")
    st.markdown("### Coming Soon")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🔄 **More Tools Coming Soon**")
        st.markdown("_Additional data and information tools will be added here_")
        
        st.markdown("""
        **Future tools may include:**
        • Data Quality Assessment
        • Information Flow Mapping
        • Data Governance Framework
        • Master Data Strategy
        """)
    
    st.markdown("---")
    
    # Quick navigation back to home
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state.page = "Home"
        st.rerun()
