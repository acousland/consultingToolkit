import streamlit as st
import pandas as pd
import json
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs

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

You are an AI system that receives a comprehensive company dossier as input. This dossier may include details about the company's industry (e.g., healthcare, finance, retail, manufacturing, etc.), organizational structure, operations, products or services offered, business processes, technology stack, and customer base.

Objective

From this dossier, infer the core business domains (also known as subject areas or data domains) that are relevant to the organization. These subject areas represent the high-level categories of information around which the company's data is organized (for example, common domains like Customer, Product/Service, Finance, Human Resources, Operations, etc.).

Instructions
• Identify Key Subject Areas: Determine the primary subject areas that cover the major functional or business domains of the company. Base these on the dossier's information about what the company does, how it is structured, and what it offers.
• Cross-Industry Domains: Include generic business domains applicable to most organizations (such as Customer, Product/Service, Finance, HR, Operations, etc.) as appropriate. Also incorporate any industry-specific domains evident from the dossier (e.g., a healthcare company might have a Patient or Clinical domain, a retail/manufacturing company might have an Inventory/Supply Chain domain, etc.).
• Clear Naming: Use concise, widely understood names for each subject area. For example, use "Product/Service" if the company offers both products and services, or use "Supplier/Vendor" for domains related to third-party providers. Aim for names that would be clear across different industries.
• Description for Each Domain: For every identified subject area, provide a brief description (1 sentence) explaining what that domain covers in the context of the company. Summarize the types of data or business functions included in that domain.
• Structured Output: Present the subject areas in a clear, structured format for easy reading. List each subject area as a separate section with a heading. Begin with the subject area name (e.g., Customer, Finance, Operations, etc.), followed by its description.
• Comprehensive Coverage: Make sure to cover all major domains relevant to the company based on the dossier. Generate exactly 7 subject areas maximum - no more than 7. Avoid introducing domains that aren't supported by the dossier's content – focus on what's relevant to the specific organization.
• Tone and Clarity: Use clear and professional language in the output. The descriptions should be understandable to both technical and non-technical stakeholders, avoiding overly specialized jargon."""
                
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
                # Prepare the prompt for data elements generation
                elements_prompt = f"""Generate Key Data Elements for Subject Areas

Based on the following subject areas that were previously identified, generate key data entities for each subject area.

Subject Areas:
{st.session_state.subject_areas}

Instructions:
• For each subject area listed above, identify 3-5 key data entities that would be essential for that domain
• For each data entity, provide a brief description (1 sentence) explaining what this entity represents and what key information it would contain
• Focus on the most important and commonly used entities within each subject area
• Use clear, professional naming conventions for entities
• Ensure entities are specific enough to be useful but general enough to apply across similar organizations

Output Format:
Present the results as a structured list where each subject area is followed by its data entities and descriptions. Use this exact format:

Subject Area Name:
- Entity Name: Description of the entity
- Entity Name: Description of the entity
- Entity Name: Description of the entity

(Repeat for each subject area)"""
                
                # Add context if available
                if dossier_content:
                    elements_prompt += f"\n\nCompany Dossier Information:\n{dossier_content}"
                
                if additional_context:
                    elements_prompt += f"\n\nAdditional Context:\n{additional_context}"
                
                try:
                    # Call LangChain model to generate data elements
                    response = model.invoke([HumanMessage(content=elements_prompt)])
                    data_elements = response.content
                    
                    # Store in session state
                    st.session_state.data_elements = data_elements
                    
                except Exception as e:
                    st.error(f"Error generating data elements: {str(e)}")
                    data_elements = None
        
        # Display generated data elements
        if 'data_elements' in st.session_state and st.session_state.data_elements:
            # Parse and create table view
            try:
                # Parse the generated content to create a table
                lines = st.session_state.data_elements.split('\n')
                table_data = []
                current_subject_area = ""
                
                for line in lines:
                    line = line.strip()
                    # Remove any asterisk formatting
                    line = line.replace('*', '')
                    
                    if line.endswith(':') and not line.startswith('-') and len(line) > 1:
                        # This is a subject area header
                        current_subject_area = line.replace(':', '').strip()
                    elif line.startswith('- ') and ':' in line:
                        # This is an entity line
                        entity_part = line[2:]  # Remove '- '
                        if ':' in entity_part:
                            entity_name, entity_desc = entity_part.split(':', 1)
                            if current_subject_area:  # Only add if we have a subject area
                                table_data.append({
                                    'Subject Area': current_subject_area,
                                    'Data Entity': entity_name.strip(),
                                    'Description': entity_desc.strip()
                                })
                
                if table_data:
                    st.markdown("#### Data Elements")
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Store data elements dataframe for Excel export
                    st.session_state.data_elements_df = df
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="data_elements.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("Could not parse data elements. Please try regenerating.")
                    # Show raw content for debugging
                    with st.expander("Debug: Raw content"):
                        st.text(st.session_state.data_elements)
                
            except Exception as e:
                st.error("Could not parse data elements into table format.")
        
        # Step 4: Generate Entity Relationships
        if 'data_elements' in st.session_state and st.session_state.data_elements:
            st.markdown("### Step 4: Generate Entity Relationships")
            st.markdown("Generate source-to-target mappings showing relationships between data entities.")
            
            if st.button("Generate Entity Relationships", type="secondary", key="generate_relationships"):
                with st.spinner("Generating entity relationships and mappings..."):
                    # Prepare the prompt for relationship generation
                    relationships_prompt = f"""Generate Entity Relationship Mappings

Based on the following data elements that were previously identified, generate source-to-target mappings showing relationships between data entities.

Data Elements:
{st.session_state.data_elements}

Instructions:
• Identify logical relationships between data entities across different subject areas
• Create source-to-target mappings showing how entities relate to each other
• Include cardinality for each relationship (One-to-One, One-to-Many, Many-to-One, Many-to-Many)
• Focus on the most important and commonly used relationships
• Use clear, professional naming conventions
• Ensure relationships are business-logical and realistic

Output Format:
Present the results as a structured list of mappings. Use this exact format:

Source Entity - Target Entity - Cardinality - Relationship Description
Source Entity - Target Entity - Cardinality - Relationship Description
Source Entity - Target Entity - Cardinality - Relationship Description

Examples:
Customer - Order - One-to-Many - A customer can place multiple orders
Order - Product - Many-to-Many - An order can contain multiple products and a product can be in multiple orders
Employee - Department - Many-to-One - Multiple employees belong to one department

Generate 10-15 key relationships that would be essential for this business domain."""
                    
                    # Add context if available
                    if dossier_content:
                        relationships_prompt += f"\n\nCompany Dossier Information:\n{dossier_content}"
                    
                    if additional_context:
                        relationships_prompt += f"\n\nAdditional Context:\n{additional_context}"
                    
                    try:
                        # Call LangChain model to generate relationships
                        response = model.invoke([HumanMessage(content=relationships_prompt)])
                        entity_relationships = response.content
                        
                        # Store in session state
                        st.session_state.entity_relationships = entity_relationships
                        
                    except Exception as e:
                        st.error(f"Error generating entity relationships: {str(e)}")
                        entity_relationships = None
            
            # Display generated entity relationships
            if 'entity_relationships' in st.session_state and st.session_state.entity_relationships:
                # Parse and create table view for relationships
                try:
                    # Parse the generated content to create a relationships table
                    lines = st.session_state.entity_relationships.split('\n')
                    relationships_data = []
                    
                    for line in lines:
                        line = line.strip()
                        # Remove any asterisk formatting
                        line = line.replace('*', '')
                        
                        if ' - ' in line and line.count(' - ') >= 3:
                            # This should be a relationship mapping line
                            parts = line.split(' - ')
                            if len(parts) >= 4:
                                source_entity = parts[0].strip()
                                target_entity = parts[1].strip()
                                cardinality = parts[2].strip()
                                description = ' - '.join(parts[3:]).strip()
                                
                                relationships_data.append({
                                    'Source Entity': source_entity,
                                    'Target Entity': target_entity,
                                    'Cardinality': cardinality,
                                    'Relationship Description': description
                                })
                    
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
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        st.session_state.data_elements_df.to_excel(writer, sheet_name='Data Elements', index=False)
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
