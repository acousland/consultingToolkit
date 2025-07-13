import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import capability_mapping_prompt, model

def capability_mapping_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_mapping"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point to Capability Mapping")
    
    # Check if pain points or themes exist in session state
    has_pain_points = 'pain_points' in st.session_state and st.session_state['pain_points']
    has_themes = 'themes' in st.session_state and st.session_state['themes']
    
    if has_pain_points or has_themes:
        # Input selection
        input_choice = st.radio(
            "What would you like to map to capabilities?",
            ["Pain Points", "Themes"] if has_themes else ["Pain Points"],
            help="Choose whether to map individual pain points or grouped themes to capabilities"
        )
        
        if input_choice == "Pain Points" and has_pain_points:
            st.markdown("### Pain Points to Map")
            pain_points_list = st.session_state['pain_points']
            
            # Display current pain points
            for i, point in enumerate(pain_points_list, 1):
                st.write(f"{i}. {point}")
            
            input_data = "\n".join([f"- {point}" for point in pain_points_list])
            
        elif input_choice == "Themes" and has_themes:
            st.markdown("### Themes to Map")
            st.markdown(st.session_state['themes'])
            input_data = st.session_state['themes']
        
        st.markdown("---")
        
        # Additional prompts input
        additional_prompts = st.text_area(
            "Additional context for capability mapping:", 
            placeholder="e.g., Focus on digital capabilities, prioritize customer-facing capabilities, consider budget constraints..."
        )
        
        # Generate capability mapping button
        if st.button("Generate Capability Mapping", type="primary"):
            with st.spinner("Mapping to organizational capabilities..."):
                # Generate prompt
                _input = capability_mapping_prompt.format(
                    additional_prompts=additional_prompts,
                    input_data=input_data
                )
                
                # Get AI response
                output = model.invoke([HumanMessage(content=_input)])
                capability_mapping = output.content
                
                # Store mapping in session state
                st.session_state['capability_mapping'] = capability_mapping
                
                # Display mapping
                st.markdown("### Capability Mapping Results")
                st.markdown(capability_mapping)
    else:
        st.info("🔍 No pain points or themes found. Please run the Pain Point Extraction tool first.")
    
    # Display previously generated mapping if it exists
    if 'capability_mapping' in st.session_state and st.session_state['capability_mapping']:
        st.markdown("---")
        st.markdown("### Previously Generated Capability Mapping")
        st.markdown(st.session_state['capability_mapping'])
