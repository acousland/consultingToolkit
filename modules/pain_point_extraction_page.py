import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import pain_point_extraction_prompt, model, comma_list_parser

def pain_point_extraction_page():
    # Home button
    if st.button("🏠 Go to Home", key="home_from_extraction"):
        st.session_state.page = "Home"
        st.rerun()
    
    st.markdown("## Pain Point extraction")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        if uploaded_file.name.endswith('.csv'):
            dataframe = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
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

        if st.button("Generate pain points", type="secondary"):
            _input = pain_point_extraction_prompt.format(additional_prompts=prompts,
                                   data=concatenated_data)
            output = model.invoke([HumanMessage(content=_input)])
            pain_points = comma_list_parser.parse(output.content)
            st.session_state['pain_points'] = pain_points
            st.write(pain_points)

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
