import streamlit as st
from langchain_core.messages import HumanMessage
from app_config import model
from navigation import render_breadcrumbs
from .api_key_manager import (
    list_keys,
    add_key,
    remove_key,
    set_active_key,
    get_active_key,
)


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
    st.markdown("## API Key Management")

    keys = list_keys()
    active = get_active_key()

    if keys:
        selected = st.radio(
            "Available keys",
            keys,
            index=keys.index(active) if active in keys else 0,
            key="key_select",
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Set Active", key="set_active"):
                set_active_key(selected)
                st.rerun()
        with col2:
            if st.button("Remove Key", key="remove_key"):
                remove_key(selected)
                st.rerun()
    else:
        st.info("No API keys configured.")

    with st.form("add_key_form"):
        st.markdown("### Add New Key")
        new_name = st.text_input("Key label")
        new_value = st.text_input("Key value", type="password")
        submitted = st.form_submit_button("Add Key")
        if submitted and new_name and new_value:
            add_key(new_name, new_value)
            st.success("Key added")
            st.rerun()
