import streamlit as st
import pandas as pd
import json
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs
import concurrent.futures
import threading
import time
# No warnings suppression needed with xlsxwriter engine

def conceptual_data_model_generator_page():
    """Tool for generating conceptual data models."""
    
    # Breadcrumbs
    render_breadcrumbs([
        ("Home", "Home"), 
        ("Data and Information Toolkit", "Data and Information Toolkit"), 
        ("Conceptual Data Model Generator", None)
    ])
    
    st.markdown("## Conceptual Data Model Generator")
    st.markdown("Generate comprehensive conceptual data models for your business domain.")
    
    # Step 1: File Upload and Context
    st.markdown("### Step 1: Upload Company Dossier (Optional)")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload Company Dossier",
        type=['html', 'json'],
        help="Upload an HTML or JSON file containing company information, business processes, or other relevant context"
    )
    
    dossier_content = ""
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/json":
                dossier_content = json.load(uploaded_file)
                dossier_content = json.dumps(dossier_content, indent=2)
                st.success(f"Successfully loaded JSON file: {uploaded_file.name}")
            else:  # HTML file
                dossier_content = uploaded_file.read().decode('utf-8')
                st.success(f"Successfully loaded HTML file: {uploaded_file.name}")
            
            with st.expander("Preview uploaded content"):
                st.text_area("File content:", dossier_content, height=200, disabled=True)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            dossier_content = ""
    
    # Additional context text box
    additional_context = st.text_area(
        "Additional Context",
        placeholder="Add any additional context about the company, industry, or specific requirements...",
        height=150,
        help="Provide any additional context that might help generate more accurate subject areas"
    )
    
    # Step 2: Subject Area Generation
    st.markdown("### Step 2: Generate Data Subject Areas")
    
    if st.button("Generate Subject Areas", type="primary", key="generate_subject_areas"):
        with st.spinner("Generating data subject areas..."):
                # Prepare the comprehensive prompt
                base_prompt = f"""Generate High-Level Data Model Subject Areas

Context

You are an AI system that receives a comprehensive company dossier as input. This dossier may include details about the company's industry (e.g., healthcare, finance, retail, manufacturing, etc.), organisational structure, operations, products or services offered, business processes, technology stack, and customer base.

Objective

From this dossier, infer the core business domains (also known as subject areas or data domains) that are relevant to the organisation. These subject areas represent the high-level categories of information around which the company's data is organised (for example, common domains like Customer, Product/Service, Finance, Human Resources, Operations, etc.).

Instructions
• Identify Key Subject Areas: Determine the primary subject areas that cover the major functional or business domains of the company. Base these on the dossier's information about what the company does, how it is structured, and what it offers.
• Cross-Industry Domains: Include generic business domains applicable to most organisations (such as Customer, Product/Service, Finance, HR, Operations, etc.) as appropriate. Also incorporate any industry-specific domains evident from the dossier (e.g., a healthcare company might have a Patient or Clinical domain, a retail/manufacturing company might have an Inventory/Supply Chain domain, etc.).
• Clear Naming: Use concise, widely understood names for each subject area. For example, use "Product/Service" if the company offers both products and services, or use "Supplier/Vendor" for domains related to third-party providers. Aim for names that would be clear across different industries.
• Description for Each Domain: For every identified subject area, provide a brief description (1 sentence) explaining what that domain covers in the context of the company. Summarise the types of data or business functions included in that domain.
• Structured Output: Present the subject areas in a clear, structured format for easy reading. List each subject area as a separate section with a heading. Begin with the subject area name (e.g., Customer, Finance, Operations, etc.), followed by its description.
• Comprehensive Coverage: Make sure to cover all major domains relevant to the company based on the dossier. Generate exactly 7 subject areas maximum - no more than 7. Avoid introducing domains that aren't supported by the dossier's content – focus on what's relevant to the specific organisation.
• Tone and Clarity: Use clear and professional language in the output. The descriptions should be understandable to both technical and non-technical stakeholders, avoiding overly specialised jargon."""
                
                # Add dossier content if available
                if dossier_content:
                    base_prompt += f"\n\nCompany Dossier Information:\n{dossier_content}"
                
                # Add additional context if provided
                if additional_context:
                    base_prompt += f"\n\nAdditional Context:\n{additional_context}"
                
                try:
                    # Call LangChain model to generate subject areas
                    response = model.invoke([HumanMessage(content=base_prompt)])
                    subject_areas = response.content
                    
                    # Store in session state for iteration
                    st.session_state.subject_areas = subject_areas
                    st.session_state.last_dossier = dossier_content
                    st.session_state.last_context = additional_context
                    
                except Exception as e:
                    st.error(f"Error generating subject areas: {str(e)}")
                    subject_areas = None
    
    # Display generated subject areas
    if 'subject_areas' in st.session_state and st.session_state.subject_areas:
        st.markdown("### Generated Data Subject Areas")
        
        with st.container():
            st.markdown(st.session_state.subject_areas)
        
        # Show iteration info
        if 'last_dossier' in st.session_state or 'last_context' in st.session_state:
            with st.expander("Generation Parameters"):
                if st.session_state.last_dossier:
                    st.write("**Dossier:** File content included")
                if st.session_state.last_context:
                    st.write(f"**Additional Context:** {st.session_state.last_context}")
        
        st.info("💡 **Tip:** You can modify the company dossier or additional context above and regenerate to refine the subject areas.")
        
        # Step 3: Generate Data Elements
        st.markdown("### Step 3: Generate Key Data Elements")
        st.markdown("Generate detailed data entities for each subject area identified above.")
        
        if st.button("Generate Data Elements", type="secondary", key="generate_data_elements"):
            with st.spinner("Generating key data elements for each subject area..."):
                # First, extract subject areas from the generated content
                subject_areas_list = []
                lines = st.session_state.subject_areas.split('\n')
                
                for line in lines:
                    line = line.strip()
                    # Remove formatting and look for subject area headers
                    clean_line = line.replace('*', '').replace('#', '').replace('_', '').strip()
                    
                    # Look for lines that could be subject area names (short, no colons in middle)
                    if (clean_line and 
                        len(clean_line.split()) <= 4 and 
                        not clean_line.startswith('-') and 
                        not clean_line.startswith('•') and
                        len(clean_line) > 3):
                        # Remove trailing colon if present
                        subject_area_name = clean_line.replace(':', '').strip()
                        if subject_area_name and subject_area_name not in subject_areas_list:
                            subject_areas_list.append(subject_area_name)
                
                # If we couldn't extract subject areas, use a fallback approach
                if not subject_areas_list:
                    subject_areas_list = ["Customer", "Product/Service", "Finance", "Operations", "Human Resources"]
                    st.info(f"Using default subject areas. Extracted: {', '.join(subject_areas_list)}")
                else:
                    st.info(f"Processing {len(subject_areas_list)} subject areas: {', '.join(subject_areas_list)}")
                
                all_data_elements = []
                
                # Function to generate data elements for a single subject area
                def generate_subject_area_elements(subject_area, index, dossier_content, additional_context):
                    """Generate data elements for a single subject area."""
                    try:
                        # Prepare specific prompt for this subject area
                        elements_prompt = f"""Generate Key Data Entities for Subject Area: {subject_area}

You are generating data entities for the "{subject_area}" subject area of a business organisation.

Instructions:
• Generate 3-5 key data entities that would be essential for the {subject_area} domain
• For each data entity, provide a brief description (1 sentence) explaining what this entity represents
• Focus on the most important and commonly used entities within {subject_area}
• Use clear, professional naming conventions for entities
• Base the entities on real business needs and the company context provided

Output Format:
Present exactly in this format (no subject area header, just the entities):

- Entity Name: Description of the entity
- Entity Name: Description of the entity
- Entity Name: Description of the entity
- Entity Name: Description of the entity

Example format:
- Customer Profile: Contains comprehensive information about individual customers including contact details, preferences, and account status
- Customer Segment: Defines customer categorisation based on demographics, behaviour, or value metrics
- Customer Communication: Records of all interactions and communications with customers across different channels"""
                        
                        # Add dossier context for each subject area call
                        if dossier_content:
                            elements_prompt += f"\n\nCompany Dossier Context:\n{dossier_content}"
                        
                        if additional_context:
                            elements_prompt += f"\n\nAdditional Context:\n{additional_context}"
                        
                        # Call LangChain model for this specific subject area
                        response = model.invoke([HumanMessage(content=elements_prompt)])
                        subject_area_elements = response.content.strip()
                        
                        # Parse the entities for this subject area
                        entity_lines = subject_area_elements.split('\n')
                        subject_area_id = f"SA{index+1:02d}"
                        subject_area_data = []
                        
                        for line in entity_lines:
                            line = line.strip()
                            # Clean formatting
                            clean_line = line.replace('*', '').replace('#', '').replace('_', '').strip()
                            
                            if (clean_line.startswith('- ') or clean_line.startswith('• ')) and ':' in clean_line:
                                entity_part = clean_line[2:]  # Remove bullet
                                if ':' in entity_part:
                                    parts = entity_part.split(':', 1)
                                    entity_name = parts[0].strip()
                                    entity_desc = parts[1].strip()
                                    
                                    if entity_name and entity_desc:
                                        subject_area_data.append({
                                            'Subject Area ID': subject_area_id,
                                            'Subject Area': subject_area,
                                            'Data Entity': entity_name,
                                            'Description': entity_desc,
                                            'Index': index  # For sorting later
                                        })
                        
                        return subject_area_data
                        
                    except Exception as e:
                        st.error(f"Error generating data elements for {subject_area}: {str(e)}")
                        return []
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Use ThreadPoolExecutor to process subject areas in parallel
                with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(subject_areas_list), 5)) as executor:
                    # Submit all tasks
                    future_to_subject_area = {
                        executor.submit(generate_subject_area_elements, subject_area, i, dossier_content, additional_context): (subject_area, i)
                        for i, subject_area in enumerate(subject_areas_list)
                    }
                    
                    completed_count = 0
                    all_subject_area_data = []
                    
                    # Process completed futures
                    for future in concurrent.futures.as_completed(future_to_subject_area):
                        subject_area, index = future_to_subject_area[future]
                        completed_count += 1
                        
                        try:
                            subject_area_data = future.result()
                            all_subject_area_data.extend(subject_area_data)
                            
                            # Update progress
                            progress = completed_count / len(subject_areas_list)
                            progress_bar.progress(progress)
                            status_text.text(f"Completed {completed_count}/{len(subject_areas_list)} subject areas. Last: {subject_area}")
                            
                        except Exception as e:
                            st.error(f"Error processing {subject_area}: {str(e)}")
                
                # Sort by original index to maintain order and assign entity IDs
                all_subject_area_data.sort(key=lambda x: x['Index'])
                
                # Assign sequential entity IDs
                for i, element in enumerate(all_subject_area_data):
                    element['Data Entity ID'] = f"DE{i+1:03d}"
                    # Remove the temporary index field
                    del element['Index']
                    all_data_elements.append(element)
                
                # Store all collected data elements
                if all_data_elements:
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Create DataFrame directly from parallel processing results
                    df = pd.DataFrame(all_data_elements)
                    
                    # Store data elements dataframe for Excel export
                    st.session_state.data_elements_df = df
                    
                    # Create entity mapping for relationships
                    entity_mapping = {}
                    for _, row in df.iterrows():
                        entity_mapping[row['Data Entity']] = row['Data Entity ID']
                    st.session_state.entity_mapping = entity_mapping
                    
                    # Create combined response for session state (for backwards compatibility)
                    combined_response = ""
                    current_subject = ""
                    for element in all_data_elements:
                        if element['Subject Area'] != current_subject:
                            combined_response += f"\n{element['Subject Area']}:\n"
                            current_subject = element['Subject Area']
                        combined_response += f"- {element['Data Entity']}: {element['Description']}\n"
                    
                    st.session_state.data_elements = combined_response.strip()
                    st.success(f"✅ Generated {len(all_data_elements)} data entities across {len(subject_areas_list)} subject areas in parallel!")
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error("No data elements were generated. Please try again.")
        
        # Display generated data elements
        if 'data_elements' in st.session_state and st.session_state.data_elements:
            # Check if we have the DataFrame from parallel processing
            if 'data_elements_df' in st.session_state:
                # Use the DataFrame directly from parallel processing
                df = st.session_state.data_elements_df
                
                st.markdown("#### Data Elements")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name="data_elements.csv",
                    mime="text/csv"
                )
            else:
                # Fallback parsing for backwards compatibility
                try:
                    # Parse the generated content to create a table
                    lines = st.session_state.data_elements.split('\n')
                    table_data = []
                    current_subject_area = ""
                    subject_area_counter = 1
                    entity_counter = 1
                    subject_area_id = ""
                    
                    for line in lines:
                        line = line.strip()
                        
                        # Skip empty lines
                        if not line:
                            continue
                        
                        # Remove any special formatting
                        clean_line = line.replace('*', '').replace('#', '').replace('_', '').strip()
                        
                        # Check for subject area headers
                        if (clean_line.endswith(':') and not clean_line.startswith('-') and len(clean_line) > 1) or \
                           (clean_line and not clean_line.startswith('-') and not ':' in clean_line and len(clean_line.split()) <= 4):
                            # This is likely a subject area header
                            current_subject_area = clean_line.replace(':', '').strip()
                            subject_area_id = f"SA{subject_area_counter:02d}"
                            subject_area_counter += 1
                        
                        # Check for entity lines
                        elif (clean_line.startswith('- ') and ':' in clean_line) or \
                             (clean_line.startswith('• ') and ':' in clean_line) or \
                             (clean_line.startswith('* ') and ':' in clean_line):
                            # This is an entity line
                            entity_part = clean_line[2:]  # Remove bullet
                            if ':' in entity_part:
                                parts = entity_part.split(':', 1)
                                entity_name = parts[0].strip()
                                entity_desc = parts[1].strip()
                                
                                if current_subject_area and entity_name:
                                    entity_id = f"DE{entity_counter:03d}"
                                    table_data.append({
                                        'Subject Area ID': subject_area_id,
                                        'Subject Area': current_subject_area,
                                        'Data Entity ID': entity_id,
                                        'Data Entity': entity_name,
                                        'Description': entity_desc
                                    })
                                    entity_counter += 1
                    
                    if table_data:
                        st.markdown("#### Data Elements")
                        df = pd.DataFrame(table_data)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Store data elements dataframe for Excel export
                        st.session_state.data_elements_df = df
                        
                        # Create entity mapping for relationships
                        entity_mapping = {}
                        for _, row in df.iterrows():
                            entity_mapping[row['Data Entity']] = row['Data Entity ID']
                        st.session_state.entity_mapping = entity_mapping
                        
                        # Download option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name="data_elements.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("Could not parse data elements. The response may be in an unexpected format.")
                        st.info("💡 Try regenerating the data elements or check that subject areas were generated correctly first.")
                    
                except Exception as e:
                    st.error(f"Error parsing data elements: {str(e)}")
        
        # Step 4: Generate Entity Relationships
        if 'data_elements' in st.session_state and st.session_state.data_elements:
            st.markdown("### Step 4: Generate Entity Relationships")
            st.markdown("Generate source-to-target mappings showing relationships between data entities.")
            
            if st.button("Generate Entity Relationships", type="secondary", key="generate_relationships"):
                with st.spinner("Generating entity relationships and mappings..."):
                    # Get unique subject areas from the data elements dataframe
                    if 'data_elements_df' not in st.session_state:
                        st.error("Data elements not found! Please generate data elements first.")
                        st.stop()
                    
                    # Check entity mapping exists
                    if 'entity_mapping' not in st.session_state:
                        st.error("Entity mapping not found! Please regenerate data elements first.")
                        st.stop()
                    
                    df = st.session_state.data_elements_df
                    subject_areas = df['Subject Area'].unique().tolist()
                    
                    all_relationships = []
                    
                    # Generate relationships for each subject area individually
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, subject_area in enumerate(subject_areas):
                        status_text.text(f"Generating relationships for {subject_area}... ({i+1}/{len(subject_areas)})")
                        
                        # Get entities for this subject area
                        subject_entities = df[df['Subject Area'] == subject_area]
                        entities_text = ""
                        for _, row in subject_entities.iterrows():
                            entities_text += f"- {row['Data Entity']}: {row['Description']}\n"
                        
                        # Also include some entities from other subject areas for cross-domain relationships
                        other_entities = df[df['Subject Area'] != subject_area].sample(min(10, len(df[df['Subject Area'] != subject_area])))
                        if not other_entities.empty:
                            entities_text += f"\nOther Available Entities (for cross-domain relationships):\n"
                            for _, row in other_entities.iterrows():
                                entities_text += f"- {row['Data Entity']} (from {row['Subject Area']}): {row['Description']}\n"
                        
                        # Prepare focused prompt for this subject area
                        relationships_prompt = f"""Generate Entity Relationship Mappings for {subject_area} Subject Area

Focus on the "{subject_area}" subject area and generate logical relationships between entities.

Primary Entities in {subject_area}:
{entities_text}

Instructions:
• Generate 3-5 key relationships involving entities from the {subject_area} subject area
• Include both intra-domain relationships (within {subject_area}) and cross-domain relationships (with other subject areas)
• Create source-to-target mappings showing how entities relate to each other
• Include cardinality for each relationship (One-to-One, One-to-Many, Many-to-One, Many-to-Many)
• Focus on the most important and commonly used relationships
• Use clear, professional naming conventions
• Ensure relationships are business-logical and realistic
• Use ONLY the exact entity names as they appear in the entities list above

Output Format:
Present the results as a structured list of mappings. Use this exact format:

Source Entity - Target Entity - Cardinality - Relationship Description
Source Entity - Target Entity - Cardinality - Relationship Description
Source Entity - Target Entity - Cardinality - Relationship Description

Examples:
Customer Profile - Customer Segment - Many-to-One - Each customer profile is categorised into one segment
Customer Communication - Customer Profile - Many-to-One - Multiple communications are linked to one customer profile

IMPORTANT: Use only the exact entity names from the entities list provided above."""
                        
                        # Add context if available
                        if dossier_content:
                            relationships_prompt += f"\n\nCompany Dossier Information:\n{dossier_content}"
                        
                        if additional_context:
                            relationships_prompt += f"\n\nAdditional Context:\n{additional_context}"
                        
                        try:
                            # Call LangChain model for this specific subject area
                            response = model.invoke([HumanMessage(content=relationships_prompt)])
                            subject_area_relationships = response.content.strip()
                            all_relationships.append(subject_area_relationships)
                            
                            # Update progress
                            progress = (i + 1) / len(subject_areas)
                            progress_bar.progress(progress)
                            
                        except Exception as e:
                            st.error(f"Error generating relationships for {subject_area}: {str(e)}")
                            continue
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Combine all relationships
                    combined_relationships = "\n\n".join(all_relationships)
                    
                    # Store in session state
                    st.session_state.entity_relationships = combined_relationships
                    st.success(f"✅ Generated relationships across {len(subject_areas)} subject areas!")
            
            # Display generated entity relationships
            if 'entity_relationships' in st.session_state and st.session_state.entity_relationships:
                # Parse and create table view for relationships
                try:
                    # Parse the generated content to create a relationships table
                    lines = st.session_state.entity_relationships.split('\n')
                    relationships_data = []
                    relationship_counter = 1
                    
                    for line in lines:
                        line = line.strip()
                        # Remove any special formatting
                        line = line.replace('*', '').replace('#', '').replace('_', '')
                        
                        if ' - ' in line and line.count(' - ') >= 3:
                            # This should be a relationship mapping line
                            parts = line.split(' - ')
                            if len(parts) >= 4:
                                source_entity = parts[0].strip()
                                target_entity = parts[1].strip()
                                cardinality = parts[2].strip()
                                description = ' - '.join(parts[3:]).strip()
                                
                                # Clean entity names - remove numbered prefixes like "1. " or "2) "
                                import re
                                source_entity = re.sub(r'^\d+[\.\)]\s*', '', source_entity)
                                target_entity = re.sub(r'^\d+[\.\)]\s*', '', target_entity)
                                
                                # Map entity names to IDs if available
                                source_entity_id = ""
                                target_entity_id = ""
                                if 'entity_mapping' in st.session_state:
                                    # Try exact match first
                                    source_entity_id = st.session_state.entity_mapping.get(source_entity, "")
                                    target_entity_id = st.session_state.entity_mapping.get(target_entity, "")
                                    
                                    # If exact match fails, try case-insensitive match
                                    if not source_entity_id:
                                        for entity_name, entity_id in st.session_state.entity_mapping.items():
                                            if entity_name.lower() == source_entity.lower():
                                                source_entity_id = entity_id
                                                break
                                    
                                    if not target_entity_id:
                                        for entity_name, entity_id in st.session_state.entity_mapping.items():
                                            if entity_name.lower() == target_entity.lower():
                                                target_entity_id = entity_id
                                                break
                                
                                # Generate relationship ID
                                relationship_id = f"REL{relationship_counter:03d}"
                                
                                relationships_data.append({
                                    'Relationship ID': relationship_id,
                                    'Source Entity ID': source_entity_id,
                                    'Source Entity': source_entity,
                                    'Target Entity ID': target_entity_id,
                                    'Target Entity': target_entity,
                                    'Cardinality': cardinality,
                                    'Relationship Description': description
                                })
                                
                                relationship_counter += 1
                    
                    if relationships_data:
                        st.markdown("#### Entity Relationships")
                        relationships_df = pd.DataFrame(relationships_data)
                        st.dataframe(relationships_df, use_container_width=True, hide_index=True)
                        
                        # Store relationships dataframe for Excel export
                        st.session_state.relationships_df = relationships_df
                        
                        # Download option for relationships
                        csv = relationships_df.to_csv(index=False)
                        st.download_button(
                            label="Download Relationships as CSV",
                            data=csv,
                            file_name="entity_relationships.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("Could not parse entity relationships. Please try regenerating.")
                        # Show raw content for debugging
                        with st.expander("Debug: Raw relationships content"):
                            st.text(st.session_state.entity_relationships)
                    
                except Exception as e:
                    st.error("Could not parse entity relationships into table format.")
            
            # Excel download with both sheets
            if ('data_elements_df' in st.session_state and 
                'relationships_df' in st.session_state):
                
                st.markdown("#### Combined Excel Export")
                
                # Create Excel file with multiple sheets
                def create_excel_file():
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        # Add all available data to Excel with descriptive sheet names
                        if 'subject_areas_df' in st.session_state:
                            st.session_state.subject_areas_df.to_excel(writer, sheet_name='Subject Areas', index=False)
                        if 'data_elements_df' in st.session_state:
                            st.session_state.data_elements_df.to_excel(writer, sheet_name='Data Elements', index=False)
                        if 'relationships_df' in st.session_state:
                            st.session_state.relationships_df.to_excel(writer, sheet_name='Entity Relationships', index=False)
                    return output.getvalue()
                
                excel_data = create_excel_file()
                
                st.download_button(
                    label="📊 Download Complete Data Model (Excel)",
                    data=excel_data,
                    file_name="conceptual_data_model.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Data Toolkit", key="back_to_data_toolkit"):
            st.session_state.page = "Data and Information Toolkit"
            st.rerun()
    
    with col2:
        if st.button("← Back to Home", key="back_to_home_from_tool"):
            st.session_state.page = "Home"
            st.rerun()
