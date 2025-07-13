import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import theme_creation_prompt, model

def theme_creation_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_theme"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point Theme Creation")
    
    # Check if pain points exist in session state
    if 'pain_points' in st.session_state and st.session_state['pain_points']:
        st.markdown("### Extracted Pain Points")
        pain_points_list = st.session_state['pain_points']
        
        # Display current pain points
        for i, point in enumerate(pain_points_list, 1):
            st.write(f"{i}. {point}")
        
        st.markdown("---")
        
        # Additional prompts input
        additional_prompts = st.text_area(
            "Additional context or specific theming instructions:", 
            placeholder="e.g., Focus on operational vs strategic themes, or group by department..."
        )
        
        # Generate themes button
        if st.button("Generate Themes", type="primary"):
            with st.spinner("Analyzing pain points and creating themes..."):
                # Format pain points as a string
                pain_points_text = "\n".join([f"- {point}" for point in pain_points_list])
                
                # Generate prompt
                _input = theme_creation_prompt.format(
                    additional_prompts=additional_prompts,
                    pain_points=pain_points_text
                )
                
                # Get AI response
                output = model.invoke([HumanMessage(content=_input)])
                themes = output.content
                
                # Store themes in session state
                st.session_state['themes'] = themes
                
                # Display themes
                st.markdown("### Generated Themes")
                st.markdown(themes)
    else:
        st.info("🔍 No pain points found. Please run the Pain Point Extraction tool first to generate themes.")
    
    # Display previously generated themes if they exist
    if 'themes' in st.session_state and st.session_state['themes']:
        st.markdown("---")
        st.markdown("### Previously Generated Themes")
        st.markdown(st.session_state['themes'])
