import streamlit as st
import pandas as pd
import math
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs

def application_categorization_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🏗️ Applications Toolkit", "Applications Toolkit"), ("📊 Application Categorisation", None)])
    
    st.markdown("# 📊 Application Categorisation")
    st.markdown("**Categorise applications into Application, Technology, or Platform classifications**")
    
    st.markdown("""
    This tool uses AI to analyse your software portfolio and categorise each item based on enterprise architecture principles.
    Upload your applications spreadsheet and receive structured categorisations for architecture planning.
    """)
    
    st.markdown("---")
    
    # Category definitions
    with st.expander("📖 Category Definitions", expanded=False):
        st.markdown("""
        **Application**  
        A discrete software solution that delivers a specific set of business functions to defined user groups. 
        Usually carries its own data, user interface, and logic, and can be mapped cleanly to one or more 
        business capabilities (e.g., payroll processing, incident management).
        
        **Technology**  
        The underlying technical building blocks—languages, frameworks, protocols, databases, devices, 
        and infrastructure services—that architects combine to build, run, and secure applications. 
        These components are typically abstracted away from end-users.
        
        **Platform**  
        A managed environment that bundles multiple technologies and shared services, offering a stable 
        foundation on which many applications can be developed, deployed, and operated. Standardises 
        common concerns like identity, integration, observability, and deployment pipelines.
        """)
    
    # File upload section
    st.markdown("## 📁 Upload Applications Data")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file containing applications to categorise",
        type=['xlsx', 'xls', 'xlsm', 'csv'],
        help="Upload a spreadsheet containing your application portfolio data"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            else:
                xls = pd.ExcelFile(uploaded_file)
                sheet_name = st.selectbox("Select sheet to load", xls.sheet_names)
                df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Convert all columns to string to prevent PyArrow errors
            df = df.astype(str)
            df = df.replace('nan', pd.NA)
            
            # Create clean display data
            display_df = df.copy()
            display_df = display_df.fillna('')
            
            st.markdown("### 📋 Data Preview")
            st.dataframe(display_df.head(10))
            
            # Column selection
            st.markdown("### 🔧 Column Selection")
            
            col1, col2 = st.columns(2)
            
            with col1:
                id_column = st.selectbox(
                    "Select Application ID column:",
                    df.columns.tolist(),
                    help="Choose the column containing unique identifiers for each application"
                )
            
            with col2:
                description_columns = st.multiselect(
                    "Select description columns:",
                    df.columns.tolist(),
                    help="Choose one or more columns that describe the applications (will be combined for analysis)"
                )
            
            if id_column and description_columns:
                # Additional context section
                st.markdown("### 📝 Additional Context (Optional)")
                additional_context = st.text_area(
                    "Provide any additional context that might help with categorisation:",
                    placeholder="e.g., Focus on distinguishing between platforms and applications, consider cloud-native solutions, emphasise business function alignment...",
                    help="Optional context to improve AI categorisation accuracy",
                    height=80
                )
                
                # Batch processing configuration
                st.markdown("### ⚙️ Processing Configuration")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    batch_size = st.selectbox(
                        "Batch Size:",
                        [5, 10, 15, 20, 25],
                        index=1,
                        help="Number of applications to process per batch. Smaller batches are more reliable but slower."
                    )
                
                with col2:
                    total_records = len(df)
                    estimated_batches = math.ceil(total_records / batch_size)
                    st.metric("Estimated Batches", estimated_batches)
                
                # Process button
                if st.button("🚀 Categorise Applications", use_container_width=True):
                    if not description_columns:
                        st.error("❌ Please select at least one description column.")
                    else:
                        categorise_applications(df, id_column, description_columns, additional_context, batch_size)
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.error("Please ensure your file is a valid Excel or CSV file with proper formatting.")

def categorise_applications(df, id_column, description_columns, additional_context, batch_size):
    """Process application categorisation with AI"""
    
    # Prepare data
    df_clean = df.copy()
    
    # Combine description columns
    df_clean['combined_description'] = df_clean[description_columns].fillna('').agg(' | '.join, axis=1)
    
    # Create processing batches
    total_records = len(df_clean)
    num_batches = math.ceil(total_records / batch_size)
    
    results = []
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    st.markdown("## 🔄 Processing Application Categorisation")
    
    if additional_context.strip():
        st.info(f"ℹ️ Using additional context: {additional_context}")
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, total_records)
        batch_df = df_clean.iloc[start_idx:end_idx]
        
        status_text.text(f"Processing batch {batch_num + 1} of {num_batches} ({len(batch_df)} applications)")
        
        # Prepare batch data for AI
        batch_data = []
        for _, row in batch_df.iterrows():
            app_id = row[id_column]
            description = row['combined_description']
            batch_data.append(f"ID: {app_id} | Description: {description}")
        
        batch_text = "\n".join(batch_data)
        
        # Create AI prompt
        context_section = f"Additional Context: {additional_context}\n\n" if additional_context.strip() else ""
        
        prompt = f"""You are a senior enterprise architect with expertise in application portfolio management and technology categorisation.

Analyse each application/system and categorise it as exactly one of: Application, Technology, or Platform.

{context_section}Definitions:
- Application: A discrete software solution that delivers specific business functions to defined user groups. Has its own data, user interface, and logic. Maps to business capabilities (e.g., payroll processing, incident management).
- Technology: Underlying technical building blocks—languages, frameworks, protocols, databases, devices, infrastructure services. Typically abstracted from end-users.
- Platform: A managed environment bundling multiple technologies and shared services. Provides stable foundation for developing, deploying, and operating applications. Standardises common concerns like identity, integration, observability.

Return ONLY the results in this exact format (one line per application):
ApplicationID,Category

Applications to categorise:
{batch_text}"""

        try:
            # Call AI model
            message = HumanMessage(content=prompt)
            response = model.invoke([message])
            ai_response = response.content.strip()
            
            # Parse results
            for line in ai_response.split('\n'):
                line = line.strip()
                if line and ',' in line:
                    try:
                        parts = line.split(',', 1)
                        if len(parts) == 2:
                            app_id = parts[0].strip()
                            category = parts[1].strip()
                            
                            # Clean app_id - remove any leading characters
                            import re
                            app_id = re.sub(r'^[^a-zA-Z0-9]*', '', app_id)
                            app_id = re.sub(r'[^a-zA-Z0-9_\-\.]*$', '', app_id)
                            
                            # Validate category
                            if category in ['Application', 'Technology', 'Platform']:
                                # Validate application ID exists in source data
                                if app_id in df_clean[id_column].astype(str).values:
                                    results.append({
                                        'Application_ID': app_id,
                                        'Category': category
                                    })
                    except Exception as e:
                        st.warning(f"⚠️ Could not parse response line: {line}")
                        continue
        
        except Exception as e:
            st.error(f"❌ Error processing batch {batch_num + 1}: {str(e)}")
            continue
        
        # Update progress
        progress = (batch_num + 1) / num_batches
        progress_bar.progress(progress)
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Display results
    if results:
        results_df = pd.DataFrame(results)
        
        st.markdown("## ✅ Categorisation Complete!")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_categorised = len(results_df)
        applications_count = len(results_df[results_df['Category'] == 'Application'])
        technologies_count = len(results_df[results_df['Category'] == 'Technology'])
        platforms_count = len(results_df[results_df['Category'] == 'Platform'])
        
        with col1:
            st.metric("Total Categorised", total_categorised)
        with col2:
            st.metric("Applications", applications_count)
        with col3:
            st.metric("Technologies", technologies_count)
        with col4:
            st.metric("Platforms", platforms_count)
        
        # Display results table
        st.markdown("### 📊 Categorisation Results")
        st.dataframe(results_df, use_container_width=True)
        
        # Create Excel download
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            # Main results
            results_df.to_excel(writer, sheet_name='Application_Categories', index=False)
            
            # Summary statistics
            summary_data = {
                'Category': ['Application', 'Technology', 'Platform', 'Total'],
                'Count': [applications_count, technologies_count, platforms_count, total_categorised],
                'Percentage': [
                    f"{(applications_count/total_categorised*100):.1f}%" if total_categorised > 0 else "0%",
                    f"{(technologies_count/total_categorised*100):.1f}%" if total_categorised > 0 else "0%",
                    f"{(platforms_count/total_categorised*100):.1f}%" if total_categorised > 0 else "0%",
                    "100%"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        excel_buffer.seek(0)
        
        # Download button
        st.download_button(
            label="📥 Download Categorisation Results",
            data=excel_buffer.getvalue(),
            file_name="application_categorisation_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.success(f"✅ Successfully categorised {total_categorised} applications!")
        
    else:
        st.warning("⚠️ No valid categorisations were generated. Please check your data and try again.")
