import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import capability_description_prompt, model
from navigation import render_breadcrumbs

def capability_description_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("📝 Capability Toolkit", "Capability Toolkit"), ("📝 Capability Description Generation", None)])
    
    
    st.markdown("## Capability Description Generation")
    
    # Option 1: Upload Excel file with capabilities
    st.markdown("### Upload Capabilities from Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file containing capabilities", type=['xlsx', 'xls', 'xlsm'])
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Select sheet to load", xls.sheet_names)
            dataframe = pd.read_excel(xls, sheet_name=sheet_name)
            
            st.markdown("#### Data Preview")
            st.dataframe(dataframe.head())
            
            # ID Column selection
            id_column = st.selectbox(
                "Select the column containing capability IDs:",
                ["None"] + dataframe.columns.tolist(),
                help="Choose the column that contains unique identifiers for each capability (optional but recommended)"
            )
            
            # Column selection
            selected_columns = st.multiselect(
                "Select columns containing capabilities to describe:",
                dataframe.columns.tolist(),
                help="Choose one or more columns that contain capability names or descriptions"
            )
            
            if selected_columns:
                # Preview selected data
                preview_data = dataframe[selected_columns]
                st.markdown("#### Selected Data Preview")
                st.dataframe(preview_data.head())
                
                # Concatenate selected columns and store IDs
                concatenated_data = ""
                capability_ids = []
                original_capabilities = []
                
                for index, row in dataframe.iterrows():
                    row_data = []
                    for col in selected_columns:
                        if pd.notna(row[col]) and str(row[col]).strip():
                            row_data.append(str(row[col]).strip())
                    
                    if row_data:
                        capability_text = " | ".join(row_data)
                        concatenated_data += capability_text + "\n"
                        original_capabilities.append(capability_text)
                        
                        # Store ID if ID column is selected
                        if id_column != "None" and id_column in dataframe.columns:
                            capability_id = str(row[id_column]) if pd.notna(row[id_column]) else f"ID_{index}"
                            capability_ids.append(capability_id)
                        else:
                            capability_ids.append(f"CAP_{index + 1}")  # Generate sequential ID
                
                st.markdown("#### Concatenated Capabilities")
                st.text_area("Capabilities extracted from file:", value=concatenated_data, height=150, disabled=True)
                
                # Additional prompts for file-based generation
                file_additional_prompts = st.text_area(
                    "Additional context for capability descriptions:", 
                    placeholder="e.g., Focus on digital transformation, include implementation timelines, consider industry-specific requirements...",
                    key="file_additional_prompts"
                )
                
                if st.button("Generate Descriptions from File", type="primary"):
                    if concatenated_data.strip():
                        with st.spinner("Generating capability descriptions from uploaded file..."):
                            # Generate prompt
                            _input = capability_description_prompt.format(
                                additional_prompts=file_additional_prompts,
                                capabilities=concatenated_data
                            )
                            
                            # Get AI response
                            output = model.invoke([HumanMessage(content=_input)])
                            descriptions = output.content
                            
                            # Store descriptions in session state
                            st.session_state['capability_descriptions'] = descriptions
                            
                            # Parse the AI response and create DataFrame
                            capability_id_list = []
                            capability_list = []
                            description_list = []
                            
                            # Parse AI response for descriptions
                            description_lines = [line.strip() for line in descriptions.split('\n') if line.strip()]
                            
                            for i, cap in enumerate(original_capabilities):
                                capability_id_list.append(capability_ids[i])
                                capability_list.append(cap)
                                
                                # Try to find matching description
                                matching_desc = "Description not found"
                                for desc_line in description_lines:
                                    if ':' in desc_line:
                                        desc_capability = desc_line.split(':')[0].strip()
                                        desc_text = desc_line.split(':', 1)[1].strip()
                                        # Check if this description matches our capability
                                        if desc_capability.lower() in cap.lower() or cap.lower() in desc_capability.lower():
                                            matching_desc = desc_text
                                            break
                                
                                # If no match found, use the corresponding line if available
                                if matching_desc == "Description not found" and i < len(description_lines):
                                    desc_line = description_lines[i]
                                    if ':' in desc_line:
                                        matching_desc = desc_line.split(':', 1)[1].strip()
                                    else:
                                        matching_desc = desc_line
                                
                                description_list.append(matching_desc)
                            
                            # Create DataFrame with ID column
                            if id_column != "None":
                                results_df = pd.DataFrame({
                                    'Capability_ID': capability_id_list,
                                    'Capability': capability_list,
                                    'Description': description_list
                                })
                            else:
                                results_df = pd.DataFrame({
                                    'Capability_ID': capability_id_list,
                                    'Capability': capability_list,
                                    'Description': description_list
                                })
                            
                            # Display results
                            st.markdown("### Generated Capability Descriptions")
                            st.dataframe(results_df)
                            
                            # Create Excel file for download
                            output_buffer = BytesIO()
                            with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
                                results_df.to_excel(writer, sheet_name='Capability Descriptions', index=False)
                            
                            output_buffer.seek(0)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Results as Excel",
                                data=output_buffer.getvalue(),
                                file_name="capability_descriptions.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            # Store results in session state
                            st.session_state['capability_results_df'] = results_df
                    else:
                        st.error("No capability data found in selected columns.")
            else:
                st.info("Please select at least one column containing capabilities.")
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    st.markdown("---")
    