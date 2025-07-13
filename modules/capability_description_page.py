import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import capability_description_prompt, model

def capability_description_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_description"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Capability Description Generation")
    
    # Option 1: Use capabilities from mapping
    if 'capability_mapping' in st.session_state and st.session_state['capability_mapping']:
        st.markdown("### Generate Descriptions from Capability Mapping")
        st.markdown("**Existing Capability Mapping:**")
        st.markdown(st.session_state['capability_mapping'])
        
        if st.button("Generate Descriptions from Mapping", type="primary"):
            with st.spinner("Generating detailed capability descriptions..."):
                # Use the existing mapping as input
                _input = capability_description_prompt.format(
                    additional_prompts="Based on the capability mapping provided above",
                    capabilities=st.session_state['capability_mapping']
                )
                
                # Get AI response
                output = model.invoke([HumanMessage(content=_input)])
                descriptions = output.content
                
                # Store descriptions in session state
                st.session_state['capability_descriptions'] = descriptions
                
                # Display descriptions
                st.markdown("### Generated Capability Descriptions")
                st.markdown(descriptions)
        
        st.markdown("---")
    
    # Option 2: Manual capability input
    st.markdown("### Manual Capability Input")
    st.markdown("Enter specific capabilities you want detailed descriptions for:")
    
    capabilities_input = st.text_area(
        "Capabilities to describe:",
        placeholder="Enter capabilities, one per line:\n- Process Management\n- Data Analytics\n- Customer Experience Management",
        height=150
    )
    
    additional_prompts = st.text_area(
        "Additional context for capability descriptions:", 
        placeholder="e.g., Focus on digital transformation, include implementation timelines, consider industry-specific requirements..."
    )
    
    if st.button("Generate Custom Descriptions", type="secondary"):
        if capabilities_input.strip():
            with st.spinner("Generating capability descriptions..."):
                # Generate prompt
                _input = capability_description_prompt.format(
                    additional_prompts=additional_prompts,
                    capabilities=capabilities_input
                )
                
                # Get AI response
                output = model.invoke([HumanMessage(content=_input)])
                descriptions = output.content
                
                # Store descriptions in session state
                st.session_state['capability_descriptions'] = descriptions
                
                # Display descriptions
                st.markdown("### Generated Capability Descriptions")
                st.markdown(descriptions)
        else:
            st.error("Please enter at least one capability to describe.")
    
    # No previous data available
    if 'capability_mapping' not in st.session_state or not st.session_state['capability_mapping']:
        st.info("💡 Tip: For better results, run the Capability Mapping tool first to identify relevant capabilities.")
    
    # Display previously generated descriptions if they exist
    if 'capability_descriptions' in st.session_state and st.session_state['capability_descriptions']:
        st.markdown("---")
        st.markdown("### Previously Generated Descriptions")
        st.markdown(st.session_state['capability_descriptions'])
