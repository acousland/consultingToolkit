import json
import os
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load model configuration from JSON file
def load_model_config():
    config_path = os.path.join(os.path.dirname(__file__), "model_config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get("openai_model", "o1-mini"), config.get("temperature", 1)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to defaults if config file doesn't exist or is invalid
        return "o1-mini", 1

# Load current configuration
current_model, current_temperature = load_model_config()

# Common model configuration - use 'model' parameter for newer LangChain versions
model = ChatOpenAI(model=current_model, temperature=current_temperature)

def reinitialize_model():
    """Reinitialize the model with current configuration"""
    global model, current_model, current_temperature
    current_model, current_temperature = load_model_config()
    model = ChatOpenAI(model=current_model, temperature=current_temperature)
    return model

# Output parsers
comma_list_parser = CommaSeparatedListOutputParser()
comma_format_instructions = comma_list_parser.get_format_instructions()

# PAIN POINT EXTRACTION PROMPT
pain_point_extraction_prompt = PromptTemplate(
    template="""You are a senior management consultant (MBA) and organisational psychologist (PhD).
Extract every distinct pain point from the text and return them as clear, single sentences.

Requirements:
- Each pain point should be one complete, standalone sentence
- Use Australian English with proper grammar
- Focus on the core problem or challenge
- Be specific about what the pain point is
- Keep each sentence concise but descriptive
- Do not include metrics or specific numbers unless essential to understanding the problem

Format: Return only a simple list, one pain point per line, like this:
Social media engagement rates are consistently below industry benchmarks across all platforms.
Website conversion rates are underperforming expected targets.
Customer data access is limited by system restrictions.

{additional_prompts}

Text to analyse:
{data}
""",
    input_variables=["additional_prompts", "data"]
)

# THEME CREATION PROMPT
theme_creation_prompt = PromptTemplate(
    template="""You are a management consultant specialising in organisational analysis and strategic planning. \
    I will provide you with a list of extracted pain points from an organisation. \
    Your task is to analyse these pain points and group them into meaningful themes or categories.
    
    For each theme, provide:
    1. A clear, descriptive theme name
    2. A brief explanation of what this theme represents
    3. The pain points that belong to this theme
    
    Guidelines:
    - Create 3-7 themes maximum
    - Themes should represent different aspects of organisational challenges
    - Common themes might include: Process Inefficiencies, Technology Gaps, Communication Issues, Resource Constraints, Customer Experience, etc.
    - Each pain point should belong to one primary theme
    - Provide actionable insights for each theme
    
    {additional_prompts}
    
    Format your response as: Theme Name: Description
    List of related pain points for each theme.
    
    Pain points to analyse:
    {pain_points}
    """,
    input_variables=["additional_prompts", "pain_points"]
)

# CAPABILITY MAPPING PROMPT  
capability_mapping_prompt = PromptTemplate(
    template="""You are a management consultant with expertise in organisational capabilities and business architecture. \
    I will provide you with pain points and/or themes from an organisation. \
    Your task is to map these pain points to the organisational capabilities that need to be developed, improved, or acquired to address them.
    
    For each pain point or theme, identify:
    1. The primary organisational capability required
    2. The capability maturity level needed (Basic, Intermediate, Advanced)
    3. The business impact of developing this capability
    4. Priority level (High, Medium, Low)
    
    Common capability areas include:
    - Process Management & Optimisation
    - Technology & Digital Capabilities
    - Data & Analytics
    - Communication & Collaboration
    - Customer Experience Management
    - Change Management
    - Resource Management
    - Leadership & Governance
    
    {additional_prompts}
    
    Format your response clearly showing the mapping between pain points and required capabilities.
    
    Pain points/themes to map:
    {input_data}
    """,
    input_variables=["additional_prompts", "input_data"]
)

# CAPABILITY DESCRIPTION PROMPT
capability_description_prompt = PromptTemplate(
    template="""
You are a management consultant and business architect with deep expertise in organisational capabilities.
Write a single-sentence description for each capability provided.

Style guardrails
– Use Australian English, present tense, active voice, and an Oxford comma.
– Verb guidance
  • Draw the opening verb(s) from: craft, create, cultivate, develop, engineer, evolve, forge, hone, pilot, pioneer, shape, steer, streamline.
  • Use each verb no more than three times across the full output, and never twice in a row.
– One short qualifier is allowed (e.g., "through data-driven insight").
– Keep each sentence ≤ 30 words.
– Avoid any stock trio like "identify, analyse, optimise".

Example  
Customer Insight & Analytics: The ability to uncover fresh patterns in purchasing behaviour, convert them into actionable tactics, and steer smarter investment decisions across every retail touch-point.

Return the results exactly like this  
(no bullets, no asterisks)  
Capability Name: The ability to …

Capabilities to describe:
{capabilities}
""",
    input_variables=["capabilities"]
)

# REVISED PAIN-POINT IMPACT ESTIMATION PROMPT
pain_point_impact_estimation_prompt = PromptTemplate(
    template="""
You are a senior business analyst specialising in enterprise-level impact assessment.
Evaluate each pain point **only** in terms of its likely effect on:
1. The organisation’s declared strategic priorities, and
2. Profitability (EBITDA or net margin) over the next 12–24 months.

{context_section}

**Classification rules**

- High – Materially jeopardises at least one strategic priority **or** is plausibly
  expected to reduce profit by ~2 percent or more (e.g., lost revenue, increased cost,
  regulatory penalties). Requires immediate executive attention.

- Medium – Has a clear but limited influence on a strategic priority **or** could move
  profit by roughly 0.5 – 2 percent. Worth addressing, but not urgent at C-suite level.

- Low – Little or no measurable influence on strategic priorities and unlikely to
  shift profit by more than ~0.5 percent. Improvements are discretionary or cosmetic.

If evidence is ambiguous, err toward the lower category.

Respond with **only** the impact level (High, Medium, or Low) for each pain point,
in the order provided. {context_instruction}

Pain points to assess:
{pain_points}
""",
    input_variables=["context_section", "context_instruction", "pain_points"]
)

# Legacy exports for backward compatibility
output_parser = comma_list_parser
format_instructions = comma_format_instructions
prompt = pain_point_extraction_prompt
