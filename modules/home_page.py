import streamlit as st

def home_page():
    st.markdown("""
    This consulting toolkit is organised into six specialised toolkits, each designed to address specific aspects 
    of organisational analysis, capability development, engagement planning, data architecture, and strategic alignment. Choose the toolkit that matches your current consulting needs.
    """)
    
    st.markdown("---")
    
    # Top row - Pain Point, Capability, and Applications Toolkits
    col1, col2, col3 = st.columns(3)
    
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
        • Pain Point Impact Estimation
        • Capability Mapping
        
        **Typical workflow:** Extract → Categorise → Assess Impact → Map to Capabilities
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

    with col3:
        # Applications Toolkit Overview
        st.markdown("## 🏗️ **Applications Toolkit**")
        st.markdown("_Map and analyse technology landscape_")
        
        st.markdown("""
        **Perfect for:** Consultants conducting technology assessments, mapping applications to business capabilities, 
        and supporting architecture planning initiatives.
        
        **Tools included:**
        • Application to Capability Mapping
        • Logical Application Model Generator
        
        **Typical workflow:** Map Applications → Generate Logical Models → Analyse Technology Landscape → Support Architecture Decisions
        """)
        
        if st.button("Enter Applications Toolkit", key="enter_applications_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Applications Toolkit"
            st.rerun()
    
    # Add some space between rows
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom row - Data Information, Engagement Planning and Strategy & Motivations Toolkits
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Data, Information, and AI Toolkit Overview
        st.markdown("## 📊 **Data, Information, and AI Toolkit**")
        st.markdown("_Design data models, information architecture, and AI solutions_")
        
        st.markdown("""
        **Perfect for:** Data consultants, data architects, AI specialists, and business analysts working on data strategy, 
        information architecture, data modeling, and AI implementation initiatives.
        
        **Tools included:**
        • Conceptual Data Model Generator
        • Data-Application Mapping
        • AI Use Case Customiser
        
        **Typical workflow:** Analyze Requirements → Generate Data Models → Document Relationships → Define Business Rules → Assess AI Opportunities
        """)
        
        if st.button("Enter Data, Information, and AI Toolkit", key="enter_data_information_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Data, Information, and AI Toolkit"
            st.rerun()
    
    with col5:
        # Engagement Planning Toolkit Overview
        st.markdown("## 📅 **Engagement Planning Toolkit**")
        st.markdown("_Plan and structure client engagements_")
        
        st.markdown("""
        **Perfect for:** Consultants designing engagement approaches, planning touchpoints and interactions, 
        and structuring client communication strategies.
        
        **Tools included:**
        • Engagement Touchpoint Planning
        
        **Typical workflow:** Plan Touchpoints → Structure Engagement → Execute Client Communications
        """)
        
        if st.button("Enter Engagement Planning Toolkit", key="enter_engagement_planning_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Engagement Planning Toolkit"
            st.rerun()

    with col6:
        # Strategy and Motivations Toolkit Overview
        st.markdown("## 🎯 **Strategy and Motivations Toolkit**")
        st.markdown("_Align strategies with organisational capabilities_")
        
        st.markdown("""
        **Perfect for:** Consultants conducting strategic analysis, mapping strategic initiatives to required capabilities, 
        and supporting strategic planning and implementation.
        
        **Tools included:**
        • Strategy to Capability Mapping
        
        **Typical workflow:** Analyse Strategic Initiatives → Map to Required Capabilities → Support Strategic Implementation
        """)
        
        if st.button("Enter Strategy and Motivations Toolkit", key="enter_strategy_motivations_toolkit", use_container_width=True, type="primary"):
            st.session_state.page = "Strategy and Motivations Toolkit"
            st.rerun()

    # Admin & Testing Tool
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        col_admin_text, col_admin_btn = st.columns([3, 1])

        with col_admin_text:
            st.markdown("### ⚙️ Admin & Testing Tool")
            st.markdown("Configure OpenAI models and check connectivity.")

        with col_admin_btn:
            if st.button("Open Tool", key="enter_admin_tool", use_container_width=True, type="primary"):
                st.session_state.page = "Admin Tool"
                st.rerun()

    st.markdown("---")
