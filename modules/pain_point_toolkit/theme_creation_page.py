import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from prompts import THEME_PERSPECTIVE_MAPPING_PROMPT
from navigation import render_breadcrumbs

def theme_creation_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🔍 Pain Point Toolkit", "Pain Point Toolkit"), ("🗂️ Theme & Perspective Mapping", None)])
    
    st.markdown("## Pain Point Theme & Perspective Mapping")
    st.markdown("Upload a pain points spreadsheet to map each pain point to themes and perspectives.")
    
    # Predefined themes and perspectives
    predefined_themes = [
        "Manual Processes", "No Single Source of Truth", "Skills & Capacity", 
        "Technology Limitations", "Vendor Dependency", "Risk & Compliance",
        "Market Pressures", "Capacity Constraints", "Project Mobilisation",
        "Governance & Decision-Making", "Integration / Data Silos", "Process Improvement",
        "Technology Opportunity", "Cross-Service Alignment", "Budget & Investment",
        "Culture & Change", "Capacity Planning", "Inefficient Governance",
        "Process Timing", "Process Inconsistencies"
    ]
    
    predefined_perspectives = [
        "Process", "Data / Information", "People", "Technology", 
        "Risk", "Market", "Governance"
    ]
    
    # Initialise session state
    if 'pain_points_df' not in st.session_state:
        st.session_state['pain_points_df'] = None
    if 'pain_columns' not in st.session_state:
        st.session_state['pain_columns'] = {'id': None, 'text': None}
    
    # File upload section
    st.markdown("### 📋 Upload Pain Points Spreadsheet")
    pain_points_file = st.file_uploader(
        "Upload Pain Points Excel file", 
        type=['xlsx', 'xls', 'xlsm'],
        key="pain_points_upload_theme"
    )
    
    if pain_points_file is not None:
        # Load pain points file
        xls = pd.ExcelFile(pain_points_file)
        pain_sheet = st.selectbox("Select sheet for pain points", xls.sheet_names, key="pain_sheet_theme")
        pain_points_df = pd.read_excel(xls, sheet_name=pain_sheet)
        st.session_state['pain_points_df'] = pain_points_df
        
        st.write("**Preview:**")
        st.dataframe(pain_points_df.head())
        
        # Column selection
        pain_id_col = st.selectbox(
            "Select Pain Point ID column", 
            pain_points_df.columns,
            key="pain_id_col_theme"
        )
        pain_text_cols = st.multiselect(
            "Select Pain Point text columns (will be concatenated)", 
            pain_points_df.columns,
            key="pain_text_cols_theme",
            help="Select one or more columns that describe the pain point"
        )
        
        # Store column selections
        st.session_state['pain_columns']['id'] = pain_id_col
        st.session_state['pain_columns']['text'] = pain_text_cols
        
        # Show available themes and perspectives
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🏷️ Available Themes")
            st.write(", ".join(predefined_themes))
        
        with col2:
            st.markdown("### 👀 Available Perspectives") 
            st.write(", ".join(predefined_perspectives))
        
        # Additional context input
        additional_context = st.text_area(
            "Additional context for theme/perspective mapping (optional):",
            placeholder="e.g., Focus on operational themes, prioritize technology perspective..."
        )
        
        # Batch size control
        batch_size = st.number_input(
            'Batch size (number of pain points to process together)', 
            min_value=1, max_value=50, value=10,
            help="Larger batches are faster but may be less accurate. Smaller batches are more precise but slower."
        )
        
        # Generate mappings button
        if (st.session_state['pain_columns']['text'] and 
            st.button("Generate Theme & Perspective Mappings", type="primary")):
            
            pain_id_col = st.session_state['pain_columns']['id']
            pain_text_cols = st.session_state['pain_columns']['text']
            
            mappings = []
            
            with st.spinner("Mapping pain points to themes and perspectives..."):
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

                    themes_text = ", ".join(predefined_themes)
                    perspectives_text = ", ".join(predefined_perspectives)

                    batch_mapping_prompt = THEME_PERSPECTIVE_MAPPING_PROMPT.format(
                        pain_points=pain_points_text,
                        themes=themes_text,
                        perspectives=perspectives_text,
                        additional_context=additional_context,
                    )
                    
                    # Get AI response for the batch
                    output = model.invoke([HumanMessage(content=batch_mapping_prompt)])
                    batch_results = output.content.strip()
                    
                    # Debug: Show AI response for first batch
                    if batch_start == 0:
                        st.write("**Sample AI Response:**")
                        st.text(batch_results[:300] + "..." if len(batch_results) > 300 else batch_results)
                    
                    # Parse the batch results
                    parsed_count = 0
                    for line in batch_results.split('\n'):
                        line = line.strip()
                        
                        # More flexible parsing - look for -> anywhere in the line
                        if '->' in line:
                            try:
                                # Split on '->' to get pain point ID and mapping
                                pain_point_part, mapping_part = line.split('->', 1)
                                pain_point_id = pain_point_part.strip()
                                
                                # Clean up pain point ID - remove markdown formatting and extra characters
                                pain_point_id = pain_point_id.replace('**', '').replace('*', '').replace('`', '')
                                pain_point_id = pain_point_id.replace('"', '').replace("'", '').strip()
                                
                                # Parse theme and perspective with more flexible approach
                                theme = "Unknown"
                                perspective = "Unknown"
                                
                                # Look for THEME: and PERSPECTIVE: patterns
                                theme_match = None
                                perspective_match = None
                                
                                # Try to find theme
                                if 'THEME:' in mapping_part.upper():
                                    # Find THEME: and extract until | or end
                                    theme_start = mapping_part.upper().find('THEME:') + 6
                                    theme_part = mapping_part[theme_start:]
                                    if '|' in theme_part:
                                        theme = theme_part.split('|')[0].strip()
                                    elif 'PERSPECTIVE:' in theme_part.upper():
                                        theme = theme_part.split('PERSPECTIVE:')[0].strip()
                                    else:
                                        theme = theme_part.strip()
                                    
                                    # Clean up theme
                                    theme = theme.replace('**', '').replace('*', '').replace('`', '')
                                    theme = theme.replace('"', '').replace("'", '').strip()
                                
                                # Try to find perspective
                                if 'PERSPECTIVE:' in mapping_part.upper():
                                    perspective_start = mapping_part.upper().find('PERSPECTIVE:') + 12
                                    perspective = mapping_part[perspective_start:].strip()
                                    
                                    # Clean up perspective
                                    perspective = perspective.replace('**', '').replace('*', '').replace('`', '')
                                    perspective = perspective.replace('"', '').replace("'", '').strip()
                                
                                # Only add if we found both theme and perspective
                                if theme != "Unknown" and perspective != "Unknown":
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
                                        'Theme': theme,
                                        'Perspective': perspective,
                                        'Pain_Point_Text': pain_text
                                    })
                                    parsed_count += 1
                                
                            except Exception as e:
                                # Skip malformed lines but log the issue
                                continue
                    
                    st.write(f"Successfully parsed {parsed_count} mappings from this batch")
                    
                    # Update progress
                    progress = batch_end / total_pain_points
                    progress_bar.progress(progress)
                
                progress_bar.progress(1.0)
            
            # Create mappings dataframe
            mappings_df = pd.DataFrame(mappings)
            
            # Check if we have any successful mappings
            if mappings_df.empty:
                st.error("❌ No valid mappings were generated. Please check your data and try again.")
                st.write("**Debug Info:**")
                st.write(f"Total batches processed: {len(range(0, total_pain_points, batch_size))}")
                st.write(f"Last AI response sample: {batch_results[:500]}...")
                return
            
            st.session_state['theme_mappings_df'] = mappings_df
            
            st.markdown("### 📊 Theme & Perspective Mapping Results")
            st.dataframe(mappings_df)
            
            # Summary statistics - only if we have the columns
            if 'Theme' in mappings_df.columns and 'Perspective' in mappings_df.columns:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Themes Distribution:**")
                    theme_counts = mappings_df['Theme'].value_counts()
                    st.dataframe(theme_counts)
                
                with col2:
                    st.markdown("**Perspectives Distribution:**")
                    perspective_counts = mappings_df['Perspective'].value_counts()
                    st.dataframe(perspective_counts)
            else:
                st.warning("⚠️ Some columns are missing from the results. Please check the mapping output.")
            
            # Download button
            buffer = BytesIO()
            mappings_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Theme & Perspective Mappings as Excel",
                data=buffer.getvalue(),
                file_name="pain_point_theme_perspective_mappings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    else:
        st.info("📤 Please upload a pain points Excel file to begin theme and perspective mapping.")
