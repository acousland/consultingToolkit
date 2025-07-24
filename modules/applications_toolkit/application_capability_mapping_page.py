import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from prompts import APPLICATION_CAPABILITY_MAPPING_PROMPT
from navigation import render_breadcrumbs

def application_capability_mapping_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🏗️ Applications Toolkit", "Applications Toolkit"), ("🔗 Application to Capability Mapping", None)])
    
    st.markdown("## 🔗 Application to Capability Mapping")
    st.markdown("_Map applications to business capabilities for technology landscape analysis_")
    
    st.markdown("---")
    
    # Applications file upload
    st.markdown("### 📱 Applications Data")
    applications_file = st.file_uploader("Choose Applications file", type=['xlsx', 'xls', 'xlsm'], key="applications_file_upload")
    
    applications_df = None
    app_sheet_names = []
    
    if applications_file is not None:
        # Read the Excel file and get sheet names
        try:
            excel_data = pd.ExcelFile(applications_file)
            app_sheet_names = excel_data.sheet_names
        except Exception as e:
            st.error(f"Error reading Applications Excel file: {str(e)}")
            return
        
        # Sheet selection for applications
        selected_app_sheet = st.selectbox("Select Applications sheet:", app_sheet_names, key="app_sheet_select")
        
        if selected_app_sheet:
            # Read the selected sheet
            applications_df = pd.read_excel(applications_file, sheet_name=selected_app_sheet)
            
            # Clean the dataframe to avoid PyArrow conversion issues
            for col in applications_df.columns:
                applications_df[col] = applications_df[col].astype(str)
            applications_df = applications_df.replace('nan', pd.NA)
            
            st.markdown(f"**Applications Sheet:** {selected_app_sheet}")
            st.markdown(f"**Rows:** {len(applications_df)} | **Columns:** {len(applications_df.columns)}")
            
            # Show preview
            with st.expander("📋 Preview Applications Data", expanded=False):
                preview_df = applications_df.head(10).copy()
                for col in preview_df.columns:
                    preview_df[col] = preview_df[col].astype(str)
                preview_df = preview_df.replace('nan', '').replace('<NA>', '')
                st.dataframe(preview_df)
    
    # Capabilities file upload
    st.markdown("### 🎯 Capabilities Data")
    capabilities_file = st.file_uploader("Choose Capabilities file", type=['xlsx', 'xls', 'xlsm'], key="capabilities_file_upload")
    
    capabilities_df = None
    cap_sheet_names = []
    
    if capabilities_file is not None:
        # Read the Excel file and get sheet names
        try:
            excel_data = pd.ExcelFile(capabilities_file)
            cap_sheet_names = excel_data.sheet_names
        except Exception as e:
            st.error(f"Error reading Capabilities Excel file: {str(e)}")
            return
        
        # Sheet selection for capabilities
        selected_cap_sheet = st.selectbox("Select Capabilities sheet:", cap_sheet_names, key="cap_sheet_select")
        
        if selected_cap_sheet:
            # Read the selected sheet
            capabilities_df = pd.read_excel(capabilities_file, sheet_name=selected_cap_sheet)
            
            # Clean the dataframe to avoid PyArrow conversion issues
            for col in capabilities_df.columns:
                capabilities_df[col] = capabilities_df[col].astype(str)
            capabilities_df = capabilities_df.replace('nan', pd.NA)
            
            st.markdown(f"**Capabilities Sheet:** {selected_cap_sheet}")
            st.markdown(f"**Rows:** {len(capabilities_df)} | **Columns:** {len(capabilities_df.columns)}")
            
            # Show preview
            with st.expander("📋 Preview Capabilities Data", expanded=False):
                preview_df = capabilities_df.head(10).copy()
                for col in preview_df.columns:
                    preview_df[col] = preview_df[col].astype(str)
                preview_df = preview_df.replace('nan', '').replace('<NA>', '')
                st.dataframe(preview_df)
    
    # Column selection (only show if both files are uploaded)
    if applications_df is not None and capabilities_df is not None:
        st.markdown("---")
        st.markdown("### 🔧 Column Selection")
        
        # Applications column selection
        st.markdown("#### Applications Mapping")
        app_col1, app_col2 = st.columns(2)
        
        with app_col1:
            app_id_column = st.selectbox(
                "Select Applications ID Column:",
                options=applications_df.columns.tolist(),
                key="app_id_column"
            )
        
        with app_col2:
            app_description_columns = st.multiselect(
                "Select Applications Description Column(s):",
                options=[col for col in applications_df.columns.tolist() if col != app_id_column],
                key="app_description_columns"
            )
        
        # Capabilities column selection
        st.markdown("#### Capabilities Mapping")
        cap_col1, cap_col2 = st.columns(2)
        
        with cap_col1:
            cap_id_column = st.selectbox(
                "Select Capabilities ID Column:",
                options=capabilities_df.columns.tolist(),
                key="cap_id_column"
            )
        
        with cap_col2:
            cap_description_columns = st.multiselect(
                "Select Capabilities Description Column(s):",
                options=[col for col in capabilities_df.columns.tolist() if col != cap_id_column],
                key="cap_description_columns"
            )
        
        # Additional context and processing
        if (app_id_column and app_description_columns and 
            cap_id_column and cap_description_columns):
            
            st.markdown("---")
            st.markdown("### 🏢 Additional Context")
            st.markdown("_Optionally provide additional context to improve mapping accuracy._")
            
            additional_context = st.text_area(
                "Enter additional context (optional - e.g., industry, organisation type, technology focus):",
                placeholder="e.g., Large financial services organisation with focus on digital banking platforms and regulatory compliance systems.",
                height=100,
                key="app_mapping_context"
            )
            
            # Show sample data
            st.markdown("### 📋 Data to be Processed")
            
            col_preview1, col_preview2 = st.columns(2)
            
            with col_preview1:
                st.markdown("**Sample Applications:**")
                app_sample = applications_df[[app_id_column] + app_description_columns].head(3).copy()
                for col in app_sample.columns:
                    app_sample[col] = app_sample[col].astype(str)
                app_sample = app_sample.replace('nan', '').replace('<NA>', '')
                st.dataframe(app_sample, use_container_width=True)
            
            with col_preview2:
                st.markdown("**Sample Capabilities:**")
                cap_sample = capabilities_df[[cap_id_column] + cap_description_columns].head(3).copy()
                for col in cap_sample.columns:
                    cap_sample[col] = cap_sample[col].astype(str)
                cap_sample = cap_sample.replace('nan', '').replace('<NA>', '')
                st.dataframe(cap_sample, use_container_width=True)
            
            st.markdown(f"**Total Applications:** {len(applications_df)} | **Total Capabilities:** {len(capabilities_df)}")
            
            # Batch size configuration
            st.markdown("### ⚙️ Processing Configuration")
            col_batch1, col_batch2 = st.columns(2)
            
            with col_batch1:
                batch_size = st.selectbox(
                    "Batch Size:",
                    options=[5, 10, 15, 20, 25],
                    index=1,  # Default to 10
                    help="Number of applications to process in each batch. Smaller batches are more reliable but slower.",
                    key="app_mapping_batch_size"
                )
            
            with col_batch2:
                estimated_batches = (len(applications_df) + batch_size - 1) // batch_size
                st.metric("Estimated Batches", estimated_batches)
            
            # Process button
            if st.button("🚀 Start Application Mapping", key="start_app_mapping", type="primary"):
                process_application_mapping(
                    applications_df, app_id_column, app_description_columns,
                    capabilities_df, cap_id_column, cap_description_columns,
                    additional_context, batch_size
                )

def process_application_mapping(applications_df, app_id_column, app_description_columns,
                              capabilities_df, cap_id_column, cap_description_columns,
                              additional_context, batch_size=10):
    """Process applications and map them to capabilities"""
    
    st.markdown("### 🔄 Processing Application to Capability Mapping")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_apps = len(applications_df)
    
    st.info(f"📊 Processing {total_apps} applications against {len(capabilities_df)} capabilities in batches of {batch_size}...")
    
    # Prepare capabilities lookup text
    capabilities_text = ""
    for _, cap_row in capabilities_df.iterrows():
        cap_id = cap_row[cap_id_column]
        cap_parts = []
        for col in cap_description_columns:
            if pd.notna(cap_row[col]) and str(cap_row[col]).strip():
                cap_parts.append(str(cap_row[col]).strip())
        
        cap_description = " | ".join(cap_parts)
        capabilities_text += f"{cap_id}: {cap_description}\n"
    
    # Create the mapping prompt header using template
    context_section = ""
    if additional_context and additional_context.strip():
        context_section = f"\nAdditional Context:\n{additional_context}\n"

    mapping_prompt_header = APPLICATION_CAPABILITY_MAPPING_PROMPT.format(
        capabilities=capabilities_text,
        context_section=context_section,
    )
    
    total_batches = (total_apps + batch_size - 1) // batch_size
    
    for i in range(0, total_apps, batch_size):
        batch_end = min(i + batch_size, total_apps)
        batch_df = applications_df.iloc[i:batch_end]
        current_batch = i // batch_size + 1
        
        # Prepare batch text
        batch_text = ""
        batch_app_ids = []
        
        for _, row in batch_df.iterrows():
            app_id = row[app_id_column]
            batch_app_ids.append(app_id)
            
            # Combine application description columns
            app_parts = []
            for col in app_description_columns:
                if pd.notna(row[col]) and str(row[col]).strip():
                    app_parts.append(str(row[col]).strip())
            
            app_description = " | ".join(app_parts)
            batch_text += f"{app_id}: {app_description}\n"
        
        status_text.text(f"🔄 Processing batch {current_batch} of {total_batches} ({len(batch_df)} applications)...")
        
        try:
            # Get AI response for the batch
            messages = [HumanMessage(content=mapping_prompt_header + batch_text)]
            response = model.invoke(messages)
            mapping_results = response.content.strip().split('\n')
            
            # Parse results
            for j, app_id in enumerate(batch_app_ids):
                if j < len(mapping_results):
                    mapping_text = mapping_results[j].strip()
                    # Extract capability IDs from the response
                    if ':' in mapping_text:
                        capabilities_part = mapping_text.split(':', 1)[1].strip()
                    else:
                        capabilities_part = mapping_text
                    
                    if capabilities_part.upper() == 'NONE' or not capabilities_part:
                        # No capabilities mapped
                        results.append({
                            'Application ID': app_id,
                            'Capability ID': 'No mapping found'
                        })
                    else:
                        # Parse multiple capability IDs
                        capability_ids = [cap.strip() for cap in capabilities_part.split(',') if cap.strip()]
                        if capability_ids:
                            for cap_id in capability_ids:
                                results.append({
                                    'Application ID': app_id,
                                    'Capability ID': cap_id
                                })
                        else:
                            results.append({
                                'Application ID': app_id,
                                'Capability ID': 'No mapping found'
                            })
                else:
                    # Default fallback
                    results.append({
                        'Application ID': app_id,
                        'Capability ID': 'No mapping found'
                    })
        
        except Exception as e:
            st.error(f"❌ Error processing batch {current_batch}: {str(e)}")
            # Add default results for this batch
            for app_id in batch_app_ids:
                results.append({
                    'Application ID': app_id,
                    'Capability ID': 'Processing error'
                })
        
        # Update progress
        progress = min((batch_end / total_apps), 1.0)
        progress_bar.progress(progress)
    
    # Clear status
    status_text.empty()
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Display results
    progress_bar.progress(1.0)
    st.success(f"🎉 Successfully processed {total_apps} applications!")
    
    # Show results summary
    st.markdown("### 📊 Mapping Results Summary")
    
    # Calculate summary statistics
    total_mappings = len(results_df)
    unique_apps = results_df['Application ID'].nunique()
    unique_caps = results_df[results_df['Capability ID'].notna()]['Capability ID'].nunique()
    no_mapping_count = len(results_df[results_df['Capability ID'] == 'No mapping found'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Mappings", total_mappings)
    with col2:
        st.metric("Applications Processed", unique_apps)
    with col3:
        st.metric("Capabilities Matched", unique_caps)
    with col4:
        st.metric("No Mappings Found", no_mapping_count)
    
    # Show results table
    st.markdown("### 📋 Application to Capability Mappings")
    
    # Clean results for display
    results_display = results_df.copy()
    for col in results_display.columns:
        results_display[col] = results_display[col].astype(str)
    results_display = results_display.replace('nan', '').replace('<NA>', '')
    
    st.dataframe(results_display, use_container_width=True)
    
    # Download button
    st.markdown("### ⬇️ Download Results")
    
    # Create Excel file for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='Application Mappings', index=False)
        
        # Add summary sheet
        summary_data = {
            'Metric': ['Total Mappings', 'Applications Processed', 'Capabilities Matched', 'No Mappings Found'],
            'Count': [total_mappings, unique_apps, unique_caps, no_mapping_count]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add applications overview
        app_mapping_counts = results_df.groupby('Application ID').size().reset_index(name='Mapping Count')
        app_mapping_counts.to_excel(writer, sheet_name='Applications Overview', index=False)
    
    output.seek(0)
    
    st.download_button(
        label="📊 Download Application Mapping Results",
        data=output.getvalue(),
        file_name="application_capability_mapping.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_app_mapping_results"
    )
    
    st.markdown("---")
    st.markdown("**📁 File Contents:**")
    st.markdown("• **Application Mappings** sheet: Application ID and Capability ID pairs")
    st.markdown("• **Summary** sheet: Mapping statistics and counts")
    st.markdown("• **Applications Overview** sheet: Number of mappings per application")
    
    # Back navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Applications Toolkit", key="back_to_apps_toolkit", use_container_width=True):
            st.session_state.page = "Applications Toolkit"
            st.rerun()
    with col2:
        if st.button("🏠 Go to Home", key="go_home_from_app_mapping", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("**📧 Want to be notified when this tool is ready?**")
    st.markdown("This tool is in active development. Check back soon for the full implementation!")
