import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage
from app_config import model
from prompts import INDIVIDUAL_APPLICATION_MAPPING_PROMPT
from navigation import render_breadcrumbs

def individual_application_mapping_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🏗️ Applications Toolkit", "Applications Toolkit"), ("🎯 Individual Application Mapping", None)])
    
    st.markdown("# 🎯 Individual Application to Capability Mapping")
    st.markdown("**Map a single application to organisational capabilities**")
    
    st.markdown("""
    This tool helps you quickly map individual applications to your capability framework. Upload your capability 
    model, describe your application, and receive AI-powered capability mappings for architecture analysis.
    """)
    
    st.markdown("---")
    
    # Initialize session state
    if 'capabilities_df' not in st.session_state:
        st.session_state['capabilities_df'] = None
    if 'cap_columns' not in st.session_state:
        st.session_state['cap_columns'] = {'id': None, 'text': None}
    
    # Step 1: Upload Capabilities Framework
    st.markdown("## 📊 Step 1: Upload Capability Framework")
    
    capabilities_file = st.file_uploader(
        "Upload Capabilities Excel file",
        type=['xlsx', 'xls', 'xlsm'],
        key="capabilities_upload",
        help="Upload your organisational capability framework"
    )
    
    if capabilities_file is not None:
        # Load capabilities file
        xls = pd.ExcelFile(capabilities_file)
        cap_sheet = st.selectbox("Select sheet for capabilities", xls.sheet_names, key="cap_sheet")
        capabilities_df = pd.read_excel(xls, sheet_name=cap_sheet)
        st.session_state['capabilities_df'] = capabilities_df
        
        st.write("**Capabilities Preview:**")
        st.dataframe(capabilities_df.head())
        
        # Column selection for capabilities
        col1, col2 = st.columns(2)
        
        with col1:
            cap_id_col = st.selectbox(
                "Select Capability ID column", 
                capabilities_df.columns,
                key="cap_id_col"
            )
        
        with col2:
            cap_text_cols = st.multiselect(
                "Select Capability description columns", 
                capabilities_df.columns,
                key="cap_text_cols",
                help="Select one or more columns to describe the capability (e.g., name, description, details)"
            )
        
        # Store column selections in session state
        st.session_state['cap_columns']['id'] = cap_id_col
        st.session_state['cap_columns']['text'] = cap_text_cols
        
        # Step 2: Application Input
        if cap_id_col and cap_text_cols:
            st.markdown("---")
            st.markdown("## 🔧 Step 2: Describe Your Application")
            
            col1, col2 = st.columns(2)
            
            with col1:
                app_name = st.text_input(
                    "Application Name:",
                    placeholder="e.g., Customer Relationship Management System",
                    help="Enter the name or identifier for your application"
                )
            
            with col2:
                app_id = st.text_input(
                    "Application ID (optional):",
                    placeholder="e.g., CRM-001, APP-345",
                    help="Optional: Enter a unique identifier for this application"
                )
            
            app_description = st.text_area(
                "Application Description:",
                placeholder="Describe what this application does, its main functions, user groups, business purpose, technical characteristics, etc.",
                help="Provide a detailed description to help with accurate capability mapping",
                height=120
            )
            
            # Additional context
            additional_context = st.text_area(
                "Additional Context (optional):",
                placeholder="e.g., Focus on customer-facing capabilities, emphasise operational processes, consider regulatory requirements...",
                help="Optional context to guide the mapping process",
                height=80
            )
            
            # Step 3: Generate Mapping
            if app_name and app_description:
                st.markdown("---")
                st.markdown("## 🚀 Step 3: Generate Capability Mapping")
                
                if st.button("🎯 Map Application to Capabilities", use_container_width=True, type="primary"):
                    map_individual_application(
                        capabilities_df, 
                        cap_id_col, 
                        cap_text_cols, 
                        app_name, 
                        app_id, 
                        app_description, 
                        additional_context
                    )

def map_individual_application(capabilities_df, cap_id_col, cap_text_cols, app_name, app_id, app_description, additional_context):
    """Generate capability mapping for individual application"""
    
    with st.spinner("Analysing application and generating capability mappings..."):
        
        # Prepare capabilities list for AI
        capabilities_list = []
        for _, cap_row in capabilities_df.iterrows():
            cap_id = cap_row[cap_id_col]
            # Concatenate selected capability text columns
            cap_text_parts = []
            for col in cap_text_cols:
                if pd.notna(cap_row[col]):
                    cap_text_parts.append(str(cap_row[col]))
            cap_text = ' | '.join(cap_text_parts)
            capabilities_list.append(f"- {cap_id}: {cap_text}")
        
        capabilities_text = "\n".join(capabilities_list)
        
        # Create application description
        app_display_id = f" (ID: {app_id})" if app_id.strip() else ""
        app_info = f"Application: {app_name}{app_display_id}\nDescription: {app_description}"
        
        # Create AI prompt using template
        context_section = f"Additional Context: {additional_context}\n\n" if additional_context.strip() else ""

        prompt = INDIVIDUAL_APPLICATION_MAPPING_PROMPT.format(
            context_section=context_section,
            app_info=app_info,
            capabilities_text=capabilities_text,
        )

        try:
            # Call AI model
            message = HumanMessage(content=prompt)
            response = model.invoke([message])
            ai_response = response.content.strip()
            
            # Display results
            st.markdown("## 🎯 Capability Mapping Results")
            
            # Application summary
            st.markdown("### 📱 Application Summary")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Application Name:** {app_name}")
                if app_id.strip():
                    st.markdown(f"**Application ID:** {app_id}")
                st.markdown(f"**Description:** {app_description}")
            
            with col2:
                # Count total capabilities in framework
                total_capabilities = len(capabilities_df)
                st.metric("Total Capabilities in Framework", total_capabilities)
            
            # AI Analysis Results
            st.markdown("### 🤖 AI Analysis Results")
            
            # Parse and display the results with better formatting
            if "No Direct Capability Mappings Found" in ai_response:
                st.warning("🔍 **No Direct Capability Mappings Found**")
                st.markdown("The AI analysis did not find any strong alignments between this application and the available capabilities in your framework.")
            else:
                # Display the AI response with proper formatting
                st.markdown(ai_response)
            
            # Additional analysis info
            if additional_context.strip():
                st.markdown("### 📝 Analysis Context")
                st.info(f"Additional context used: {additional_context}")
            
            # Quick actions
            st.markdown("---")
            st.markdown("### 🔄 Quick Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Analyse Another Application", use_container_width=True):
                    st.rerun()
            
            with col2:
                if st.button("🔗 Bulk Application Mapping", use_container_width=True):
                    st.session_state.page = "Application to Capability Mapping"
                    st.rerun()
            
            with col3:
                if st.button("🏗️ Back to Applications Toolkit", use_container_width=True):
                    st.session_state.page = "Applications Toolkit"
                    st.rerun()
            
            st.success("✅ Capability mapping analysis complete!")
            
        except Exception as e:
            st.error(f"❌ Error generating capability mapping: {str(e)}")
            st.error("Please check your inputs and try again.")
