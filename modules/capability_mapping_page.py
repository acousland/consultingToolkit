import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model

def capability_mapping_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_mapping"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point to Capability Mapping")
    st.markdown("Upload pain points and capabilities spreadsheets to create ID-based mappings.")
    
    # Create two columns for side-by-side uploads
    col1, col2 = st.columns(2)
    
    # Initialize session state for dataframes
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
            pain_text_col = st.selectbox(
                "Select Pain Point text column", 
                pain_points_df.columns,
                key="pain_text_col"
            )
            
            # Store column selections in session state (but not with widget key names)
            st.session_state['pain_columns']['id'] = pain_id_col
            st.session_state['pain_columns']['text'] = pain_text_col
    
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
            cap_text_col = st.selectbox(
                "Select Capability text column", 
                capabilities_df.columns,
                key="cap_text_col"
            )
            
            # Store column selections in session state (but not with widget key names)
            st.session_state['cap_columns']['id'] = cap_id_col
            st.session_state['cap_columns']['text'] = cap_text_col
    
    # Mapping section
    if (st.session_state['pain_points_df'] is not None and 
        st.session_state['capabilities_df'] is not None and
        st.session_state['pain_columns']['id'] is not None and 
        st.session_state['cap_columns']['id'] is not None):
        
        st.markdown("---")
        st.markdown("### 🔗 Generate Mappings")
        
        # Additional context input
        additional_context = st.text_area(
            "Additional context for AI mapping (optional):",
            placeholder="e.g., Prioritize digital capabilities, focus on customer-facing solutions, consider budget constraints..."
        )
        
        if st.button("Generate AI Mappings", type="primary"):
            pain_points_df = st.session_state['pain_points_df']
            capabilities_df = st.session_state['capabilities_df']
            pain_id_col = st.session_state['pain_columns']['id']
            pain_text_col = st.session_state['pain_columns']['text']
            cap_id_col = st.session_state['cap_columns']['id']
            cap_text_col = st.session_state['cap_columns']['text']
            
            mappings = []
            
            with st.spinner("Generating mappings with AI..."):
                progress_bar = st.progress(0)
                
                for idx, pain_row in pain_points_df.iterrows():
                    pain_id = pain_row[pain_id_col]
                    pain_text = pain_row[pain_text_col]
                    
                    # Create mapping prompt for this specific pain point
                    mapping_prompt = f"""You are an expert management consultant specializing in organizational capabilities.

Your task: Match the given pain point to the MOST APPROPRIATE capability from the provided list.

Pain Point to Match:
ID: {pain_id}
Text: {pain_text}

Available Capabilities:
"""
                    
                    for _, cap_row in capabilities_df.iterrows():
                        cap_id = cap_row[cap_id_col]
                        cap_text = cap_row[cap_text_col]
                        mapping_prompt += f"- {cap_id}: {cap_text}\n"
                    
                    mapping_prompt += f"""
Additional Context: {additional_context}

Instructions:
1. Analyze the pain point and determine which capability would best address it
2. Consider both direct solutions and preventive capabilities
3. Choose the single most appropriate capability ID
4. Return ONLY the capability ID (e.g., CAP001) - no explanations or additional text

Capability ID:"""
                    
                    # Get AI response
                    output = model.invoke([HumanMessage(content=mapping_prompt)])
                    mapped_capability_id = output.content.strip()
                    
                    # Clean up the response to get just the ID
                    if ':' in mapped_capability_id:
                        mapped_capability_id = mapped_capability_id.split(':')[-1].strip()
                    
                    mappings.append({
                        'Pain_Point_ID': pain_id,
                        'Capability_ID': mapped_capability_id,
                        'Pain_Point_Text': pain_text
                    })
                    
                    # Update progress
                    progress = (idx + 1) / len(pain_points_df)
                    progress_bar.progress(progress)
                
                progress_bar.progress(1.0)
            
            # Create mappings dataframe
            mappings_df = pd.DataFrame(mappings)
            
            # Add capability text for reference
            cap_lookup = dict(zip(capabilities_df[cap_id_col], capabilities_df[cap_text_col]))
            mappings_df['Capability_Text'] = mappings_df['Capability_ID'].map(cap_lookup)
            
            st.session_state['mappings_df'] = mappings_df
            
            st.markdown("### 📊 Mapping Results")
            st.dataframe(mappings_df)
            
            # Download button
            buffer = BytesIO()
            mappings_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            
            st.download_button(
                label="� Download Mappings as Excel",
                data=buffer.getvalue(),
                file_name="pain_point_capability_mappings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Display previously generated mappings if they exist
    if 'mappings_df' in st.session_state and st.session_state['mappings_df'] is not None:
        st.markdown("---")
        st.markdown("### 📋 Previous Mappings")
        st.dataframe(st.session_state['mappings_df'])
        
        # Re-download button for previous mappings
        buffer = BytesIO()
        st.session_state['mappings_df'].to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        
        st.download_button(
            label="📥 Re-download Previous Mappings",
            data=buffer.getvalue(),
            file_name="pain_point_capability_mappings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="redownload_mappings"
        )
