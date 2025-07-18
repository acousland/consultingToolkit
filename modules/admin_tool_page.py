import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import model


def admin_tool_page():
    # Breadcrumb navigation
    breadcrumb_container = st.container()
    with breadcrumb_container:
        col1, col2, col3 = st.columns([1.2, 0.2, 4])
        with col1:
            if st.button("🏠 Home", key="breadcrumb_home", help="Go to Home"):
                st.session_state.page = "Home"
                st.rerun()
        with col2:
            st.markdown("**›**")
        with col3:
            st.markdown("**⚙️ Admin & Testing Tool**")

    st.markdown("---")
    st.markdown("## Connection Check")

    # Check for OpenAI API key
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        st.success("OpenAI API key detected")
    else:
        st.error("OpenAI API key not found in Streamlit secrets")

    # Display configured model name
    model_name = getattr(model, "model_name", "Unknown")
    st.info(f"Configured model: **{model_name}**")

    if st.button("Run connectivity test", type="primary"):
        with st.spinner("Contacting model..."):
            try:
                response = model.invoke([HumanMessage(content="Hello")])
                st.success("Model responded successfully")
                st.write(response.content)
            except Exception as e:
                st.error(f"Failed to connect: {e}")

