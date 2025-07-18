import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs


def admin_tool_page():
    render_breadcrumbs([("🏠 Home", "Home"), ("⚙️ Admin & Testing Tool", None)])
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

    st.markdown("---")
    st.markdown("## Additional Tools")
    st.info("Additional admin tools can be added here as needed.")
