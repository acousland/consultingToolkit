import streamlit as st
import pandas as pd
from navigation import render_breadcrumbs
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model, pain_point_impact_estimation_prompt

def pain_point_impact_estimation_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🔍 Pain Point Toolkit", "Pain Point Toolkit"), ("📊 Pain Point Impact Estimation", None)])
    
    st.markdown("## 📊 Pain Point Impact Estimation")
    st.markdown("_Assess the business impact of identified pain points_")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'xls', 'xlsm'], key="impact_file_upload")

    if uploaded_file is not None:
        # Read the Excel file and get sheet names
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            sheet_names = excel_data.sheet_names
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
            return
        
        # Sheet selection
        selected_sheet = st.selectbox("Select a sheet:", sheet_names, key="impact_sheet_select")
        
        if selected_sheet:
            # Read the selected sheet
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            
            # Clean the dataframe to avoid PyArrow conversion issues
            # Convert all columns to string type to ensure compatibility
            for col in df.columns:
                df[col] = df[col].astype(str)
            
            # Replace 'nan' strings back to actual NaN for better handling
            df = df.replace('nan', pd.NA)
            
            st.markdown(f"**Sheet:** {selected_sheet}")
            st.markdown(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
            
            # Show preview
            with st.expander("📋 Preview Data", expanded=True):
                st.dataframe(df.head(10))
            
            # Column selection
            st.markdown("### Column Selection")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # ID column selection
                id_column = st.selectbox(
                    "Select ID Column:",
                    options=df.columns.tolist(),
                    key="impact_id_column"
                )
            
            with col2:
                # Description columns selection
                description_columns = st.multiselect(
                    "Select Description Column(s):",
                    options=[col for col in df.columns.tolist() if col != id_column],
                    key="impact_description_columns"
                )
            
            if id_column and description_columns:
                # Context input
                st.markdown("### Business Context")
                st.markdown("_Optionally provide key contextual information to help the AI assess business impact more accurately._")
                
                context = st.text_area(
                    "Enter business context (optional - e.g., industry type, company size, strategic priorities, regulatory environment):",
                    placeholder="e.g., We are a mid-size financial services company focused on digital transformation. Key priorities include customer experience, regulatory compliance, and operational efficiency. Any disruptions to customer-facing systems or compliance processes have high business impact.",
                    height=120,
                    key="impact_context"
                )
                
                # Sample of data that will be processed
                sample_data = df[[id_column] + description_columns].head(5)
                
                # Clean sample data for display
                sample_display = sample_data.copy()
                for col in sample_display.columns:
                    sample_display[col] = sample_display[col].astype(str)
                sample_display = sample_display.replace('nan', '')
                sample_display = sample_display.replace('<NA>', '')
                
                st.markdown("### 📋 Data to be Processed")
                st.dataframe(sample_display)
                
                st.markdown(f"**Total records to process:** {len(df)}")
                
                # Batch size configuration
                st.markdown("### ⚙️ Processing Configuration")
                col_batch1, col_batch2 = st.columns(2)
                
                with col_batch1:
                    batch_size = st.selectbox(
                        "Batch Size:",
                        options=[5, 10, 15, 20, 25],
                        index=1,  # Default to 10
                        help="Number of pain points to process in each batch. Smaller batches are more reliable but slower.",
                        key="impact_batch_size"
                    )
                
                with col_batch2:
                    estimated_batches = (len(df) + batch_size - 1) // batch_size
                    st.metric("Estimated Batches", estimated_batches)
                
                # Process button
                if st.button("🚀 Estimate Impact", key="start_impact_estimation", type="primary"):
                    # Process the impact estimation (context is optional)
                    process_impact_estimation(df, id_column, description_columns, context, batch_size)

def process_impact_estimation(df, id_column, description_columns, context, batch_size=10):
    """Process pain points and estimate their business impact"""
    
    st.markdown("### 🔄 Processing Impact Assessment")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_rows = len(df)
    
    st.info(f"📊 Processing {total_rows} pain points in batches of {batch_size}...")
    
    batch_size = batch_size  # Use the configured batch size
    total_batches = (total_rows + batch_size - 1) // batch_size
    
    for i in range(0, total_rows, batch_size):
        batch_end = min(i + batch_size, total_rows)
        batch_df = df.iloc[i:batch_end]
        current_batch = i // batch_size + 1
        
        # Prepare batch text
        batch_text = ""
        batch_ids = []
        
        for _, row in batch_df.iterrows():
            pain_point_id = row[id_column]
            batch_ids.append(pain_point_id)
            
            # Combine description columns
            description_parts = []
            for col in description_columns:
                if pd.notna(row[col]) and str(row[col]).strip():
                    description_parts.append(str(row[col]).strip())
            
            combined_description = " | ".join(description_parts)
            batch_text += f"{pain_point_id}: {combined_description}\n"
        
        status_text.text(f"🔄 Processing batch {current_batch} of {total_batches} ({len(batch_df)} pain points)...")
        
        try:
            # Get AI response for the batch using the prompt template
            # Handle optional context
            if context and context.strip():
                context_section = f"Business Context:\n{context}"
                context_instruction = "Consider the business context provided when making your assessment."
            else:
                context_section = "No specific business context provided - use general business impact principles."
                context_instruction = "Use general business impact principles for your assessment."
            
            prompt_input = pain_point_impact_estimation_prompt.format(
                context_section=context_section,
                context_instruction=context_instruction,
                pain_points=batch_text
            )
            messages = [HumanMessage(content=prompt_input)]
            response = model.invoke(messages)
            impact_assessments = response.content.strip().split('\n')
            
            # Parse results
            for j, pain_point_id in enumerate(batch_ids):
                if j < len(impact_assessments):
                    impact_text = impact_assessments[j].strip()
                    # Extract impact level (handle various response formats)
                    if 'HIGH' in impact_text.upper():
                        impact = 'High'
                    elif 'MEDIUM' in impact_text.upper():
                        impact = 'Medium'
                    elif 'LOW' in impact_text.upper():
                        impact = 'Low'
                    else:
                        impact = 'Medium'  # Default fallback
                else:
                    impact = 'Medium'  # Default fallback
                
                results.append({
                    'Pain Point ID': pain_point_id,
                    'Business Impact': impact
                })
        
        except Exception as e:
            st.error(f"❌ Error processing batch {current_batch}: {str(e)}")
            # Add default impacts for this batch
            for pain_point_id in batch_ids:
                results.append({
                    'Pain Point ID': pain_point_id,
                    'Business Impact': 'Medium'  # Default fallback
                })
        
        # Update progress
        progress = min((batch_end / total_rows), 1.0)
        progress_bar.progress(progress)
    
    # Clear status
    status_text.empty()
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Display results
    status_text.text("✅ Impact estimation completed!")
    progress_bar.progress(1.0)
    
    st.success(f"🎉 Successfully estimated impact for {len(results_df)} pain points!")
    
    # Show results summary
    st.markdown("### 📊 Impact Distribution")
    impact_counts = results_df['Business Impact'].value_counts()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High Impact", impact_counts.get('High', 0))
    with col2:
        st.metric("🟡 Medium Impact", impact_counts.get('Medium', 0))
    with col3:
        st.metric("🟢 Low Impact", impact_counts.get('Low', 0))
    
    # Show results table
    st.markdown("### 📋 Impact Assessment Results")
    
    # Clean results for display
    results_display = results_df.copy()
    for col in results_display.columns:
        results_display[col] = results_display[col].astype(str)
    results_display = results_display.replace('nan', '')
    results_display = results_display.replace('<NA>', '')
    
    st.dataframe(results_display, use_container_width=True)
    
    # Download button
    st.markdown("### ⬇️ Download Results")
    
    # Create Excel file for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='Impact Assessment', index=False)
        
        # Add summary sheet
        summary_df = pd.DataFrame({
            'Impact Level': ['High', 'Medium', 'Low'],
            'Count': [impact_counts.get('High', 0), impact_counts.get('Medium', 0), impact_counts.get('Low', 0)],
            'Percentage': [
                f"{(impact_counts.get('High', 0) / len(results_df) * 100):.1f}%" if len(results_df) > 0 else "0%",
                f"{(impact_counts.get('Medium', 0) / len(results_df) * 100):.1f}%" if len(results_df) > 0 else "0%",
                f"{(impact_counts.get('Low', 0) / len(results_df) * 100):.1f}%" if len(results_df) > 0 else "0%"
            ]
        })
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    
    st.download_button(
        label="📊 Download Impact Assessment Results",
        data=output.getvalue(),
        file_name="pain_point_impact_assessment.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_impact_results"
    )
    
    st.markdown("---")
    st.markdown("**📁 File Contents:**")
    st.markdown("• **Impact Assessment** sheet: Pain Point ID and Business Impact classification")
    st.markdown("• **Summary** sheet: Impact distribution statistics")
