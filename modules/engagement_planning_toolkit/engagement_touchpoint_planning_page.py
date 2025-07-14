import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model

def engagement_touchpoint_planning_page():
    # Breadcrumb navigation as a single line with clickable elements
    breadcrumb_container = st.container()
    
    with breadcrumb_container:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 0.2, 1.5, 0.2, 1.5, 0.2, 1])
        
        with col1:
            if st.button("🏠 Home", key="nav_home_etp", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
        
        with col2:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>→</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("📅 Engagement Planning Toolkit", key="nav_ep_toolkit_etp", use_container_width=True):
                st.session_state.page = "Engagement Planning Toolkit"
                st.rerun()
        
        with col4:
            st.markdown("<div style='text-align: center; padding-top: 8px;'>→</div>", unsafe_allow_html=True)
        
        with col5:
            st.markdown("<div style='background-color: #e6f3ff; padding: 8px; border-radius: 4px; text-align: center;'><strong>📞 Touchpoint Planning</strong></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Under Development Banner
    st.warning("🚧 **Under Development** - This tool is currently being developed and refined. Features and functionality may change.")
    
    # Tool Header
    st.markdown("# 📞 Engagement Touchpoint Planning")
    st.markdown("**Design structured touchpoint sequences for effective client engagement**")
    
    st.markdown("""
    Plan your client engagement strategy with purpose-driven touchpoints. This tool helps you 
    design communication schedules, stakeholder interactions, and milestone check-ins that 
    maintain strong client relationships and ensure project success.
    """)
    
    st.markdown("---")
    
    # Input Section
    st.markdown("## 📋 Engagement Details")
    
    # Basic engagement information
    col1, col2 = st.columns(2)
    
    with col1:
        engagement_type = st.selectbox(
            "Engagement Type",
            ["Strategy Consulting", "Digital Transformation", "Process Improvement", 
             "Organisational Change", "Technology Implementation", "Due Diligence", 
             "Capability Assessment", "Other"],
            help="Select the type of engagement to customise touchpoint recommendations"
        )
        
        engagement_duration = st.selectbox(
            "Engagement Duration",
            ["2-4 weeks", "1-2 months", "3-6 months", "6-12 months", "12+ months"],
            help="Expected duration of the engagement"
        )
    
    with col2:
        client_size = st.selectbox(
            "Client Organisation Size",
            ["Small (< 100 employees)", "Medium (100-1000 employees)", 
             "Large (1000-10000 employees)", "Enterprise (10000+ employees)"],
            help="Size of the client organisation"
        )
        
        engagement_phase = st.selectbox(
            "Current Engagement Phase",
            ["Pre-engagement/Proposal", "Kickoff & Discovery", "Analysis & Design", 
             "Implementation", "Change Management", "Closure & Handover"],
            help="Current phase of the engagement"
        )
    
    # Key stakeholders
    st.markdown("### 👥 Key Stakeholders")
    stakeholder_input = st.text_area(
        "Key Stakeholders & Roles",
        placeholder="e.g., CEO (Executive Sponsor), CTO (Technical Lead), PMO Director (Project Oversight), Department Heads (End Users)...",
        help="List the key stakeholders and their roles in this engagement",
        height=100
    )
    
    # Engagement objectives
    st.markdown("### 🎯 Engagement Objectives")
    objectives_input = st.text_area(
        "Primary Objectives & Success Criteria",
        placeholder="e.g., Reduce operational costs by 15%, Improve customer satisfaction scores, Implement new technology platform...",
        help="Describe the main objectives and success criteria for this engagement",
        height=100
    )
    
    # Additional context
    st.markdown("### 📝 Additional Context")
    additional_context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Any specific requirements, constraints, or preferences for the engagement approach...",
        help="Provide any additional context that might influence the touchpoint planning",
        height=80
    )
    
    st.markdown("---")
    
    # Processing Configuration
    st.markdown("## ⚙️ Planning Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        touchpoint_frequency = st.selectbox(
            "Preferred Touchpoint Frequency",
            ["Daily", "Every 2-3 days", "Weekly", "Bi-weekly", "Monthly"],
            index=2,
            help="How frequently you prefer to have formal touchpoints"
        )
    
    with col2:
        communication_style = st.selectbox(
            "Communication Style Preference",
            ["Formal & Structured", "Professional but Flexible", "Collaborative & Informal"],
            index=1,
            help="Preferred style for client communications"
        )
    
    # Process button
    if st.button("🔄 Generate Touchpoint Plan", type="primary", use_container_width=True):
        if not stakeholder_input.strip() or not objectives_input.strip():
            st.error("❌ Please provide stakeholder information and engagement objectives to generate a touchpoint plan.")
        else:
            generate_touchpoint_plan(
                engagement_type, engagement_duration, client_size, engagement_phase,
                stakeholder_input, objectives_input, additional_context,
                touchpoint_frequency, communication_style
            )

def generate_touchpoint_plan(engagement_type, engagement_duration, client_size, engagement_phase,
                           stakeholder_input, objectives_input, additional_context,
                           touchpoint_frequency, communication_style):
    """Generate a structured touchpoint plan for the engagement"""
    
    st.markdown("### 🔄 Generating Touchpoint Plan")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Analysing engagement requirements...")
    progress_bar.progress(0.2)
    
    # Create the touchpoint planning prompt
    context_section = ""
    if additional_context and additional_context.strip():
        context_section = f"\nAdditional Context:\n{additional_context}\n"
    
    touchpoint_prompt = f"""You are an experienced engagement manager and client relationship specialist. Your task is to create a comprehensive touchpoint plan for a consulting engagement.

Engagement Details:
- Type: {engagement_type}
- Duration: {engagement_duration}
- Client Size: {client_size}
- Current Phase: {engagement_phase}
- Touchpoint Frequency: {touchpoint_frequency}
- Communication Style: {communication_style}

Key Stakeholders:
{stakeholder_input}

Engagement Objectives:
{objectives_input}

{context_section}

Create a comprehensive touchpoint plan that includes:

1. **ENGAGEMENT CALENDAR**: A timeline of key touchpoints throughout the engagement
2. **STAKEHOLDER MATRIX**: Specific communication plan for each stakeholder group
3. **TOUCHPOINT TYPES**: Different types of interactions (meetings, reports, check-ins, etc.)
4. **COMMUNICATION CADENCE**: Frequency and timing for each type of touchpoint
5. **MILESTONE REVIEWS**: Key decision points and milestone celebrations
6. **ESCALATION PROTOCOLS**: When and how to escalate issues or concerns
7. **SUCCESS MEASUREMENTS**: How to track and demonstrate progress

Format your response with clear sections and Australian English. Include specific recommendations for:
- Meeting formats and durations
- Reporting cadences
- Stakeholder-specific touchpoints
- Key milestone reviews
- Communication protocols

Make the plan practical and actionable for immediate implementation."""
    
    status_text.text("🤖 Generating comprehensive touchpoint plan...")
    progress_bar.progress(0.6)
    
    try:
        # Get AI response
        messages = [HumanMessage(content=touchpoint_prompt)]
        response = model.invoke(messages)
        touchpoint_plan = response.content.strip()
        
        progress_bar.progress(1.0)
        status_text.empty()
        
        # Display results
        st.success("🎉 Touchpoint plan generated successfully!")
        
        # Show the touchpoint plan
        st.markdown("### 📅 Your Engagement Touchpoint Plan")
        st.markdown(touchpoint_plan)
        
        # Create downloadable plan
        st.markdown("### ⬇️ Download Plan")
        
        # Create a structured document for download
        plan_document = f"""ENGAGEMENT TOUCHPOINT PLAN
================================

Engagement Overview:
- Type: {engagement_type}
- Duration: {engagement_duration}
- Client Size: {client_size}
- Current Phase: {engagement_phase}
- Touchpoint Frequency: {touchpoint_frequency}
- Communication Style: {communication_style}

Key Stakeholders:
{stakeholder_input}

Engagement Objectives:
{objectives_input}

{context_section}

TOUCHPOINT PLAN:
{touchpoint_plan}

Generated on: {pd.Timestamp.now().strftime('%d %B %Y at %I:%M %p')}
"""
        
        # Create download button
        st.download_button(
            label="📋 Download Touchpoint Plan",
            data=plan_document,
            file_name=f"touchpoint_plan_{engagement_type.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            key="download_touchpoint_plan"
        )
        
        # Create Excel version with structured data
        st.markdown("### 📊 Structured Plan (Excel)")
        
        # Create sample structured data for Excel
        sample_data = {
            'Week': [f'Week {i}' for i in range(1, 9)],
            'Touchpoint Type': ['Kickoff Meeting', 'Progress Review', 'Stakeholder Check-in', 
                              'Milestone Review', 'Status Update', 'Issue Resolution', 
                              'Progress Review', 'Final Review'],
            'Stakeholders': ['All Key Stakeholders', 'Project Team', 'Executive Sponsor',
                           'Department Heads', 'Project Team', 'All Stakeholders',
                           'Project Team', 'All Key Stakeholders'],
            'Duration': ['2 hours', '1 hour', '30 minutes', '1.5 hours',
                       '30 minutes', '1 hour', '1 hour', '2 hours'],
            'Format': ['In-person/Virtual', 'Virtual', 'One-on-one', 'In-person/Virtual',
                     'Email/Dashboard', 'Virtual', 'Virtual', 'In-person/Virtual']
        }
        
        sample_df = pd.DataFrame(sample_data)
        
        # Create Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            sample_df.to_excel(writer, sheet_name='Touchpoint Schedule', index=False)
            
            # Add engagement details sheet
            details_data = {
                'Attribute': ['Engagement Type', 'Duration', 'Client Size', 'Current Phase',
                            'Touchpoint Frequency', 'Communication Style'],
                'Value': [engagement_type, engagement_duration, client_size, engagement_phase,
                         touchpoint_frequency, communication_style]
            }
            details_df = pd.DataFrame(details_data)
            details_df.to_excel(writer, sheet_name='Engagement Details', index=False)
        
        output.seek(0)
        
        st.download_button(
            label="📊 Download Structured Plan (Excel)",
            data=output.getvalue(),
            file_name=f"touchpoint_plan_{engagement_type.lower().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_touchpoint_excel"
        )
        
    except Exception as e:
        progress_bar.progress(1.0)
        status_text.empty()
        st.error(f"❌ Error generating touchpoint plan: {str(e)}")
        st.markdown("Please try again or contact support if the issue persists.")
    
    st.markdown("---")
    st.markdown("### 💡 Next Steps")
    st.markdown("""
    **After downloading your touchpoint plan:**
    1. Review the plan with your engagement team
    2. Customise timings based on client preferences
    3. Set up calendar invitations for key touchpoints
    4. Prepare templates for regular communications
    5. Establish success metrics and tracking mechanisms
    """)
