import streamlit as st
import pandas as pd
import json
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs
import concurrent.futures
import time

def data_application_mapping_page():
    """Tool for mapping data entities to applications."""
    
    # Breadcrumbs
    render_breadcrumbs([
        ("Home", "Home"), 
        ("Data and Information Toolkit", "Data and Information Toolkit"), 
        ("Data-Application Mapping", None)
    ])
    
    st.markdown("## Data-Application Mapping Tool")
    st.markdown("Map data entities to applications and determine system of record vs system of entry relationships.")
    
    # Step 1: Data Entity Upload
    st.markdown("### Step 1: Upload Data Entities")
    
    # Data file upload
    data_file = st.file_uploader(
        "Upload Data Entities Spreadsheet",
        type=['xlsx', 'xls', 'xlsm', 'csv'],
        help="Upload a spreadsheet containing data entities with IDs and descriptions",
        key="data_upload"
    )
    
    data_df = None
    data_entity_id_col = None
    data_description_cols = []
    
    if data_file is not None:
        try:
            # Load the file
            if data_file.name.endswith('.csv'):
                available_sheets = ['CSV File']
                data_df = pd.read_csv(data_file)
            else:
                # Read Excel file and get sheet names
                excel_file = pd.ExcelFile(data_file)
                available_sheets = excel_file.sheet_names
                
                # Sheet selection for data
                data_sheet = st.selectbox(
                    "Select Data Sheet",
                    available_sheets,
                    key="data_sheet_select"
                )
                
                data_df = pd.read_excel(data_file, sheet_name=data_sheet)
                
                # Show preview of selected sheet
                if data_df is not None and not data_df.empty:
                    with st.expander(f"Preview of '{data_sheet}' sheet"):
                        st.write(f"**Rows:** {len(data_df)} | **Columns:** {len(data_df.columns)}")
                        st.dataframe(data_df.head(5), use_container_width=True)
            
            if data_df is not None and not data_df.empty:
                st.success(f"Successfully loaded data file with {len(data_df)} rows")
                
                # Column selection for data entities
                st.markdown("#### Configure Data Entity Columns")
                
                data_columns = data_df.columns.tolist()
                
                # Data Entity ID column (required)
                data_entity_id_col = st.selectbox(
                    "Data Entity ID Column",
                    data_columns,
                    help="Select the column containing unique data entity identifiers",
                    key="data_id_col"
                )
                
                # Description columns (optional, multi-select)
                remaining_data_cols = [col for col in data_columns if col != data_entity_id_col]
                data_description_cols = st.multiselect(
                    "Data Description Columns (Optional)",
                    remaining_data_cols,
                    help="Select columns that provide descriptions or additional context for data entities",
                    key="data_desc_cols"
                )
                
                # Preview data selection
                if data_entity_id_col:
                    preview_cols = [data_entity_id_col] + data_description_cols
                    with st.expander("Preview Data Entities"):
                        st.dataframe(data_df[preview_cols].head(10), use_container_width=True)
                        st.info(f"Total data entities: {len(data_df)}")
            
        except Exception as e:
            st.error(f"Error loading data file: {str(e)}")
    
    # Step 2: Application Upload
    st.markdown("### Step 2: Upload Applications")
    
    # Application file upload
    app_file = st.file_uploader(
        "Upload Applications Spreadsheet",
        type=['xlsx', 'xls', 'xlsm', 'csv'],
        help="Upload a spreadsheet containing applications with IDs and descriptions",
        key="app_upload"
    )
    
    app_df = None
    app_id_col = None
    app_description_cols = []
    
    if app_file is not None:
        try:
            # Load the application file
            if app_file.name.endswith('.csv'):
                app_available_sheets = ['CSV File']
                app_df = pd.read_csv(app_file)
            else:
                # Read Excel file and get sheet names
                app_excel_file = pd.ExcelFile(app_file)
                app_available_sheets = app_excel_file.sheet_names
                
                # Sheet selection for applications
                app_sheet = st.selectbox(
                    "Select Application Sheet",
                    app_available_sheets,
                    key="app_sheet_select"
                )
                
                app_df = pd.read_excel(app_file, sheet_name=app_sheet)
                
                # Show preview of selected sheet
                if app_df is not None and not app_df.empty:
                    with st.expander(f"Preview of '{app_sheet}' sheet"):
                        st.write(f"**Rows:** {len(app_df)} | **Columns:** {len(app_df.columns)}")
                        st.dataframe(app_df.head(5), use_container_width=True)
            
            if app_df is not None and not app_df.empty:
                st.success(f"Successfully loaded application file with {len(app_df)} rows")
                
                # Column selection for applications
                st.markdown("#### Configure Application Columns")
                
                app_columns = app_df.columns.tolist()
                
                # Application ID column (required)
                app_id_col = st.selectbox(
                    "Application ID Column",
                    app_columns,
                    help="Select the column containing unique application identifiers",
                    key="app_id_col"
                )
                
                # Description columns (optional, multi-select)
                remaining_app_cols = [col for col in app_columns if col != app_id_col]
                app_description_cols = st.multiselect(
                    "Application Description Columns (Optional)",
                    remaining_app_cols,
                    help="Select columns that provide descriptions or additional context for applications",
                    key="app_desc_cols"
                )
                
                # Preview application selection
                if app_id_col:
                    app_preview_cols = [app_id_col] + app_description_cols
                    with st.expander("Preview Applications"):
                        st.dataframe(app_df[app_preview_cols].head(10), use_container_width=True)
                        st.info(f"Total applications: {len(app_df)}")
            
        except Exception as e:
            st.error(f"Error loading application file: {str(e)}")
    
    # Step 3: Generate Mappings
    if (data_df is not None and app_df is not None and 
        data_entity_id_col is not None and app_id_col is not None):
        
        st.markdown("### Step 3: Generate Data-Application Mappings")
        st.markdown("Select an application and analyze which data entities are relevant to it.")
        
        # Prepare applications for selection
        applications = []
        for _, row in app_df.iterrows():
            app_info = {
                'id': str(row[app_id_col]),
                'name': str(row[app_id_col])  # Use ID as name if no other identifier
            }
            
            # Add description information
            descriptions = []
            for desc_col in app_description_cols:
                if pd.notna(row[desc_col]):
                    descriptions.append(f"{desc_col}: {str(row[desc_col])}")
            
            if descriptions:
                app_info['description'] = " | ".join(descriptions)
            else:
                app_info['description'] = "No description available"
            
            applications.append(app_info)
        
        # Application selection
        app_options = [f"{app['id']}: {app['description']}" for app in applications]
        selected_app_index = st.selectbox(
            "Select Application to Map",
            range(len(app_options)),
            format_func=lambda x: app_options[x],
            help="Choose the application you want to map data entities to"
        )
        
        selected_app = applications[selected_app_index]
        
        if st.button("Generate Mappings for Selected Application", type="primary", key="generate_mappings"):
            with st.spinner(f"Analyzing data entities for {selected_app['id']}..."):
                
                # Prepare data entities for processing
                data_entities = []
                for _, row in data_df.iterrows():
                    entity_info = {
                        'id': str(row[data_entity_id_col]),
                        'name': str(row[data_entity_id_col])  # Use ID as name if no other identifier
                    }
                    
                    # Add description information
                    descriptions = []
                    for desc_col in data_description_cols:
                        if pd.notna(row[desc_col]):
                            descriptions.append(f"{desc_col}: {str(row[desc_col])}")
                    
                    if descriptions:
                        entity_info['description'] = " | ".join(descriptions)
                    else:
                        entity_info['description'] = "No description available"
                    
                    data_entities.append(entity_info)
                
                # Create application context
                app_context = f"{selected_app['id']}: {selected_app['description']}"
                
                # Create entity context
                entity_context = ""
                for entity in data_entities:
                    entity_context += f"{entity['id']}: {entity['description']}\n"
                
                # Create mapping prompt with your new format
                mapping_prompt = f"""Application-to-Data Entity Mapping Analysis

You are a solution architect evaluating how a single application fits into an organisation's enterprise data model. Your task is to identify all data entities that are meaningfully connected to the application based on how it is used in real business operations.

APPLICATION CONTEXT:

{app_context}

DATA ENTITY CATALOGUE:

{entity_context}

TASK:

List all Data Entity IDs that are relevant to this application. For each mapping, explain why the application interacts with or relies on that data entity. You should consider the full range of business functions the application performs—such as capturing user inputs, managing customer interactions, logging activities, supporting marketing efforts, or integrating with other systems.

INSTRUCTIONS:

• Focus only on the current application—do not reference other systems  
• Include any data entities the application helps create, view, manage, use, or exchange  
• Your goal is to build a comprehensive picture of how this application fits into the data landscape  
• Base your reasoning on common enterprise usage patterns, integrations, and practical business processes  
• If a data entity is not relevant, omit it

OUTPUT FORMAT:

Present each mapping as a single line in the format:

Data Entity ID | Reasoning

EXAMPLE (for Calendly):

DE014 | Calendly captures lead details when a prospect books a meeting, making it an important touchpoint in the sales funnel  
DE020 | Meeting bookings scheduled via Calendly represent sales activities that should be tracked for performance and forecasting  
DE033 | Booking actions in Calendly contribute to digital analytics events that measure engagement across channels  
DE034 | Calendly booking links are often embedded in marketing campaigns, making them relevant to lead source attribution

IMPORTANT:
- Use only the exact Data Entity IDs from the list above
- Be thorough and precise in your reasoning"""
                
                try:
                    # Call LangChain model
                    response = model.invoke([HumanMessage(content=mapping_prompt)])
                    result = response.content.strip()
                    
                    # Parse results into structured data
                    mapping_data = []
                    mapping_counter = 1
                    
                    lines = result.split('\n')
                    for line in lines:
                        line = line.strip()
                        if ' | ' in line and not line.startswith('Data Entity ID'):
                            parts = line.split(' | ', 1)  # Split only on first occurrence
                            if len(parts) == 2:
                                data_entity_id = parts[0].strip()
                                reasoning = parts[1].strip()
                                
                                # Validate data entity ID exists in our data
                                data_entity_exists = any(entity['id'] == data_entity_id for entity in data_entities)
                                
                                if data_entity_exists:
                                    mapping_id = f"DAM{mapping_counter:03d}"
                                    mapping_data.append({
                                        'Mapping ID': mapping_id,
                                        'Data Entity ID': data_entity_id,
                                        'Application ID': selected_app['id'],
                                        'Reasoning': reasoning
                                    })
                                    mapping_counter += 1
                    
                    if mapping_data:
                        # Store results with explicit string conversion to avoid Arrow conversion issues
                        mappings_df = pd.DataFrame(mapping_data)
                        
                        # Ensure all columns are properly typed as strings
                        mappings_df['Mapping ID'] = mappings_df['Mapping ID'].astype(str)
                        mappings_df['Data Entity ID'] = mappings_df['Data Entity ID'].astype(str)
                        mappings_df['Application ID'] = mappings_df['Application ID'].astype(str)
                        mappings_df['Reasoning'] = mappings_df['Reasoning'].astype(str)
                        
                        # Initialize or append to existing mappings
                        if 'data_app_mappings_df' in st.session_state:
                            # Remove existing mappings for this application
                            existing_df = st.session_state.data_app_mappings_df
                            
                            # Ensure existing DataFrame has same column types
                            existing_df['Mapping ID'] = existing_df['Mapping ID'].astype(str)
                            existing_df['Data Entity ID'] = existing_df['Data Entity ID'].astype(str)
                            existing_df['Application ID'] = existing_df['Application ID'].astype(str)
                            existing_df['Reasoning'] = existing_df['Reasoning'].astype(str)
                            
                            filtered_df = existing_df[existing_df['Application ID'] != selected_app['id']]
                            # Append new mappings
                            st.session_state.data_app_mappings_df = pd.concat([filtered_df, mappings_df], ignore_index=True)
                        else:
                            st.session_state.data_app_mappings_df = mappings_df
                        
                        st.success(f"✅ Generated {len(mapping_data)} data entity mappings for {selected_app['id']}!")
                    else:
                        st.error("No valid mappings were generated. Please check your data and try again.")
                        
                except Exception as e:
                    st.error(f"Error generating mappings: {str(e)}")
    
    # Step 4: Display Results
    if 'data_app_mappings_df' in st.session_state:
        st.markdown("### Step 4: Generated Mappings")
        
        mappings_df = st.session_state.data_app_mappings_df
        
        # Ensure proper data types for display to avoid Arrow conversion issues
        if not mappings_df.empty:
            mappings_df = mappings_df.copy()
            mappings_df['Mapping ID'] = mappings_df['Mapping ID'].astype(str)
            mappings_df['Data Entity ID'] = mappings_df['Data Entity ID'].astype(str)
            mappings_df['Application ID'] = mappings_df['Application ID'].astype(str)
            mappings_df['Reasoning'] = mappings_df['Reasoning'].astype(str)
        
        st.dataframe(mappings_df, use_container_width=True, hide_index=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Mappings", len(mappings_df))
        with col2:
            unique_entities = mappings_df['Data Entity ID'].nunique()
            st.metric("Unique Data Entities", unique_entities)
        with col3:
            unique_apps = mappings_df['Application ID'].nunique()
            st.metric("Mapped Applications", unique_apps)
        
        # Download options
        st.markdown("#### Download Options")
        
        # CSV download
        csv = mappings_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="data_application_mappings.csv",
            mime="text/csv"
        )
        
        # Excel download
        def create_excel_file():
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                mappings_df.to_excel(writer, sheet_name='Data-Application Mappings', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': ['Total Mappings', 'Unique Data Entities', 'Mapped Applications'],
                    'Count': [
                        len(mappings_df),
                        mappings_df['Data Entity ID'].nunique(),
                        mappings_df['Application ID'].nunique()
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
            return output.getvalue()
        
        excel_data = create_excel_file()
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name="data_application_mappings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Data Toolkit", key="back_to_data_toolkit"):
            st.session_state.page = "Data and Information Toolkit"
            st.rerun()
    
    with col2:
        if st.button("← Back to Home", key="back_to_home_from_mapping"):
            st.session_state.page = "Home"
            st.rerun()
