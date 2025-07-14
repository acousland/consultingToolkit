import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model

def strategy_capability_mapping_page():
    # Breadcrumb navigation as a single line with clickable elements
    breadcrumb_container = st.container()
    
    with breadcrumb_container:
        col1, col2, col3, col4, col5 = st.columns([1.2, 0.2, 2.8, 0.2, 3])
        
        with col1:
            if st.button("🏠 Home", key="breadcrumb_home", help="Go to Home"):
                st.session_state.page = "Home"
                st.rerun()
        
        with col2:
            st.markdown("**›**")
        
        with col3:
            if st.button("🎯 Strategy and Motivations Toolkit", key="breadcrumb_toolkit", help="Go to Strategy and Motivations Toolkit"):
                st.session_state.page = "Strategy and Motivations Toolkit"
                st.rerun()
        
        with col4:
            st.markdown("**›**")
        
        with col5:
            st.markdown("**🎯 Strategy to Capability Mapping**")
    
    st.markdown("---")
    
    st.markdown("## Strategy to Capability Mapping")
    st.markdown("Upload strategic initiatives and capabilities spreadsheets to create ID-based mappings.")
    
    # Create two columns for side-by-side uploads
    col1, col2 = st.columns(2)
    
    # Initialise session state for dataframes
    if 'strategies_df' not in st.session_state:
        st.session_state['strategies_df'] = None
    if 'capabilities_df' not in st.session_state:
        st.session_state['capabilities_df'] = None
    if 'strategy_columns' not in st.session_state:
        st.session_state['strategy_columns'] = {'id': None, 'text': None}
    if 'cap_columns' not in st.session_state:
        st.session_state['cap_columns'] = {'id': None, 'text': None}
    
    with col1:
        st.markdown("### 🎯 Strategic Initiatives Spreadsheet")
        strategies_file = st.file_uploader(
            "Upload Strategic Initiatives Excel file", 
            type=['xlsx', 'xls', 'xlsm'],
            key="strategies_upload"
        )
        
        if strategies_file is not None:
            # Load strategies file
            xls = pd.ExcelFile(strategies_file)
            strategy_sheet = st.selectbox("Select sheet for strategic initiatives", xls.sheet_names, key="strategy_sheet")
            strategies_df = pd.read_excel(xls, sheet_name=strategy_sheet)
            st.session_state['strategies_df'] = strategies_df
            
            st.write("**Preview:**")
            st.dataframe(strategies_df.head())
            
            # Column selection for strategies
            strategy_id_col = st.selectbox(
                "Select Strategic Initiative ID column", 
                strategies_df.columns,
                key="strategy_id_col"
            )
            strategy_text_cols = st.multiselect(
                "Select Strategic Initiative text columns (will be concatenated)", 
                strategies_df.columns,
                key="strategy_text_cols",
                help="Select one or more columns to describe the strategic initiative (e.g., title, description, objectives, outcomes)"
            )
            
            # Store column selections in session state (but not with widget key names)
            st.session_state['strategy_columns']['id'] = strategy_id_col
            st.session_state['strategy_columns']['text'] = strategy_text_cols
    
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
    if (st.session_state['strategies_df'] is not None and 
        st.session_state['capabilities_df'] is not None and
        st.session_state['strategy_columns']['id'] is not None and 
        st.session_state['cap_columns']['id'] is not None and
        st.session_state['strategy_columns']['text'] and  # Check if list is not empty
        st.session_state['cap_columns']['text']):  # Check if list is not empty
        
        st.markdown("---")
        st.markdown("### � Generate Mappings")
        
        # Additional context input
        additional_context = st.text_area(
            "Additional context for AI mapping (optional):",
            placeholder="e.g., Focus on digital transformation capabilities, prioritise customer-facing capabilities, consider implementation timeline constraints..."
        )
        
        # Batch size control
        batch_size = st.number_input(
            'Batch size (number of strategic initiatives to process together)', 
            min_value=1, max_value=50, value=10,
            help="Larger batches are faster but may be less accurate. Smaller batches are more precise but slower."
        )
        
        if st.button("Generate AI Mappings", type="primary"):
            strategies_df = st.session_state['strategies_df']
            capabilities_df = st.session_state['capabilities_df']
            strategy_id_col = st.session_state['strategy_columns']['id']
            strategy_text_cols = st.session_state['strategy_columns']['text']
            cap_id_col = st.session_state['cap_columns']['id']
            cap_text_cols = st.session_state['cap_columns']['text']
            
            mappings = []
            
            with st.spinner("Generating mappings with AI..."):
                progress_bar = st.progress(0)
                total_strategies = len(strategies_df)
                
                # Process in batches
                for batch_start in range(0, total_strategies, batch_size):
                    batch_end = min(batch_start + batch_size, total_strategies)
                    batch_df = strategies_df.iloc[batch_start:batch_end]
                    
                    st.write(f"Processing strategic initiatives {batch_start + 1} to {batch_end} of {total_strategies}")
                    
                    # Create batch mapping prompt
                    batch_mapping_prompt = f"""You are an expert strategy consultant specialising in organisational capabilities and strategic implementation.

Your task: Match each strategic initiative to the MOST APPROPRIATE capability from the provided list.

Strategic Initiatives to Match:
"""
                    
                    # Add all strategic initiatives in this batch
                    for _, strategy_row in batch_df.iterrows():
                        strategy_id = strategy_row[strategy_id_col]
                        # Concatenate selected strategy text columns
                        strategy_text_parts = []
                        for col in strategy_text_cols:
                            if pd.notna(strategy_row[col]):
                                strategy_text_parts.append(str(strategy_row[col]))
                        strategy_text = ' '.join(strategy_text_parts)
                        batch_mapping_prompt += f"- {strategy_id}: {strategy_text}\n"
                    
                    batch_mapping_prompt += f"""
Available Capabilities:
"""
                    
                    # Add all available capabilities
                    for _, cap_row in capabilities_df.iterrows():
                        cap_id = cap_row[cap_id_col]
                        # Concatenate selected capability text columns
                        cap_text_parts = []
                        for col in cap_text_cols:
                            if pd.notna(cap_row[col]):
                                cap_text_parts.append(str(cap_row[col]))
                        cap_text = ' '.join(cap_text_parts)
                        batch_mapping_prompt += f"- {cap_id}: {cap_text}\n"
                    
                    batch_mapping_prompt += f"""
Additional Context: {additional_context}

Instructions:
1. For each strategic initiative, analyse and determine which capabilities are required for successful implementation
2. Consider both enablement capabilities (that make the strategy possible) and execution capabilities (that deliver the strategy)
3. A strategy can map to 0, 1, or many capabilities - choose all that are necessary
4. Only return the Strategy ID and Capability ID - no additional text to save tokens
5. Return your response in this exact format:
- For strategies with no required capabilities: STRATEGIC_INITIATIVE_ID -> NONE
- For strategies with one capability: STRATEGIC_INITIATIVE_ID -> CAPABILITY_ID
- For strategies with multiple capabilities: STRATEGIC_INITIATIVE_ID -> CAPABILITY_ID1, CAPABILITY_ID2, CAPABILITY_ID3

Example format:
STRAT001 -> CAP003, CAP007
STRAT002 -> CAP012
STRAT003 -> NONE
STRAT004 -> CAP001, CAP005, CAP009

Mappings:"""
                    
                    # Get AI response for the batch
                    output = model.invoke([HumanMessage(content=batch_mapping_prompt)])
                    batch_results = output.content.strip()
                    
                    # Parse the batch results
                    for line in batch_results.split('\n'):
                        line = line.strip()
                        if '->' in line:
                            try:
                                strategy_id, capability_ids = line.split('->', 1)
                                strategy_id = strategy_id.strip()
                                capability_ids = capability_ids.strip()
                                
                                # Clean strategy_id - remove any leading dashes or other characters
                                # Only keep alphanumeric characters and common ID separators
                                import re
                                strategy_id = re.sub(r'^[^a-zA-Z0-9]*', '', strategy_id)
                                strategy_id = re.sub(r'[^a-zA-Z0-9_\-\.]*$', '', strategy_id)
                                
                                # Validate that this strategy_id exists in our data
                                strategy_ids_in_batch = batch_df[strategy_id_col].astype(str).tolist()
                                if strategy_id not in strategy_ids_in_batch:
                                    continue  # Skip if strategy ID doesn't match our data
                                
                                # Handle multiple capabilities or NONE
                                if capability_ids.upper() == 'NONE':
                                    # Strategy has no required capabilities - skip
                                    continue
                                else:
                                    # Split by comma for multiple capabilities
                                    cap_list = [cap.strip() for cap in capability_ids.split(',')]
                                    
                                    # Get valid capability IDs from our data for validation
                                    valid_cap_ids = capabilities_df[cap_id_col].astype(str).tolist()
                                    
                                    # Create one mapping entry for each capability
                                    for capability_id in cap_list:
                                        if capability_id:  # Ensure not empty
                                            # Clean capability_id - remove any leading/trailing characters
                                            capability_id = re.sub(r'^[^a-zA-Z0-9]*', '', capability_id)
                                            capability_id = re.sub(r'[^a-zA-Z0-9_\-\.]*$', '', capability_id)
                                            
                                            # Validate that this capability_id exists in our data
                                            if capability_id in valid_cap_ids:
                                                mappings.append({
                                                    'Strategic_Initiative_ID': strategy_id,
                                                    'Capability_ID': capability_id
                                                })
                            except ValueError:
                                # Skip malformed lines
                                continue
                    
                    # Update progress
                    progress = batch_end / total_strategies
                    progress_bar.progress(progress)
                
                progress_bar.progress(1.0)
            
            # Create mappings dataframe
            mappings_df = pd.DataFrame(mappings)
            
            if not mappings_df.empty:
                st.session_state['strategy_mappings_df'] = mappings_df
                
                st.markdown("### 📊 Mapping Results")
                st.dataframe(mappings_df)
                
                # Download button
                buffer = BytesIO()
                mappings_df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Mappings as Excel",
                    data=buffer.getvalue(),
                    file_name="strategy_capability_mappings.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("No capability mappings were generated. This could mean all strategies were mapped to 'NONE' or there was an issue with the AI response format.")
