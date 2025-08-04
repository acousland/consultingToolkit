# Centralised prompts used across the application

from langchain.prompts import PromptTemplate

# Pain Point Theme & Perspective Mapping prompt template
THEME_PERSPECTIVE_MAPPING_PROMPT = PromptTemplate(
    input_variables=["pain_points", "themes", "perspectives", "additional_context"],
    template="""You are an expert management consultant specialising in organisational analysis.

Your task: Map each pain point to the MOST APPROPRIATE theme and perspective from the provided lists.

Pain Points to Map:
{pain_points}
Available Themes:
{themes}
Available Perspectives:
{perspectives}
Additional Context: {additional_context}

Instructions:
1. For each pain point, analyse and determine which theme best categorises it
2. For each pain point, determine which perspective best represents the viewpoint/domain
3. Choose exactly one theme and one perspective for each pain point
4. Return your response in this exact format (one set per pain point):
PAIN_POINT_ID -> THEME: [theme_name] | PERSPECTIVE: [perspective_name]
5. Do NOT use any formatting like bold (**), italics (*), or backticks (`) in your response
6. Use plain text only for all IDs, themes, and perspectives

Example format:
PP001 -> THEME: Technology Limitations | PERSPECTIVE: Technology
PP002 -> THEME: Manual Processes | PERSPECTIVE: Process
PP003 -> THEME: Skills & Capacity | PERSPECTIVE: People

Mappings:"""
)

# Pain Point to Capability Mapping prompt template
PAIN_POINT_CAPABILITY_MAPPING_PROMPT = PromptTemplate(
    input_variables=["pain_points", "capabilities", "additional_context"],
    template="""You are an expert management consultant specialising in organisational capabilities.

Your task: Match each pain point to the MOST APPROPRIATE capability from the provided list.

Pain Points to Match:
{pain_points}
Available Capabilities:
{capabilities}
Additional Context: {additional_context}

Instructions:
1. For each pain point, analyse and determine which capability would best address it
2. Consider both direct solutions and preventive capabilities
3. Choose the single most appropriate capability ID for each pain point
4. Return your response in this exact format (one line per pain point):
PAIN_POINT_ID -> CAPABILITY_ID

Example format:
PP001 -> CAP003
PP002 -> CAP007
PP003 -> CAP001

Mappings:"""
)

# Application to Capability Mapping prompt template
APPLICATION_CAPABILITY_MAPPING_PROMPT = PromptTemplate(
    input_variables=["capabilities", "context_section"],
    template="""You are an enterprise architect mapping software applications to a business-capability model for a residential construction and home-building organisation.

**How to reason (think silently, do not show your thinking):**
1. Read each application's description carefully.
2. Scan the full name *and* the detailed prose for functional verbs, nouns, and domain cues.
3. Compare those cues to both the capability titles and their detailed descriptions.
4. Look for synonyms and near-synonyms (e.g., "CRM" → "Customer Relationship Management",  
   "virtual tour analytics" → "Marketing Analytics & Reporting").
5. Only count a capability when the application directly delivers, automates, or materially
   supports that business function. Ignore incidental or indirect links.

**Output rules (show only these in your answer):**
• Return just the Capability IDs, separated by commas, for each application.  
• Preserve the exact "Application Name:" label before the IDs.  
• If no clear capability match exists, output `NONE`.  
• Provide no explanations, qualifiers, or extra text.

{context_section}

Available Capabilities:
{capabilities}

Applications to map:"""
)

# Engagement Touchpoint Planning prompt template
ENGAGEMENT_TOUCHPOINT_PROMPT = PromptTemplate(
    input_variables=["engagement_type", "engagement_duration", "client_size", "engagement_phase", "touchpoint_frequency", "communication_style", "stakeholder_input", "objectives_input", "context_section"],
    template="""You are an experienced engagement manager and client relationship specialist. Your task is to create a comprehensive touchpoint plan for a consulting engagement.

Engagement Details:
- Type: {engagement_type}
- Duration: {engagement_duration}
- Client Size: {client_size}
- Current Phase: {engagement_phase}
- Touchpoint Frequency: {touchpoint_frequency}
- Communication Style: {communication_style}

Key Stakeholders:
{stakeholder_input}

Engagement Objectives:
{objectives_input}

{context_section}Create a comprehensive touchpoint plan that includes:

1. **ENGAGEMENT CALENDAR**: A timeline of key touchpoints throughout the engagement
2. **STAKEHOLDER MATRIX**: Specific communication plan for each stakeholder group
3. **TOUCHPOINT TYPES**: Different types of interactions (meetings, reports, check-ins, etc.)
4. **COMMUNICATION CADENCE**: Frequency and timing for each type of touchpoint
5. **MILESTONE REVIEWS**: Key decision points and milestone celebrations
6. **ESCALATION PROTOCOLS**: When and how to escalate issues or concerns
7. **SUCCESS MEASUREMENTS**: How to track and demonstrate progress

Format your response with clear sections and Australian English. Include specific recommendations for:
- Meeting formats and durations
- Reporting cadences
- Stakeholder-specific touchpoints
- Key milestone reviews
- Communication protocols

Make the plan practical and actionable for immediate implementation."""
)

# Individual Application Capability Mapping prompt template
INDIVIDUAL_APPLICATION_MAPPING_PROMPT = PromptTemplate(
    input_variables=["context_section", "app_info", "capabilities_text"],
    template="""You are an expert enterprise architect specialising in capability mapping and application portfolio management.

Your task: Analyse the application and identify which capabilities from the provided framework are most relevant.

{context_section}Application to Analyse:
{app_info}

Available Capabilities:
{capabilities_text}

Instructions:
1. Analyse the application's functions, purpose, and characteristics
2. Identify which capabilities from the framework are most relevant to this application
3. Consider both direct functional alignment and supporting capabilities
4. An application can map to multiple capabilities (0 to many)
5. Provide a confidence level for each mapping (High, Medium, Low)
6. Return your response in this exact format:

**Primary Capabilities** (High Confidence):
- CAPABILITY_ID: Brief explanation of relevance

**Secondary Capabilities** (Medium Confidence):
- CAPABILITY_ID: Brief explanation of relevance

**Potential Capabilities** (Low Confidence):
- CAPABILITY_ID: Brief explanation of relevance

If no capabilities are relevant, respond with:
**No Direct Capability Mappings Found**

Analysis:"""
)

# Strategic Initiatives Grouping prompt template
STRATEGY_GROUPING_PROMPT = PromptTemplate(
    input_variables=["context_section", "total_initiatives", "initiatives_text"],
    template="""You are a senior strategy consultant with expertise in strategic planning and portfolio analysis.

Task: Analyse the provided tactical initiatives and determine the optimal number of strategic activities (themes) they should be grouped into.

{context_section}Guidelines for Optimal Grouping:
- For 5-15 initiatives: Usually 3-4 strategic activities
- For 16-30 initiatives: Usually 4-6 strategic activities
- For 31-50 initiatives: Usually 5-7 strategic activities
- For 50+ initiatives: Usually 6-9 strategic activities
- Look for natural clusters and strategic coherence
- Avoid having too many small groups or too few large groups
- Each strategic activity should represent a distinct strategic approach

Instructions:
1. Review all tactical initiatives
2. Identify natural strategic themes and groupings
3. Determine the optimal number of strategic activities
4. Provide brief reasoning for your recommendation

Return your analysis in this exact format:

**RECOMMENDED NUMBER OF STRATEGIC ACTIVITIES:** [Number]

**REASONING:**
[2-3 sentences explaining why this number is optimal for this portfolio]

**PRELIMINARY STRATEGIC THEMES IDENTIFIED:**
1. [Brief theme name] - [1 sentence description]
2. [Brief theme name] - [1 sentence description]
[Continue for recommended number...]

Tactical Initiatives to Analyse ({total_initiatives} total):
{initiatives_text}

Analysis:"""
)

# Detailed Strategic Activities prompt template
STRATEGY_DETAILED_PROMPT = PromptTemplate(
    input_variables=["recommended_number", "context_section", "total_initiatives", "initiatives_text"],
    template="""You are a senior strategy consultant with deep expertise in strategic planning and tactical execution.

Your task: Create {recommended_number} strategic activities from the provided tactical initiatives, with unique IDs and comprehensive mapping.

{context_section}Strategic Framework:
- Tactics: The specific initiatives, projects, and activities being executed (what you're analysing)
- Strategic Activities: The broader strategic approaches these tactics are designed to deliver
- Each strategic activity needs a unique ID (SA-001, SA-002, etc.)

Instructions:
1. Create exactly {recommended_number} strategic activities
2. Assign each strategic activity a unique ID (SA-001, SA-002, SA-003, etc.)
3. Map each tactical initiative to the most appropriate strategic activity
4. Ensure every tactical initiative is mapped to exactly one strategic activity
5. Provide comprehensive details for each strategic activity

Return your analysis in this exact format:

**STRATEGIC ACTIVITY SA-001: [Strategic Activity Name]**
*Strategic Description:* [3-4 sentences describing the strategic approach and methodology]
*Mapped Tactics:* [Tactic_ID_1, Tactic_ID_2, Tactic_ID_3, ...]
*Success Factors:* [2-3 key factors critical to success]
*Risk Considerations:* [2-3 main risks or challenges]
*Expected Outcomes:* [2-3 strategic outcomes this activity should deliver]

**STRATEGIC ACTIVITY SA-002: [Strategic Activity Name]**
*Strategic Description:* [3-4 sentences describing the strategic approach and methodology]
*Mapped Tactics:* [Tactic_ID_1, Tactic_ID_2, Tactic_ID_3, ...]
*Success Factors:* [2-3 key factors critical to success]
*Risk Considerations:* [2-3 main risks or challenges]
*Expected Outcomes:* [2-3 strategic outcomes this activity should deliver]

[Continue for all {recommended_number} strategic activities...]

**TACTICS TO STRATEGIC ACTIVITIES MAPPING TABLE**
Tactic_ID | Strategic_Activity_ID | Strategic_Activity_Name
[For each tactic, show: Tactic_ID | SA-XXX | Strategic Activity Name]

**STRATEGIC EXECUTION SUMMARY**
*Overall Strategic Approach:* [2-3 sentences summarising the collective strategic approach]
*Strategic Execution Priorities:* [3-5 bullet points of main execution priorities]
*Tactical Coverage Assessment:* [Assessment confirming all tactics are mapped]
*Implementation Readiness:* [Brief assessment of readiness to execute these strategic activities]

Tactical Initiatives to Analyse and Map ({total_initiatives} total):
{initiatives_text}

Strategic Analysis:"""
)

# Strategic Initiative to Capability Mapping prompt template
STRATEGY_CAPABILITY_MAPPING_PROMPT = PromptTemplate(
    input_variables=["strategies_text", "capabilities_text", "additional_context"],
    template="""You are an expert strategy consultant specialising in organisational capabilities and strategic implementation.

Your task: Match each strategic initiative to the MOST APPROPRIATE capability from the provided list.

Strategic Initiatives to Match:
{strategies_text}
Available Capabilities:
{capabilities_text}
Additional Context: {additional_context}

Instructions:
1. For each strategic initiative, analyse and determine which capabilities are required for successful implementation
2. Consider both enablement capabilities (that make the strategy possible) and execution capabilities (that deliver the strategy)
3. A strategy can map to 0, 1, or many capabilities - choose all that are necessary
4. Only return the Strategy ID and Capability ID - no additional text to save tokens
5. Return your response in this exact format:
- For strategies with no required capabilities: STRATEGIC_INITIATIVE_ID -> NONE
- For strategies with one capability: STRATEGIC_INITIATIVE_ID -> CAPABILITY_ID
- For strategies with multiple capabilities: STRATEGIC_INITIATIVE_ID -> CAPABILITY_ID1, CAPABILITY_ID2, CAPABILITY_ID3

Example format:
STRAT001 -> CAP003, CAP007
STRAT002 -> CAP012
STRAT003 -> NONE
STRAT004 -> CAP001, CAP005, CAP009

Mappings:"""
)
