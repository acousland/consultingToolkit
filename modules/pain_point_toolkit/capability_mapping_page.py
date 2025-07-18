import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from prompts import PAIN_POINT_CAPABILITY_MAPPING_PROMPT
from navigation import render_breadcrumbs

def capability_mapping_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🔍 Pain Point Toolkit", "Pain Point Toolkit"), ("🎯 Capability Mapping", None)])
    
    st.markdown("## Pain Point to Capability Mapping")
    st.markdown("Upload pain points and capabilities spreadsheets to create ID-based mappings.")
    
    # Create two columns for side-by-side uploads
    col1, col2 = st.columns(2)
    
    # Initialise session state for dataframes
    if 'pain_points_df' not in st.session_state:
        st.session_state['pain_points_df'] = None
    if 'capabilities_df' not in st.session_state:
        st.session_state['capabilities_df'] = None
    if 'pain_columns' not in st.session_state:
        st.session_state['pain_columns'] = {'id': None, 'text': None}
    if 'cap_columns' not in st.session_state:
        st.session_state['cap_columns'] = {'id': None, 'text': None}
    
    with col1:
        st.markdown("### 📋 Pain Points Spreadsheet")
        pain_points_file = st.file_uploader(
            "Upload Pain Points Excel file", 
            type=['xlsx', 'xls', 'xlsm'],
            key="pain_points_upload"
        )
        
        if pain_points_file is not None:
            # Load pain points file
            xls = pd.ExcelFile(pain_points_file)
            pain_sheet = st.selectbox("Select sheet for pain points", xls.sheet_names, key="pain_sheet")
            pain_points_df = pd.read_excel(xls, sheet_name=pain_sheet)
            st.session_state['pain_points_df'] = pain_points_df
            
            st.write("**Preview:**")
            st.dataframe(pain_points_df.head())
            
            # Column selection for pain points
            pain_id_col = st.selectbox(
                "Select Pain Point ID column", 
                pain_points_df.columns,
                key="pain_id_col"
            )
            pain_text_cols = st.multiselect(
                "Select Pain Point text columns (will be concatenated)", 
                pain_points_df.columns,
                key="pain_text_cols",
                help="Select one or more columns to describe the pain point (e.g., title, description, details)"
            )
            
            # Store column selections in session state (but not with widget key names)
            st.session_state['pain_columns']['id'] = pain_id_col
            st.session_state['pain_columns']['text'] = pain_text_cols
    
    with col2:
        st.markdown("### ⚙️ Capabilities Spreadsheet")
        capabilities_file = st.file_uploader(
            "Upload Capabilities Excel file", 
            type=['xlsx', 'xls', 'xlsm'],
            key="capabilities_upload"
        )
        
        if capabilities_file is not None:
            # Load capabilities file
            xls = pd.ExcelFile(capabilities_file)
            cap_sheet = st.selectbox("Select sheet for capabilities", xls.sheet_names, key="cap_sheet")
            capabilities_df = pd.read_excel(xls, sheet_name=cap_sheet)
            st.session_state['capabilities_df'] = capabilities_df
            
            st.write("**Preview:**")
            st.dataframe(capabilities_df.head())
            
            # Column selection for capabilities
            cap_id_col = st.selectbox(
                "Select Capability ID column", 
                capabilities_df.columns,
                key="cap_id_col"
            )
            cap_text_cols = st.multiselect(
                "Select Capability text columns (will be concatenated)", 
                capabilities_df.columns,
                key="cap_text_cols",
                help="Select one or more columns to describe the capability (e.g., name, description, details)"
            )
            
            # Store column selections in session state (but not with widget key names)
            st.session_state['cap_columns']['id'] = cap_id_col
            st.session_state['cap_columns']['text'] = cap_text_cols
    
    # Mapping section
    if (st.session_state['pain_points_df'] is not None and 
        st.session_state['capabilities_df'] is not None and
        st.session_state['pain_columns']['id'] is not None and 
        st.session_state['cap_columns']['id'] is not None and
        st.session_state['pain_columns']['text'] and  # Check if list is not empty
        st.session_state['cap_columns']['text']):  # Check if list is not empty
        
        st.markdown("---")
        st.markdown("### 🔗 Generate Mappings")
        
        # Additional context input
        additional_context = st.text_area(
            "Additional context for AI mapping (optional):",
            placeholder="e.g., Prioritize digital capabilities, focus on customer-facing solutions, consider budget constraints..."
        )
        
        # Batch size control
        batch_size = st.number_input(
            'Batch size (number of pain points to process together)', 
            min_value=1, max_value=50, value=10,
            help="Larger batches are faster but may be less accurate. Smaller batches are more precise but slower."
        )
        
        if st.button("Generate AI Mappings", type="primary"):
            pain_points_df = st.session_state['pain_points_df']
            capabilities_df = st.session_state['capabilities_df']
            pain_id_col = st.session_state['pain_columns']['id']
            pain_text_cols = st.session_state['pain_columns']['text']
            cap_id_col = st.session_state['cap_columns']['id']
            cap_text_cols = st.session_state['cap_columns']['text']
            
            mappings = []
            
            with st.spinner("Generating mappings with AI..."):
                progress_bar = st.progress(0)
                total_pain_points = len(pain_points_df)
                
                # Process in batches
                for batch_start in range(0, total_pain_points, batch_size):
                    batch_end = min(batch_start + batch_size, total_pain_points)
                    batch_df = pain_points_df.iloc[batch_start:batch_end]
                    
                    st.write(f"Processing pain points {batch_start + 1} to {batch_end} of {total_pain_points}")
                    
                    # Build prompt using template
                    pain_points_text = ""
                    for _, pain_row in batch_df.iterrows():
                        pain_id = pain_row[pain_id_col]
                        pain_text_parts = []
                        for col in pain_text_cols:
                            if pd.notna(pain_row[col]):
                                pain_text_parts.append(str(pain_row[col]))
                        pain_text = " ".join(pain_text_parts)
                        pain_points_text += f"- {pain_id}: {pain_text}\n"

                    capabilities_lines = []
                    for _, cap_row in capabilities_df.iterrows():
                        cap_id = cap_row[cap_id_col]
                        cap_text_parts = []
                        for col in cap_text_cols:
                            if pd.notna(cap_row[col]):
                                cap_text_parts.append(str(cap_row[col]))
                        cap_text = " ".join(cap_text_parts)
                        capabilities_lines.append(f"- {cap_id}: {cap_text}")
                    capabilities_text = "\n".join(capabilities_lines)

                    batch_mapping_prompt = PAIN_POINT_CAPABILITY_MAPPING_PROMPT.format(
                        pain_points=pain_points_text,
                        capabilities=capabilities_text,
                        additional_context=additional_context,
                    )
                    
                    # Get AI response for the batch
                    output = model.invoke([HumanMessage(content=batch_mapping_prompt)])
                    batch_results = output.content.strip()
                    
                    # Parse the batch results
                    for line in batch_results.split('\n'):
                        line = line.strip()
                        if '->' in line:
                            try:
                                pain_point_id, capability_id = line.split('->')
                                pain_point_id = pain_point_id.strip()
                                capability_id = capability_id.strip()
                                
                                # Get the pain point text for reference
                                pain_text = ""
                                matching_rows = batch_df[batch_df[pain_id_col].astype(str) == str(pain_point_id)]
                                if not matching_rows.empty:
                                    # Concatenate selected pain point text columns
                                    pain_text_parts = []
                                    for col in pain_text_cols:
                                        if pd.notna(matching_rows.iloc[0][col]):
                                            pain_text_parts.append(str(matching_rows.iloc[0][col]))
                                    pain_text = ' '.join(pain_text_parts)
                                
                                mappings.append({
                                    'Pain_Point_ID': pain_point_id,
                                    'Capability_ID': capability_id,
                                    'Pain_Point_Text': pain_text
                                })
                            except ValueError:
                                # Skip malformed lines
                                continue
                    
                    # Update progress
                    progress = batch_end / total_pain_points
                    progress_bar.progress(progress)
                
                progress_bar.progress(1.0)
            
            # Create mappings dataframe
            mappings_df = pd.DataFrame(mappings)
            
            # Add capability text for reference (concatenate selected columns)
            cap_lookup = {}
            for _, cap_row in capabilities_df.iterrows():
                cap_id = cap_row[cap_id_col]
                cap_text_parts = []
                for col in cap_text_cols:
                    if pd.notna(cap_row[col]):
                        cap_text_parts.append(str(cap_row[col]))
                cap_text = ' '.join(cap_text_parts)
                cap_lookup[cap_id] = cap_text
            
            mappings_df['Capability_Text'] = mappings_df['Capability_ID'].map(cap_lookup)
            
            st.session_state['mappings_df'] = mappings_df
            
            st.markdown("### 📊 Mapping Results")
            st.dataframe(mappings_df)
            
            # Download button
            buffer = BytesIO()
            mappings_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Mappings as Excel",
                data=buffer.getvalue(),
                file_name="pain_point_capability_mappings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
