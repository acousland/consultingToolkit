import streamlit as st
import pandas as pd
import io
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs


def logical_application_model_generator_page():
    render_breadcrumbs([
        ("🏠 Home", "Home"),
        ("🏗️ Applications Toolkit", "Applications Toolkit"),
        ("🏛️ Logical Application Model Generator", None)
    ])
    
    st.markdown("# 🏛️ Logical Application Model Generator")
    
    st.markdown("""
    Generate a logical application model by categorizing applications into high-level architectural groups 
    based on their purpose and functionality. This creates a taxonomy of applications based on their 
    architectural role (e.g., Digital Experience Platform, Customer Data Platform, Data Integration Pipeline Tool).
    """)
    
    st.markdown("---")
    
    # Company Context Section
    st.markdown("## 📋 Step 1: Company Context")
    st.markdown("Provide context about the organization to help generate relevant application categories.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Company Dossier Upload")
        company_file = st.file_uploader(
            "Upload company dossier (PDF, TXT, Word, JSON, or XML)",
            type=['pdf', 'txt', 'docx', 'json', 'xml'],
            key="company_dossier",
            help="Upload a document containing company information, business context, or organizational overview"
        )
        
        if company_file:
            st.success(f"✅ Uploaded: {company_file.name}")
    
    with col2:
        st.markdown("### Company Description")
        company_description = st.text_area(
            "Enter company description:",
            placeholder="Describe the organization, industry, business model, key operations, etc...",
            height=150,
            help="Provide context about the company's business, industry, and key operational areas"
        )
    
    st.markdown("---")
    
    # Applications Data Section
    st.markdown("## 📊 Step 2: Applications Data")
    st.markdown("Upload or enter information about the applications to be categorized.")
    
    # File upload option
    st.markdown("### Upload Applications File")
    apps_file = st.file_uploader(
        "Upload applications list (Excel or CSV)",
        type=['xlsx', 'xls', 'xlsm', 'csv'],
        key="applications_file",
        help="Upload a file containing application names and descriptions"
    )
    
    applications_df = None
    
    if apps_file:
        try:
            # Handle different file types
            if apps_file.type == "text/csv":
                applications_df = pd.read_csv(apps_file)
                available_sheets = ["CSV File"]
                selected_sheet = "CSV File"
            else:
                # For Excel files, get available sheets
                excel_file = pd.ExcelFile(apps_file)
                available_sheets = excel_file.sheet_names
                
                # Sheet selection
                st.markdown("#### Select Worksheet")
                selected_sheet = st.selectbox(
                    "Choose worksheet:",
                    available_sheets,
                    help="Select the worksheet containing your applications data"
                )
                
                # Load the selected sheet
                applications_df = pd.read_excel(apps_file, sheet_name=selected_sheet)
            
            st.success(f"✅ Loaded {len(applications_df)} rows from '{selected_sheet}'")
            
            # Show basic info about the data
            st.info(f"📊 Data shape: {applications_df.shape[0]} rows × {applications_df.shape[1]} columns")
            
            # Column selection
            st.markdown("#### Select Columns")
            col_name_col, col_desc_col = st.columns(2)
            
            with col_name_col:
                name_column = st.selectbox(
                    "Application Name Column:",
                    applications_df.columns.tolist(),
                    help="Select the column containing application names"
                )
            
            with col_desc_col:
                desc_columns = st.multiselect(
                    "Description Columns:",
                    applications_df.columns.tolist(),
                    help="Select one or more columns containing application descriptions, purposes, or details. Multiple columns will be concatenated together."
                )
            
            # Show concatenation preview if multiple description columns selected
            if len(desc_columns) > 1:
                st.markdown("#### Description Concatenation Preview")
                concat_separator = st.selectbox(
                    "Separator for concatenating descriptions:",
                    [" | ", " - ", " ", "\\n", "; "],
                    index=0,
                    help="Choose how to join multiple description columns"
                )
                
                # Show preview of concatenated descriptions
                if name_column and desc_columns:
                    preview_sample = applications_df.head(3)
                    concatenated_preview = []
                    
                    for _, row in preview_sample.iterrows():
                        app_name = row[name_column]
                        concatenated_desc = concat_separator.join([
                            str(row[col]) for col in desc_columns 
                            if pd.notna(row[col]) and str(row[col]).strip()
                        ])
                        concatenated_preview.append({
                            'Application': app_name,
                            'Concatenated Description': concatenated_desc
                        })
                    
                    st.markdown("**Sample of concatenated descriptions:**")
                    st.dataframe(pd.DataFrame(concatenated_preview), use_container_width=True)
            
            # Data preview
            if name_column and desc_columns:
                st.markdown("#### Data Preview")
                preview_df = applications_df[[name_column] + desc_columns].head(10)
                st.dataframe(preview_df, use_container_width=True)
                
                # Show summary statistics
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    missing_names = applications_df[name_column].isna().sum()
                    st.metric("Missing Application Names", missing_names)
                
                with col_stats2:
                    missing_descriptions = sum([applications_df[col].isna().sum() for col in desc_columns])
                    st.metric("Total Missing Description Values", missing_descriptions)
        
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    st.markdown("---")
    
    # Generation Section
    if applications_df is not None and 'name_column' in locals() and 'desc_columns' in locals():
        st.markdown("## 🤖 Step 3: Generate Logical Application Model")
        
        col_settings1, col_settings2 = st.columns(2)
        
        with col_settings1:
            num_categories = st.slider(
                "Target number of categories:",
                min_value=3,
                max_value=15,
                value=8,
                help="Suggested number of high-level application categories to create"
            )
        
        with col_settings2:
            include_context = st.checkbox(
                "Include company context in analysis",
                value=True,
                help="Use company information to generate industry-relevant categories"
            )
        
        if st.button("🚀 Generate Logical Application Model", type="primary"):
            with st.spinner("Analyzing applications and generating logical model..."):
                try:
                    # Prepare applications data with concatenated descriptions
                    apps_data = []
                    
                    # Determine separator if multiple description columns
                    separator = " | "  # Default
                    if len(desc_columns) > 1 and 'concat_separator' in locals():
                        separator = concat_separator
                    
                    for _, row in applications_df.iterrows():
                        app_name = row[name_column]
                        
                        # Concatenate description columns
                        if len(desc_columns) == 1:
                            app_desc = str(row[desc_columns[0]]) if pd.notna(row[desc_columns[0]]) else ""
                        else:
                            desc_parts = [
                                str(row[col]) for col in desc_columns 
                                if pd.notna(row[col]) and str(row[col]).strip()
                            ]
                            app_desc = separator.join(desc_parts)
                        
                        if app_desc.strip():  # Only include if we have a description
                            apps_data.append(f"- {app_name}: {app_desc}")
                    
                    apps_text = "\\n".join(apps_data)
                    
                    # Prepare context
                    context_text = ""
                    if include_context and company_description:
                        context_text = f"Company Context: {company_description}\\n\\n"
                    
                    # Create prompt
                    prompt = f"""You are a senior enterprise architect specializing in application portfolio management and logical application modeling.

{context_text}Please analyze the following applications and create a logical application model with the following outputs:

1. **High-Level Application Categories**: Create {num_categories} logical categories that group applications by their architectural purpose and functionality (e.g., "Digital Experience Platforms", "Customer Data Management", "Integration & APIs", "Analytics & Business Intelligence", etc.)

2. **Application Categorization**: Assign each application to the most appropriate category

3. **Category Definitions**: Provide a clear definition for each category explaining its purpose and typical characteristics

4. **Architectural Insights**: Highlight any gaps, overlaps, or architectural observations

Applications to analyze:
{apps_text}

Format your response as:
## Logical Application Categories

### [Category Name]
**Definition:** [Clear definition of category purpose]
**Applications:** [List applications in this category]

[Repeat for each category]

## Architectural Analysis
[Provide insights about the application portfolio, gaps, overlaps, recommendations]"""

                    # Generate response
                    response = model.invoke([HumanMessage(content=prompt)])
                    
                    # Display results
                    st.markdown("## 📊 Generated Logical Application Model")
                    st.markdown(response.content)
                    
                    # Create downloadable summary
                    summary_data = {
                        'Application': applications_df[name_column].tolist(),
                        'Description': [" | ".join([str(row[col]) for col in desc_columns if pd.notna(row[col])]) 
                                      for _, row in applications_df.iterrows()]
                    }
                    
                    summary_df = pd.DataFrame(summary_data)
                    
                    # Add export functionality
                    st.markdown("---")
                    st.markdown("## 📥 Export Results")
                    
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        # Export application summary
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            summary_df.to_excel(writer, sheet_name='Applications', index=False)
                        
                        st.download_button(
                            label="📊 Download Applications Summary (Excel)",
                            data=excel_buffer.getvalue(),
                            file_name="logical_application_model_summary.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    with col_export2:
                        # Export full analysis
                        analysis_text = f"""Logical Application Model Analysis
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

{response.content}

Application List:
{apps_text}
"""
                        st.download_button(
                            label="📄 Download Full Analysis (Text)",
                            data=analysis_text,
                            file_name="logical_application_model_analysis.txt",
                            mime="text/plain"
                        )
                
                except Exception as e:
                    st.error(f"Error generating logical application model: {e}")
                    st.markdown("**Troubleshooting suggestions:**")
                    st.markdown("- Check your OpenAI API configuration in the Admin Tool")
                    st.markdown("- Ensure applications data is properly formatted")
                    st.markdown("- Try with fewer applications if the request is too large")
    
    else:
        st.info("👆 Please upload applications data to generate the logical application model.")
