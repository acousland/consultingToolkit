import streamlit as st
from typing import List, Tuple, Optional, Callable

# Type alias for breadcrumb items
BreadcrumbItem = Tuple[str, Optional[str]]  # (label, target page)


def render_breadcrumbs(items: List[BreadcrumbItem]) -> None:
    """Render a breadcrumb navigation bar.

    Parameters
    ----------
    items: List of tuples where each tuple contains the label to display and
        an optional target page name. When a target page is provided, a button
        is rendered that navigates to that page when clicked. The last item is
        treated as the current page and should typically have ``None`` as the
        target.
    """
    breadcrumb_container = st.container()

    # Build column weights: slightly wider first column, arrows in between,
    # last column a bit larger.
    weights = []
    for i, _ in enumerate(items):
        if i == 0:
            weights.append(1.2)
        elif i == len(items) - 1 and len(items) == 2:
            weights.append(4)
        elif i == len(items) - 1:
            weights.append(3)
        else:
            weights.append(2.2)
        if i < len(items) - 1:
            weights.append(0.2)

    with breadcrumb_container:
        cols = st.columns(weights)
        for i, (label, page) in enumerate(items):
            with cols[i * 2]:
                if page:
                    key = f"breadcrumb_{label.replace(' ', '_').lower()}_{i}"
                    if st.button(label, key=key, help=f"Go to {label}"):
                        st.session_state.page = page
                        st.rerun()
                else:
                    st.markdown(f"**{label}**")
            if i < len(items) - 1:
                with cols[i * 2 + 1]:
                    st.markdown("**›**")
    st.markdown("---")


# Mapping of page names to their corresponding functions
PageFunc = Callable[[], None]
PAGE_ROUTES: dict[str, PageFunc] = {}

# Page modules imported below for route mapping
from modules.home_page import home_page
from modules.pain_point_toolkit.pain_point_toolkit_page import pain_point_toolkit_page
from modules.capability_toolkit.capability_toolkit_page import capability_toolkit_page
from modules.capability_toolkit.capability_description_page import capability_description_page
from modules.applications_toolkit.applications_toolkit_page import applications_toolkit_page
from modules.pain_point_toolkit.pain_point_extraction_page import pain_point_extraction_page
from modules.pain_point_toolkit.capability_mapping_page import capability_mapping_page
from modules.pain_point_toolkit.theme_creation_page import theme_creation_page
from modules.pain_point_toolkit.pain_point_impact_estimation_page import pain_point_impact_estimation_page
from modules.applications_toolkit.application_capability_mapping_page import application_capability_mapping_page
from modules.applications_toolkit.application_categorization_page import application_categorization_page
from modules.applications_toolkit.logical_application_model_generator_page import logical_application_model_generator_page
from modules.applications_toolkit.individual_application_mapping_page import individual_application_mapping_page
from modules.engagement_planning_toolkit.engagement_planning_toolkit_page import engagement_planning_toolkit_page
from modules.engagement_planning_toolkit.engagement_touchpoint_planning_page import engagement_touchpoint_planning_page
from modules.strategy_motivations_toolkit.strategy_motivations_toolkit_page import strategy_motivations_toolkit_page
from modules.strategy_motivations_toolkit.strategy_capability_mapping_page import strategy_capability_mapping_page
from modules.strategy_motivations_toolkit.initiatives_strategy_generator_page import initiatives_strategy_generator_page
from modules.data_information_toolkit.data_information_toolkit_page import data_information_toolkit_page
from modules.data_information_toolkit.conceptual_data_model_generator_page import conceptual_data_model_generator_page
from modules.data_information_toolkit.data_application_mapping_page import data_application_mapping_page
from modules.data_information_toolkit.ai_use_case_customiser_page import ai_use_case_customiser_page
from modules.data_information_toolkit.use_case_ethics_review_page import use_case_ethics_review_page
from modules.admin_tool_page import admin_tool_page

# Dictionary mapping page names to functions
PAGE_ROUTES: dict[str, PageFunc] = {
    "Home": home_page,
    "Pain Point Toolkit": pain_point_toolkit_page,
    "Capability Toolkit": capability_toolkit_page,
    "Applications Toolkit": applications_toolkit_page,
    "Engagement Planning Toolkit": engagement_planning_toolkit_page,
    "Strategy and Motivations Toolkit": strategy_motivations_toolkit_page,
    "Data, Information, and AI Toolkit": data_information_toolkit_page,
    "Pain Point Extraction": pain_point_extraction_page,
    "Pain Point Theme Creation": theme_creation_page,
    "Pain Point to Capability Mapping": capability_mapping_page,
    "Pain Point Impact Estimation": pain_point_impact_estimation_page,
    "Application to Capability Mapping": application_capability_mapping_page,
    "Application Categorisation": application_categorization_page,
    "Logical Application Model Generator": logical_application_model_generator_page,
    "Individual Application to Capability Mapping": individual_application_mapping_page,
    "Engagement Touchpoint Planning": engagement_touchpoint_planning_page,
    "Capability Description Generation": capability_description_page,
    "Strategy to Capability Mapping": strategy_capability_mapping_page,
    "Tactics to Strategies Generator": initiatives_strategy_generator_page,
    "Conceptual Data Model Generator": conceptual_data_model_generator_page,
    "Data-Application Mapping": data_application_mapping_page,
    "AI Use Case Customiser": ai_use_case_customiser_page,
    "Use Case Ethics Review": use_case_ethics_review_page,
    "Admin Tool": admin_tool_page,
}
