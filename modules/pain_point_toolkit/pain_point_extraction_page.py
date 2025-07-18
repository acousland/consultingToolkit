import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import pain_point_extraction_prompt, model
from navigation import render_breadcrumbs

def pain_point_extraction_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🔍 Pain Point Toolkit", "Pain Point Toolkit"), ("🔍 Pain Point Extraction", None)])
    
    st.markdown("## Pain Point extraction")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        if uploaded_file.name.endswith('.csv'):
            dataframe = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx', '.xlsm')):
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Select sheet to load", xls.sheet_names)
            dataframe = pd.read_excel(xls, sheet_name=sheet_name)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            st.stop()

        st.write(dataframe)

        selected_columns = st.multiselect(
            "Select one or more columns to concatenate for analysis",
            list(dataframe.columns)
        )
        if selected_columns:
            st.write('You selected:', selected_columns)
            concatenated_data = dataframe[selected_columns].astype(str).agg(' '.join, axis=1)
        else:
            st.write('No columns selected.')
            concatenated_data = pd.Series(dtype=str)

        prompts = st.text_input('Any additional context for the AI to consider', '')
        
        # Add chunk size control
        chunk_size = st.number_input('Number of rows to process per chunk (to manage context window)', 
                                   min_value=1, max_value=100, value=20, 
                                   help="Smaller chunks prevent context window overflow but require more API calls")

        if st.button("Generate pain points", type="secondary"):
            if concatenated_data.empty:
                st.error("Please select columns to analyse.")
                st.stop()
            
            all_pain_points = []
            total_rows = len(concatenated_data)
            
            # Process in chunks to avoid context window issues
            with st.spinner(f"Processing {total_rows} rows in chunks of {chunk_size}..."):
                progress_bar = st.progress(0)
                
                for i in range(0, total_rows, chunk_size):
                    chunk_end = min(i + chunk_size, total_rows)
                    chunk_data = concatenated_data.iloc[i:chunk_end]
                    
                    # Convert chunk to string for processing
                    chunk_text = '\n'.join(chunk_data.astype(str))
                    
                    # Update progress
                    progress = (chunk_end) / total_rows
                    progress_bar.progress(progress)
                    
                    st.write(f"Processing rows {i+1} to {chunk_end} of {total_rows}")
                    
                    # Process this chunk
                    _input = pain_point_extraction_prompt.format(
                        additional_prompts=prompts,
                        data=chunk_text
                    )
                    output = model.invoke([HumanMessage(content=_input)])
                    
                    # Parse the output as simple text lines instead of comma-separated
                    raw_content = output.content.strip()
                    
                    # Clean up any markdown formatting or JSON artifacts
                    if "```" in raw_content:
                        # Remove code blocks
                        lines = raw_content.split('\n')
                        cleaned_lines = []
                        in_code_block = False
                        for line in lines:
                            if line.strip().startswith('```'):
                                in_code_block = not in_code_block
                                continue
                            if not in_code_block and line.strip():
                                cleaned_lines.append(line.strip())
                        raw_content = '\n'.join(cleaned_lines)
                    
                    # Remove any JSON artifacts like brackets and quotes
                    raw_content = raw_content.replace('["', '').replace('"]', '').replace('",', '\n').replace('"', '')
                    
                    # Split into lines and clean up
                    chunk_pain_points = []
                    for line in raw_content.split('\n'):
                        line = line.strip()
                        # Remove bullet points and numbering
                        if line.startswith('•'):
                            line = line[1:].strip()
                        elif line.startswith('-'):
                            line = line[1:].strip()
                        elif line.split('.')[0].isdigit():
                            line = '.'.join(line.split('.')[1:]).strip()
                        
                        # Only include non-empty lines that look like sentences
                        if line and len(line) > 10:
                            chunk_pain_points.append(line)
                    
                    all_pain_points.extend(chunk_pain_points)
                
                progress_bar.progress(1.0)
            
            # Remove duplicates while preserving order
            unique_pain_points = []
            seen = set()
            for point in all_pain_points:
                point_lower = point.lower().strip()
                if point_lower not in seen:
                    seen.add(point_lower)
                    unique_pain_points.append(point)
            
            st.session_state['pain_points'] = unique_pain_points
            st.write(f"**Extracted {len(unique_pain_points)} Unique Pain Points:**")
            for i, point in enumerate(unique_pain_points, 1):
                st.write(f"{i}. {point}")

        # Show download button if pain_points exist
        if 'pain_points' in st.session_state and st.session_state['pain_points']:
            df_pain_points = pd.DataFrame({'Pain Points': st.session_state['pain_points']})
            buffer = BytesIO()
            df_pain_points.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="Download pain points as Excel",
                data=buffer.getvalue(),
                file_name="pain_points.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
