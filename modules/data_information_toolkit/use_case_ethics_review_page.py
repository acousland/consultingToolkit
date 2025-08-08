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
                    kantian_prompt = f"""You are an expert in deontological ethics and legal compliance. Analyze the following use case from a Kantian perspective, focusing on rules, laws, and universal principles.

Use Case:
{use_case_description}

Conduct a thorough deontological analysis covering:

1. **Legal Compliance**:
   - What laws might this use case potentially violate? (Consider privacy laws, discrimination laws, labor laws, etc.)
   - Are there any regulatory requirements that need to be considered?
   - What licenses or permissions might be required?

2. **Policy Violations**:
   - What organizational policies might be affected?
   - Are there industry standards or codes of conduct that apply?
   - What professional ethical guidelines are relevant?

3. **Kantian Categorical Imperative Test**:
   - Universal Law Test: Could this action become a universal law that everyone follows?
   - Humanity as End Test: Does this treat people as ends in themselves, not merely as means?
   - Kingdom of Ends Test: Would rational agents in an ideal moral community accept this?

4. **Rights and Duties Analysis**:
   - What rights of individuals or groups might be affected?
   - What duties does the organization have to various stakeholders?
   - Are there conflicting duties that need to be balanced?

Provide a detailed, objective analysis. Do not assume the use case is inherently good or bad - evaluate based on the ethical framework."""

                    kantian_response = model.invoke([HumanMessage(content=kantian_prompt)])
                    st.markdown(kantian_response.content)
                
                st.markdown("---")
                
                # Analysis 2: Utilitarian Analysis
                st.markdown("### 2. ⚖️ Utilitarian Analysis")
                st.markdown("*Cost-benefit evaluation with quantified pros and cons*")
                
                with st.spinner("Analyzing costs, benefits, and overall utility..."):
                    utilitarian_prompt = f"""You are an expert in utilitarian ethics and cost-benefit analysis. Analyze the following use case from a utilitarian perspective, focusing on maximizing overall well-being and happiness.

Use Case:
{use_case_description}

Conduct a comprehensive utilitarian analysis:

1. **Identify All Stakeholders**:
   - Who will be affected by this use case?
   - Consider direct and indirect stakeholders
   - Include individuals, groups, organizations, and society

2. **Detailed Pros Analysis**:
   List all potential positive outcomes and assign utilitarian points (1-10 scale):
   - Economic benefits
   - Efficiency gains
   - Quality of life improvements
   - Innovation and progress
   - Other positive impacts
   
   For each pro, explain:
   - Who benefits and how many people
   - Magnitude of the benefit
   - Likelihood of the benefit occurring
   - Assign points: 1-3 (minor), 4-6 (moderate), 7-8 (significant), 9-10 (major)

3. **Detailed Cons Analysis**:
   List all potential negative outcomes and assign utilitarian points (1-10 scale):
   - Economic costs
   - Harm to individuals or groups
   - Loss of privacy or autonomy
   - Environmental impacts
   - Other negative consequences
   
   For each con, explain:
   - Who is harmed and how many people
   - Magnitude of the harm
   - Likelihood of the harm occurring
   - Assign points: 1-3 (minor), 4-6 (moderate), 7-8 (significant), 9-10 (major)

4. **Utilitarian Calculation**:
   - Total Pro Points: [sum]
   - Total Con Points: [sum]
   - Net Utilitarian Score: [pros - cons]
   - Overall Assessment: Is this use case utilitarian-positive or negative?

5. **Sensitivity Analysis**:
   - What assumptions could change the outcome?
   - What uncertainties exist in the analysis?

Be objective and thorough. Consider both short-term and long-term consequences."""

                    utilitarian_response = model.invoke([HumanMessage(content=utilitarian_prompt)])
                    st.markdown(utilitarian_response.content)
                
                st.markdown("---")
                
                # Analysis 3: Social Contract Analysis
                st.markdown("### 3. 🤝 Social Contract Analysis")
                st.markdown("*Assessment of implicit and explicit social agreements*")
                
                with st.spinner("Analyzing social contracts and agreements..."):
                    social_contract_prompt = f"""You are an expert in social contract theory and organizational sociology. Analyze the following use case from a social contract perspective, examining both explicit and implicit agreements.

Use Case:
{use_case_description}

Conduct a thorough social contract analysis:

1. **Explicit Social Contracts**:
   - What formal agreements might be affected? (employment contracts, user agreements, etc.)
   - Are there explicit terms of service or privacy policies that apply?
   - What legal contracts with customers, partners, or employees are relevant?
   - Are there explicit stakeholder commitments or promises?

2. **Implicit Social Contracts**:
   - What unwritten expectations do stakeholders have?
   - What social norms and conventions apply?
   - What implicit trust relationships exist?
   - What are the unstated assumptions about how the organization operates?

3. **Stakeholder Expectations Analysis**:
   - **Employees**: What do they expect in terms of job security, privacy, fair treatment?
   - **Customers**: What implicit promises about service, privacy, and value exist?
   - **Community**: What does society expect from the organization?
   - **Shareholders/Investors**: What implicit agreements about responsible business practices exist?
   - **Partners**: What mutual expectations and dependencies exist?

4. **Social Contract Violations Assessment**:
   - Which explicit contracts might be breached?
   - What implicit expectations might be violated?
   - How might trust relationships be affected?
   - What social norms might be challenged?

5. **Legitimacy and Authority**:
   - Does the organization have the social legitimacy to implement this use case?
   - What authority or permission from stakeholders might be needed?
   - How might this affect the organization's social license to operate?

6. **Potential for Renegotiation**:
   - Can affected social contracts be renegotiated fairly?
   - What transparency and communication would be needed?
   - How can stakeholder consent be obtained?

Provide an objective analysis of how this use case aligns with or challenges existing social contracts."""

                    social_contract_response = model.invoke([HumanMessage(content=social_contract_prompt)])
                    st.markdown(social_contract_response.content)
                
                st.markdown("---")
                
                # Analysis 4: Virtue Ethics Analysis
                st.markdown("### 4. 🌟 Virtue Ethics Analysis")
                st.markdown("*Evaluation of character and organizational virtue implications*")
                
                with st.spinner("Analyzing virtue and character implications..."):
                    virtue_ethics_prompt = f"""You are an expert in virtue ethics and organizational character. Analyze the following use case from a virtue ethics perspective, focusing on character traits and moral excellence.

Use Case:
{use_case_description}

Conduct a comprehensive virtue ethics analysis:

1. **Core Virtues Assessment**:
   Evaluate how this use case aligns with key virtues:
   - **Honesty/Integrity**: Does this promote truthfulness and authenticity?
   - **Justice/Fairness**: Does this treat all stakeholders fairly?
   - **Compassion/Care**: Does this show concern for others' well-being?
   - **Courage**: Does this require and demonstrate moral courage?
   - **Temperance/Moderation**: Does this show restraint and balance?
   - **Wisdom/Prudence**: Does this demonstrate good judgment and practical wisdom?
   - **Respect/Dignity**: Does this honor the dignity of all people involved?

2. **Organizational Character**:
   - What character traits would this use case cultivate in the organization?
   - How would this affect the organization's reputation and identity?
   - What kind of company would implement this use case?
   - How does this align with stated organizational values?

3. **Individual Character Development**:
   - How might this use case affect the character of employees involved?
   - What virtues or vices might it encourage in individuals?
   - Does it promote moral growth or moral compromise?

4. **Role Model Test**:
   - Would a virtuous organization want to be known for this use case?
   - Could this organization serve as a positive example to others?
   - What would stakeholders think if this became widely known?

5. **Virtue vs. Vice Analysis**:
   **Virtues Promoted**:
   - List virtues this use case would cultivate
   - Explain how each virtue is expressed
   
   **Vices Risked**:
   - List potential vices or character flaws this might encourage
   - Explain the risk factors

6. **Excellence and Flourishing**:
   - Does this contribute to human flourishing (eudaimonia)?
   - How does this promote or hinder excellence in the organization?
   - What is the impact on the common good?

7. **Virtue Ethics Conclusion**:
   - Would a virtuous agent pursue this use case?
   - How can the organization embody virtue while implementing this?
   - What modifications might enhance virtue alignment?

Provide an objective assessment focused on character and moral excellence."""

                    virtue_ethics_response = model.invoke([HumanMessage(content=virtue_ethics_prompt)])
                    st.markdown(virtue_ethics_response.content)
                
                st.markdown("---")
                
                # Summary Section
                st.markdown("## 📋 Ethics Review Summary")
                st.success("✅ Comprehensive ethical analysis completed!")
                
                st.markdown("""
                **Next Steps:**
                1. Review each analysis section carefully
                2. Consider how different ethical frameworks highlight different concerns
                3. Identify areas where modifications might improve ethical alignment
                4. Consult with relevant stakeholders and experts
                5. Document your ethical considerations and decisions
                
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
