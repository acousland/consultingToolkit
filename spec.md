# Consulting Toolkit Functional Specification

This document describes the expected behaviour of every page and tool in the Consulting Toolkit Streamlit application. The specification covers user interface elements, AI prompts, data processing logic and file manipulation so that the application can be recreated from scratch.

## 1. Home Page

### Purpose
Entry point that introduces the six specialised toolkits and the Admin & Testing Tool.

### UI Summary
- Static markdown description of the toolkit collection.
- Two rows of buttons linking to the toolkits:
  - Row 1: Pain Point Toolkit, Capability Toolkit, Applications Toolkit
  - Row 2: Data, Information, and AI Toolkit; Engagement Planning Toolkit; Strategy and Motivations Toolkit
- Each card contains brief feature text and a **Enter ... Toolkit** button that sets `st.session_state.page` to the relevant page and reruns Streamlit.
- A final section exposes the **Admin & Testing Tool** button.

### Behaviour
Clicking any button updates `st.session_state.page` and reruns the app to display the selected page. No file processing or AI calls occur on the home page.

## 2. Pain Point Toolkit

Overview page that explains the toolkit workflow and links to four analytical tools.

### 2.1 Pain Point Extraction
**Purpose:** Extract distinct pain points from qualitative text.

**UI Elements**
- Breadcrumb: Home › Pain Point Toolkit › Pain Point Extraction
- File uploader accepting CSV or Excel.
- Multiselect to choose one or more text columns to concatenate.
- Text input for additional context sent to the model.
- Numeric input `chunk_size` (default 20) controlling batch size.
- "Generate pain points" button.
- Progress bar and status text while processing.
- Results list and download button exporting `pain_points.xlsx`.

**Processing Flow**
1. Load uploaded spreadsheet using pandas.
2. Concatenate selected text columns per row.
3. Iterate over rows in chunks of `chunk_size`:
   - Create prompt using `pain_point_extraction_prompt`:
```
You are a senior management consultant (MBA) and organisational psychologist (PhD).
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
```
   - Send to OpenAI via `model.invoke([HumanMessage(content=_input)])`.
   - Strip markdown, bullet points and numbering from output and collect lines.
4. Deduplicate pain points case‑insensitively.
5. Persist list in `st.session_state['pain_points']`.
6. Offer Excel download by writing DataFrame with one column "Pain Points" to `BytesIO` using `openpyxl`.

### 2.2 Pain Point Theme & Perspective Mapping
**Purpose:** Categorise pain points into predefined themes and organisational perspectives.

**UI Elements**
- Breadcrumb navigation.
- Upload pain points Excel; select sheet.
- Select pain point ID column and one or more text columns to concatenate.
- Display predefined theme list and perspective list.
- Additional context textarea.
- Batch size number input (default 10).
- "Generate Theme & Perspective Mappings" button.
- Progress bar, preview of AI response for first batch, summary statistics, download button.

**Processing Flow**
1. After column selection, build batches of pain points.
2. For each batch construct prompt `THEME_PERSPECTIVE_MAPPING_PROMPT`:
```
You are an expert management consultant specialising in organisational analysis.
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
```
3. Invoke model and parse lines containing `->`, extracting theme and perspective tokens.
4. Aggregate results into DataFrame with columns `Pain_Point_ID`, `Theme`, `Perspective`, and original text.
5. Display distribution counts; offer Excel download `pain_point_theme_perspective_mappings.xlsx`.

### 2.3 Pain Point Impact Estimation
**Purpose:** Classify each pain point as High, Medium or Low business impact.

**UI Elements**
- Breadcrumb navigation.
- Upload Excel file; choose sheet.
- Select ID column and one or more description columns.
- Optional business context textarea.
- Batch size select (5–25).
- "Estimate Impact" button.
- Progress bar, metrics for impact distribution, results table, Excel download with summary sheet.

**AI Prompt**
Uses `pain_point_impact_estimation_prompt`:
```
You are a senior business analyst specialising in enterprise-level impact assessment.
Evaluate each pain point only in terms of its likely effect on:
1. The organisation’s declared strategic priorities, and
2. Profitability (EBITDA or net margin) over the next 12–24 months.

{context_section}

Classification rules
- High – Materially jeopardises at least one strategic priority or is plausibly expected to reduce profit by ~2 percent or more.
- Medium – Has a clear but limited influence on a strategic priority or could move profit by roughly 0.5 – 2 percent.
- Low – Little or no measurable influence on strategic priorities and unlikely to shift profit by more than ~0.5 percent.

If evidence is ambiguous, err toward the lower category.
Respond with only the impact level (High, Medium, or Low) for each pain point, in the order provided. {context_instruction}

Pain points to assess:
{pain_points}
```

**Processing Flow**
- Split dataset into batches; for each send prompt, parse impact words; default to Medium if missing.
- After processing combine all results, count occurrences and generate Excel with assessment sheet and summary sheet.

### 2.4 Pain Point to Capability Mapping
**Purpose:** Map pain points to capability IDs.

**UI Elements**
- Two upload widgets: pain points and capabilities Excel files with sheet selectors.
- For each file choose ID column and multiple text columns.
- Additional context textarea and batch size number input.
- "Generate AI Mappings" button with progress bar and mapping results table.
- Download button exporting `pain_point_capability_mappings.xlsx` with pain point text and capability text.

**AI Prompt**
`PAIN_POINT_CAPABILITY_MAPPING_PROMPT`:
```
You are an expert management consultant specialising in organisational capabilities.
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
```

**Processing Flow**
- Build text blocks of pain points and capabilities for each batch.
- Invoke model; parse `PAIN_POINT_ID -> CAPABILITY_ID` pairs.
- After all batches, join with capability text to display reference column, then export to Excel.

## 3. Capability Toolkit
Overview page linking to capability description generator.

### 3.1 Capability Description Generation
**Purpose:** Create professional single‑sentence descriptions for capabilities.

**UI Elements**
- Breadcrumb navigation.
- Upload Excel; select sheet.
- Optional ID column selection.
- Multiselect for columns containing capability names/descriptions.
- Textarea for additional context.
- Button "Generate Descriptions from File".
- Results table with capability ID, original text, and generated description.
- Download button exporting `capability_descriptions.xlsx`.

**AI Prompt**
`capability_description_prompt`:
```
You are a management consultant and business architect with deep expertise in organisational capabilities.
Write a single-sentence description for each capability provided.

Style guardrails
– Use Australian English, present tense, active voice, and an Oxford comma.
– Verb guidance – draw verbs from: craft, create, cultivate, develop, engineer, evolve, forge, hone, pilot, pioneer, shape, steer, streamline.
– Use each verb no more than three times across the full output, and never twice in a row.
– One short qualifier is allowed.
– Keep each sentence ≤ 30 words.
– Avoid any stock trio like “identify, analyse, optimise”.

Return the results exactly like this
Capability Name: The ability to …

Capabilities to describe:
{capabilities}
```

**Processing Flow**
- Concatenate selected columns to create capability strings and optionally keep IDs.
- Send combined list to model once; parse lines `Capability: Description` to match original capability list.
- Build DataFrame and export via `xlsxwriter`.

## 4. Applications Toolkit
Overview page with four tools.

### 4.1 Application to Capability Mapping
**Purpose:** Map applications to organisational capabilities for technology landscape analysis.

**UI Elements**
- Upload applications and capabilities spreadsheets with sheet selectors.
- For each file select ID and description columns.
- Additional context textarea and batch size selector.
- "Start Application Mapping" button, progress bar and results table with summary metrics.
- Download button exporting `application_capability_mapping.xlsx` with summary and per‑application counts.

**AI Prompt**
`APPLICATION_CAPABILITY_MAPPING_PROMPT`:
```
You are an enterprise architect mapping software applications to a business-capability model for a residential construction and home-building organisation.
How to reason (think silently):
1. Read each application's description carefully.
2. Scan the full name and the detailed prose for functional verbs, nouns, and domain cues.
3. Compare those cues to both the capability titles and their detailed descriptions.
4. Look for synonyms and near-synonyms …
5. Only count a capability when the application directly delivers or materially supports that business function.

Output rules:
• Return just the Capability IDs, separated by commas, for each application.
• Preserve the exact "Application Name:" label before the IDs.
• If no clear capability match exists, output `NONE`.
• Provide no explanations, qualifiers, or extra text.

{context_section}

Available Capabilities:
{capabilities}

Applications to map:
```

**Processing Flow**
- Build prompt header with capability list and optional context once per batch and append application lines.
- Parse returned lines, splitting capability IDs by comma; add "No mapping found" when response is `NONE` or empty.
- Calculate summary metrics (total mappings, applications processed, capability count, no mappings) and export Excel with summary sheet and application overview.

### 4.2 Logical Application Model Generator
**Purpose:** Create high‑level logical categories and architectural analysis for uploaded applications.

**UI Elements**
- Company context section: optional dossier upload and free‑text description.
- Applications data section: upload CSV/Excel, select sheet, choose application name column and description columns, optional separator preview.
- Generation settings: target number of categories slider and checkbox to include company context.
- Button "Generate Logical Application Model".
- Displays AI response as markdown plus two download buttons (applications summary Excel and full analysis text file).

**AI Prompt**
Assembled dynamically asking the model to create `{num_categories}` logical application categories, assign each application, provide definitions and an architectural analysis section.

**Processing Flow**
- Concatenate application descriptions using selected separator.
- Insert company context if requested.
- Invoke model and render markdown output.
- Export `summary_df` (application and description) to Excel and full analysis to text.

### 4.3 Application Categorisation
**Purpose:** Automatically categorise software portfolio items as Application, Technology, or Platform.

**UI Elements**
- Upload CSV/Excel; select sheet.
- Select ID column and description columns.
- Optional additional context textarea.
- Batch size selector and estimated batches metric.
- "Categorise Applications" button with progress bar.
- Metrics for counts per category, results table and Excel download with summary.

**AI Prompt**
Inline prompt instructs the model to analyse each application/system and return lines `ApplicationID,Category` using definitions for Application, Technology and Platform.

**Processing Flow**
- Combine description columns using ` | `.
- Process in batches; send prompt containing category definitions and list `ID: description`.
- Parse comma‑separated output, validate IDs and categories, and export results to Excel with summary statistics.

### 4.4 Individual Application to Capability Mapping
**Purpose:** Map a single application to capabilities with confidence tiers.

**UI Elements**
- Upload capability framework Excel and select sheet.
- Choose capability ID column and description columns.
- Text inputs for application name and optional ID.
- Text area for application description and optional additional context.
- Button "Map Application to Capabilities".
- Displays application summary, AI analysis, and quick action buttons to analyse another app, open bulk mapping tool, or return to toolkit.

**AI Prompt**
`INDIVIDUAL_APPLICATION_MAPPING_PROMPT`:
```
You are an expert enterprise architect specialising in capability mapping and application portfolio management.
Your task: Analyse the application and identify which capabilities from the provided framework are most relevant.

{context_section}Application to Analyse:
{app_info}

Available Capabilities:
{capabilities_text}

Instructions:
1. Analyse the application's functions, purpose, and characteristics
2. Identify which capabilities from the framework are most relevant
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
```

**Processing Flow**
- Build capability list text, insert optional context and application info into template.
- Invoke model and render markdown response; show warning if no mappings found.

## 5. Engagement Planning Toolkit
Toolkit landing page linking to Engagement Touchpoint Planning.

### 5.1 Engagement Touchpoint Planning
**Purpose:** Generate structured client engagement plan.

**UI Elements**
- Breadcrumb and banner noting the tool is under development.
- Select boxes for engagement type, engagement duration, client size and current phase.
- Text areas for stakeholder roles, engagement objectives and additional context.
- Planning configuration: preferred touchpoint frequency and communication style.
- Button "Generate Touchpoint Plan".
- Displays plan markdown and offers text file and Excel downloads with sample schedule and engagement details.

**AI Prompt**
`ENGAGEMENT_TOUCHPOINT_PROMPT`:
```
You are an experienced engagement manager and client relationship specialist. Your task is to create a comprehensive touchpoint plan for a consulting engagement.

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
1. ENGAGEMENT CALENDAR – timeline of touchpoints
2. STAKEHOLDER MATRIX – communication plan for each stakeholder group
3. TOUCHPOINT TYPES – interaction types
4. COMMUNICATION CADENCE – frequency for each touchpoint type
5. MILESTONE REVIEWS – key decision points
6. ESCALATION PROTOCOLS – issue escalation guidance
7. SUCCESS MEASUREMENTS – how to track progress

Format response with clear sections and Australian English.
```

**Processing Flow**
- Assemble prompt including optional context, send to model and display response.
- Create downloadable text document summarising engagement details and the plan.
- Generate sample structured Excel file with touchpoint schedule and engagement details sheets.

## 6. Strategy and Motivations Toolkit
Toolkit landing page linking to strategy‑capability mapping and tactics‑to‑strategies generator.

### 6.1 Strategy to Capability Mapping
**Purpose:** Map strategic initiatives to organisational capabilities.

**UI Elements**
- Dual file uploaders for strategies and capabilities with sheet selection.
- Select ID and text columns for each dataset.
- Additional context textarea and batch size input.
- "Generate AI Mappings" button with progress bar and results table.
- Download button exporting `strategy_capability_mappings.xlsx`.

**AI Prompt**
`STRATEGY_CAPABILITY_MAPPING_PROMPT`:
```
You are an expert strategy consultant specialising in organisational capabilities and strategic implementation.
Your task: Match each strategic initiative to the MOST APPROPRIATE capability from the provided list.

Strategic Initiatives to Match:
{strategies_text}
Available Capabilities:
{capabilities_text}
Additional Context: {additional_context}

Instructions:
1. For each strategic initiative, analyse and determine which capabilities are required for successful implementation
2. Consider both enablement capabilities and execution capabilities
3. A strategy can map to 0, 1, or many capabilities
4. Only return the Strategy ID and Capability ID
5. Return your response in this exact format:
STRATEGIC_INITIATIVE_ID -> CAPABILITY_ID1, CAPABILITY_ID2
```

**Processing Flow**
- Build text blocks for strategies and capabilities in each batch.
- Invoke model, parse ID pairs separated by commas (skip `NONE`).
- Combine to DataFrame and export to Excel.

### 6.2 Tactics to Strategies Generator
**Purpose:** Group tactical initiatives into strategic activities and perform SWOT analysis.

**UI Elements**
- Upload Excel of initiatives; select sheet.
- Choose initiative ID column and description columns.
- Optional additional context textarea.
- "Identify Strategic Activities" button.
- During processing shows step messages for determining optimal number of strategies, generating activities and conducting SWOT for each.
- Outputs AI analysis markdown, warnings for unmapped tactics, and download button with Excel containing mapping table, strategy summaries and SWOT analyses.

**AI Interaction**
1. Determine optimal number of strategic activities using `STRATEGY_GROUPING_PROMPT` with context and initiatives list.
2. Generate detailed activities with IDs using `STRATEGY_DETAILED_PROMPT`.
3. For each strategic activity, perform SWOT analysis via inline prompt referencing activity description and mapped tactics.

**Processing Flow**
- Combine selected description columns into `combined_description` and build bullet list for prompts.
- Parse AI responses to extract mapping table and strategic activity details.
- Generate SWOT analysis for each strategic activity individually.
- Export Excel with three sheets:
  - **Tactics to Strategies**: tactic ID, strategic activity ID and name.
  - **Strategic Activities**: ID, name, description, success factors, risks, expected outcomes.
  - **SWOT Analyses**: strategy ID, name, SWOT text.

## 7. Data, Information, and AI Toolkit
Landing page linking to four tools: Conceptual Data Model Generator, Data‑Application Mapping, AI Use Case Customiser, and Use Case Ethics Review.

### 7.1 Conceptual Data Model Generator
**Purpose:** Generate subject areas and key data entities from company context.

**UI Elements**
- Breadcrumb navigation.
- Optional company dossier upload (HTML or JSON) with preview.
- Additional context textarea.
- Button "Generate Subject Areas"; result stored in session state and displayed as markdown.
- Button "Generate Data Elements" to produce 3–5 entities per subject area.
- Download button exporting subject areas and entities to Excel.

**AI Prompts**
- Subject area generation prompt instructing the model to infer up to seven business domains from dossier and context.
- For each subject area, entity prompt:
```
Generate Key Data Entities for Subject Area: {subject_area}
You are generating data entities for the "{subject_area}" subject area of a business organisation.
Instructions:
• Generate 3-5 key data entities
• Provide a brief description for each
• Use clear, professional naming

Output format:
- Entity Name: Description
- Entity Name: Description
```

**Processing Flow**
- Read dossier content; combine with additional context to form prompts.
- Parse generated subject areas, then iterate to generate entities (can run in parallel threads).
- Aggregate results and export to Excel via `xlsxwriter`.

### 7.2 Data-Application Mapping
**Purpose:** Map data entities to applications and label each relationship as system of entry or system of record.

**UI Elements**
- Upload data entities and applications files separately with sheet selectors.
- Select ID and optional description columns for each dataset.
- Optional filter to process only applications with specific column values.
- Additional context textarea and batch size input.
- Mapping button with progress indicators.
- Results table and Excel download.

**AI Interaction**
- For each batch build prompt summarising data entities and applications, requesting mappings and relationship type with rationale.

**Processing Flow**
- Concatenate description columns and apply optional application filtering.
- Process in batches using concurrent futures for efficiency.
- Parse model output into DataFrame columns `Data_Entity_ID`, `Application_ID`, `Relationship` and `Rationale`.
- Export results to Excel.

### 7.3 AI Use Case Customiser
**Purpose:** Evaluate and rank AI use cases for a specific company context.

**UI Elements**
- Optional company dossier upload (JSON/XML) and text area for additional description – at least one form of context required.
- Context summarisation step that caches or summarises long descriptions (>1500 characters).
- Upload Excel of AI use cases; select sheet and choose ID and description columns.
- Button to start evaluation.
- Displays ranked table with scores and rationale; provides Excel download.

**AI Interaction**
- For each use case, send prompt combining company summary and use case description asking for a score from 1–10 and brief explanation.
- Uses `ThreadPoolExecutor` to process multiple use cases in parallel.

**Processing Flow**
- Summarise company context if necessary via an additional prompt.
- Iterate through use cases, invoking OpenAI and collecting scores.
- Sort by score descending and export results to Excel.

### 7.4 Use Case Ethics Review
**Purpose:** Perform multi‑perspective ethical analysis of a described use case.

**UI Elements**
- Breadcrumb navigation.
- Large text area for use case description.
- Button "Conduct Ethics Review".
- Displays four analysis sections: Deontological, Utilitarian, Social Contract, Virtue Ethics.

**AI Prompts**
- **Deontological**: evaluates legal compliance, policy violations, categorical imperative tests, and rights/duties.
- **Utilitarian**: identifies stakeholders, scores pros and cons on a 1–10 scale, computes net utilitarian score and sensitivity analysis.
- **Social Contract**: analyses explicit contracts, implicit expectations, stakeholder perspectives and legitimacy.
- **Virtue Ethics**: examines virtues, character implications and organisational values (prompt later in file).

**Processing Flow**
- For each perspective, compose the respective prompt with the use case description and display the returned markdown.

## 8. Admin & Testing Tool
**Purpose:** Configure OpenAI model settings, view pricing and test API connectivity.

**UI Elements**
- Breadcrumb navigation.
- Model configuration:
  - "Refresh Models" button retrieves model list from OpenAI and caches in session state.
  - Selectbox lists models sorted by estimated cost using `format_model_with_cost`.
  - Temperature slider (0–2).
  - "Save Configuration" button writes selection to `model_config.json`.
- Pricing table built from `get_model_pricing()`.
- Test section allowing user to send a prompt to the configured model and display response with cost estimate.

**Behaviour and File Operations**
- Saving model configuration writes JSON to the repository root.
- Model list cached in `st.session_state` to avoid repeated API calls.
- `estimate_call_cost` calculates approximate cost based on token counts.

---

This specification should enable a developer to recreate each component of the Consulting Toolkit including its Streamlit interfaces, OpenAI prompt patterns, and data handling behaviours.
