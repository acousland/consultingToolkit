import streamlit as st
from navigation import render_breadcrumbs
from app_config import model
from langchain_core.messages import HumanMessage


def use_case_ethics_review_page():
    """Use Case Ethics Review tool for comprehensive ethical analysis of use cases."""
    
    # Breadcrumbs
    render_breadcrumbs([
        ("Home", "Home"), 
        ("Data, Information, and AI Toolkit", "Data, Information, and AI Toolkit"),
        ("Use Case Ethics Review", None)
    ])
    
    st.markdown("# ⚖️ Use Case Ethics Review")
    st.markdown("Conduct a comprehensive ethical analysis of your use case from multiple philosophical perspectives.")
    
    st.markdown("""
    **This tool provides:**
    - **Deontological Analysis** (Kantian ethics): Rule-based evaluation considering laws, policies, and universal principles
    - **Utilitarian Analysis**: Cost-benefit evaluation with quantified pros and cons
    - **Social Contract Analysis**: Assessment of implicit and explicit social agreements
    - **Virtue Ethics Analysis**: Evaluation of character and organizational virtue implications
    """)
    
    st.markdown("---")
    
    # Use Case Input Section
    st.markdown("## 📝 Use Case Description")
    st.markdown("Please provide a detailed description of your use case for ethical analysis.")
    
    use_case_description = st.text_area(
        "Describe your use case in detail:",
        placeholder="""Please include as much detail as possible:
- What is the use case about?
- Who are the stakeholders involved?
- What data or resources will be used?
- What are the intended outcomes?
- How will it be implemented?
- What are the potential impacts on different groups?
- Any relevant context about your organization or industry...""",
        height=200,
        help="The more detail you provide, the more comprehensive and accurate the ethical analysis will be."
    )
    
    if not use_case_description.strip():
        st.info("👆 Please provide a detailed description of your use case to begin the ethical analysis.")
        return
    
    st.markdown("---")
    
    # Analysis Section
    st.markdown("## 🔍 Ethical Analysis")
    
    if st.button("🚀 Conduct Ethics Review", type="primary"):
        with st.spinner("Conducting comprehensive ethical analysis..."):
            try:
                # Analysis 1: Deontological (Kantian) Analysis
                st.markdown("### 1. 📜 Deontological Analysis (Kantian Ethics)")
                st.markdown("*Rule-based evaluation considering laws, policies, and universal principles*")
                
                with st.spinner("Analyzing rules, laws, and universal principles..."):
                    kantian_prompt = f"""You are an expert in deontological ethics. Analyze this use case from a Kantian perspective with CONCISE, focused responses.

Use Case: {use_case_description}

Provide a brief analysis (3-4 paragraphs maximum) covering:

1. **Legal & Policy Compliance**: Key laws, regulations, or policies that may be affected
2. **Categorical Imperative Test**: Could this become a universal law? Does it treat people as ends, not means?
3. **Rights & Duties**: What rights and duties are at stake?
4. **Compliance Rating**: Rate 1-10 (1=major violations, 10=fully compliant)

Be concise and focused on the most critical deontological concerns."""

                    kantian_response = model.invoke([HumanMessage(content=kantian_prompt)])
                    st.markdown(kantian_response.content)
                
                st.markdown("---")
                
                # Analysis 2: Utilitarian Analysis
                st.markdown("### 2. ⚖️ Utilitarian Analysis")
                st.markdown("*Cost-benefit evaluation with quantified pros and cons*")
                
                with st.spinner("Analyzing costs, benefits, and overall utility..."):
                    utilitarian_prompt = f"""You are an expert in utilitarian ethics. Analyze this use case with CONCISE, focused responses.

Use Case: {use_case_description}

Provide a brief analysis (3-4 paragraphs maximum) covering:

1. **Key Stakeholders**: Who are the main affected parties?
2. **Major Benefits**: Top 3-5 positive outcomes with impact scores (1-10)
3. **Major Costs/Harms**: Top 3-5 negative outcomes with impact scores (1-10)
4. **Net Utilitarian Score**: [Total benefits - Total costs] and overall assessment

Be concise and focus on the most significant utilitarian impacts. Provide clear numerical scoring."""

                    utilitarian_response = model.invoke([HumanMessage(content=utilitarian_prompt)])
                    st.markdown(utilitarian_response.content)
                
                st.markdown("---")
                
                # Analysis 3: Social Contract Analysis
                st.markdown("### 3. 🤝 Social Contract Analysis")
                st.markdown("*Assessment of implicit and explicit social agreements*")
                
                with st.spinner("Analyzing social contracts and agreements..."):
                    social_contract_prompt = f"""You are an expert in social contract theory. Analyze this use case with CONCISE, focused responses.

Use Case: {use_case_description}

Provide a brief analysis (3-4 paragraphs maximum) covering:

1. **Explicit Contracts**: What formal agreements (employment, user terms, privacy policies) might be affected?
2. **Implicit Expectations**: What unwritten social expectations and trust relationships are at stake?
3. **Stakeholder Impact**: How might employees, customers, community, and partners be affected?
4. **Social License Rating**: Rate 1-10 (1=major violations of social trust, 10=fully aligned with social expectations)

Be concise and focus on the most critical social contract implications."""

                    social_contract_response = model.invoke([HumanMessage(content=social_contract_prompt)])
                    st.markdown(social_contract_response.content)
                
                st.markdown("---")
                
                # Analysis 4: Virtue Ethics Analysis
                st.markdown("### 4. 🌟 Virtue Ethics Analysis")
                st.markdown("*Evaluation of character and organizational virtue implications*")
                
                with st.spinner("Analyzing virtue and character implications..."):
                    virtue_ethics_prompt = f"""You are an expert in virtue ethics. Analyze this use case with CONCISE, focused responses.

Use Case: {use_case_description}

Provide a brief analysis (3-4 paragraphs maximum) covering:

1. **Key Virtues Assessment**: How does this align with core virtues (honesty, justice, compassion, courage, wisdom, respect)?
2. **Organizational Character**: What character traits would this cultivate in the organization?
3. **Role Model Test**: Would a virtuous organization want to be known for this use case?
4. **Virtue Rating**: Rate 1-10 (1=promotes vices, 10=exemplifies virtue)

Be concise and focus on the most significant virtue and character implications."""

                    virtue_ethics_response = model.invoke([HumanMessage(content=virtue_ethics_prompt)])
                    st.markdown(virtue_ethics_response.content)
                
                st.markdown("---")
                
                # Generate Comprehensive Summary
                st.markdown("## 📋 Comprehensive Ethics Review Summary")
                
                with st.spinner("Generating comprehensive summary..."):
                    summary_prompt = f"""You are an expert ethics advisor. Based on the use case analysis, create a COMPREHENSIVE EXECUTIVE SUMMARY.

Use Case: {use_case_description}

Create a structured executive summary with these sections:

## Executive Summary

### 🎯 Overall Ethics Assessment
Provide an overall ethical recommendation (Proceed/Proceed with Caution/Do Not Proceed) with key reasoning.

### 📊 Ethics Framework Scores Summary
- **Deontological (Rules/Law) Score**: X/10 - Brief reasoning
- **Utilitarian (Cost/Benefit) Score**: X/10 - Brief reasoning  
- **Social Contract Score**: X/10 - Brief reasoning
- **Virtue Ethics Score**: X/10 - Brief reasoning
- **Overall Composite Score**: X/10

### ⚠️ Critical Risk Areas
List the top 3-5 most significant ethical concerns that require attention.

### ✅ Ethical Strengths  
List the top 3-5 ethical advantages or positive aspects of this use case.

### 🔄 Key Recommendations
Provide 3-5 specific, actionable recommendations to improve ethical alignment.

### 🚦 Implementation Gates
Suggest specific checkpoints or approvals needed before proceeding.

### 📋 Stakeholder Consultation
Identify key stakeholders who should be consulted before implementation.

Keep the summary concise but comprehensive - aim for executive-level briefing format."""

                    summary_response = model.invoke([HumanMessage(content=summary_prompt)])
                    st.markdown(summary_response.content)
                
                st.success("✅ Comprehensive ethical analysis completed!")
                
                st.markdown("""
                **Next Steps:**
                1. Review the executive summary carefully  
                2. Address critical risk areas identified
                3. Implement key recommendations  
                4. Consult with identified stakeholders
                5. Consider establishing implementation gates
                6. Document your ethical decision-making process
                7. Plan for ongoing ethical monitoring
                
                **Remember:** This analysis is meant to inform decision-making, not replace human judgment and consultation with relevant experts, legal counsel, and stakeholders.
                """)
                
            except Exception as e:
                st.error(f"Error conducting ethical analysis: {e}")
                st.markdown("**Troubleshooting suggestions:**")
                st.markdown("- Check your AI model configuration in the Admin Tool")
                st.markdown("- Ensure your use case description is clear and detailed")
                st.markdown("- Try again with a shorter description if the request is too large")


if __name__ == "__main__":
    use_case_ethics_review_page()
