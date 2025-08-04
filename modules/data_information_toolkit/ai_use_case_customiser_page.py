import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from navigation import render_breadcrumbs
from app_config import model
from langchain_core.messages import HumanMessage


def ai_use_case_customiser_page():
    """AI Use Case Customiser tool for evaluating and ranking AI use cases based on company context."""
    
    # Breadcrumbs
    render_breadcrumbs([
        ("Home", "Home"), 
        ("Data, Information, and AI Toolkit", "Data, Information, and AI Toolkit"),
        ("AI Use Case Customiser", None)
    ])
    
    st.markdown("# 🤖 AI Use Case Customiser")
    st.markdown("Evaluate and rank AI use cases based on your specific company context and business needs.")
    
    st.markdown("""
    **This tool helps you:**
    - Upload company information to provide context for AI evaluation
    - Process reference AI use cases from Excel files
    - Score each use case (1-10) based on relevance to your company
    - Get ranked recommendations for AI implementation priorities
    """)
    
    st.markdown("---")
    
    # Company Context Section
    st.markdown("## 📋 Step 1: Company Context")
    st.markdown("Provide information about your company to customize the AI use case evaluation.")
    
    company_description = ""
    
    # Optional dossier upload
    st.markdown("### Optional: Upload Company Dossier")
    dossier_file = st.file_uploader(
        "Upload company dossier (JSON or XML):",
        type=['json', 'xml'],
        help="Upload a JSON or XML file containing detailed company information"
    )
    
    if dossier_file is not None:
        try:
            if dossier_file.name.endswith('.json'):
                dossier_content = json.load(dossier_file)
                # Convert JSON to readable text
                company_description = json.dumps(dossier_content, indent=2)
                st.success("✅ JSON dossier loaded successfully")
                
                # Show preview
                with st.expander("📖 Preview Dossier Content"):
                    st.json(dossier_content)
                    
            elif dossier_file.name.endswith('.xml'):
                tree = ET.parse(dossier_file)
                root = tree.getroot()
                # Convert XML to readable text
                company_description = ET.tostring(root, encoding='unicode')
                st.success("✅ XML dossier loaded successfully")
                
                # Show preview
                with st.expander("📖 Preview Dossier Content"):
                    st.code(company_description, language='xml')
                    
        except Exception as e:
            st.error(f"Error reading dossier file: {e}")
    
    # Additional company information
    st.markdown("### Company Description")
    additional_info = st.text_area(
        "Describe your company, industry, business model, and key characteristics:",
        placeholder="Enter company details here, or provide additional context if you've uploaded a dossier...",
        height=150,
        help="This information will be used to evaluate how relevant each AI use case is to your specific company"
    )
    
    # Combine dossier and additional info
    full_company_context = ""
    if company_description:
        full_company_context += f"Company Dossier:\n{company_description}\n\n"
    if additional_info:
        full_company_context += f"Additional Information:\n{additional_info}"
    
    # Validation: Require either dossier or description
    has_company_context = bool(company_description.strip() or additional_info.strip())
    
    if not has_company_context:
        st.error("⚠️ **Company context required**: Please either upload a company dossier or provide a company description to proceed.")
    
    # Company Context Summarization (if context is provided)
    company_summary = ""
    if has_company_context and full_company_context.strip():
        # Create a unique key for this company context to cache the summary
        import hashlib
        context_hash = hashlib.md5(full_company_context.encode()).hexdigest()
        summary_key = f"company_summary_{context_hash}"
        
        # Check if we already have a summary for this context in session state
        if summary_key in st.session_state:
            company_summary = st.session_state[summary_key]
            
            with st.expander("📋 Company Context Processing", expanded=False):
                st.success(f"✅ Using cached company summary ({len(company_summary):,} characters)")
                with st.expander("📖 View Company Summary"):
                    st.markdown(company_summary)
        else:
            with st.expander("📋 Company Context Processing", expanded=False):
                st.markdown("**Processing company information for AI evaluation...**")
                
                # Check if context is long and needs summarization
                context_length = len(full_company_context)
                st.info(f"Company context length: {context_length:,} characters")
                
                if context_length > 1500:  # Reduced threshold for more aggressive summarization
                    st.markdown("⚡ **Summarizing company context** to optimize AI evaluation performance...")
                    
                    try:
                        with st.spinner("Creating company summary..."):
                            summary_prompt = f"""You are a business analyst. Create a CONCISE summary of this company information for AI use case evaluation.

Company Information:
{full_company_context}

Create a brief summary (MAX 300 words) covering:
1. Industry & Business Model
2. Key Operations & Size
3. Strategic Priorities
4. Technology Maturity
5. Main Challenges

Keep it factual and focused - only the most critical information for AI use case assessment.

Summary:"""

                            summary_response = model.invoke([HumanMessage(content=summary_prompt)])
                            company_summary = summary_response.content.strip()
                            
                            # Cache the summary in session state
                            st.session_state[summary_key] = company_summary
                            
                            st.success(f"✅ Company context summarized ({len(company_summary):,} characters)")
                            
                            # Show preview of summary
                            with st.expander("📖 View Company Summary"):
                                st.markdown(company_summary)
                                
                    except Exception as e:
                        st.warning(f"⚠️ Could not summarize company context: {e}")
                        st.markdown("Using full company context (may affect performance)")
                        company_summary = full_company_context
                        st.session_state[summary_key] = company_summary
                else:
                    st.success("✅ Company context length is optimal - no summarization needed")
                    company_summary = full_company_context
                    st.session_state[summary_key] = company_summary
    
    st.markdown("---")
    
    # AI Use Cases Upload Section
    st.markdown("## 📊 Step 2: Upload AI Use Cases")
    st.markdown("Upload an Excel file containing reference AI use cases to evaluate.")
    
    use_cases_df = None
    
    use_cases_file = st.file_uploader(
        "Upload AI use cases file:",
        type=['xlsx', 'xls', 'xlsm'],
        help="Upload an Excel file containing AI use cases with descriptions"
    )
    
    if use_cases_file is not None:
        try:
            # Read Excel file and get sheet names
            excel_file = pd.ExcelFile(use_cases_file)
            sheet_names = excel_file.sheet_names
            
            st.markdown("### Select Sheet")
            selected_sheet = st.selectbox(
                "Choose the sheet containing use cases:",
                sheet_names,
                help="Select the worksheet that contains your AI use cases"
            )
            
            # Read the selected sheet
            use_cases_df = pd.read_excel(use_cases_file, sheet_name=selected_sheet)
            
            # Show basic info about the data
            st.info(f"📊 Data shape: {use_cases_df.shape[0]} rows × {use_cases_df.shape[1]} columns")
            
            # Column selection
            st.markdown("#### Select Columns")
            col_id_col, col_desc_col = st.columns(2)
            
            with col_id_col:
                id_column = st.selectbox(
                    "Use Case ID Column:",
                    use_cases_df.columns.tolist(),
                    help="Select the column containing unique identifiers for each use case"
                )
            
            with col_desc_col:
                desc_columns = st.multiselect(
                    "Description Columns:",
                    use_cases_df.columns.tolist(),
                    help="Select one or more columns containing use case descriptions, titles, or details. Multiple columns will be concatenated together."
                )
            
            # Show concatenation preview if multiple description columns selected
            if len(desc_columns) > 1:
                st.markdown("#### Description Concatenation Preview")
                concat_separator = st.selectbox(
                    "Separator for concatenating descriptions:",
                    [" | ", " - ", " ", "\\n", "; "],
                    index=0,
                    help="Choose how to join multiple description columns"
                )
                
                # Show preview of concatenated descriptions
                if id_column and desc_columns:
                    preview_sample = use_cases_df.head(3)
                    concatenated_preview = []
                    
                    for _, row in preview_sample.iterrows():
                        use_case_id = row[id_column]
                        concatenated_desc = concat_separator.join([
                            str(row[col]) for col in desc_columns 
                            if pd.notna(row[col]) and str(row[col]).strip()
                        ])
                        concatenated_preview.append({
                            'Use Case ID': use_case_id,
                            'Concatenated Description': concatenated_desc
                        })
                    
                    st.markdown("**Sample of concatenated descriptions:**")
                    st.dataframe(pd.DataFrame(concatenated_preview), use_container_width=True)
            
            # Data preview
            if id_column and desc_columns:
                st.markdown("#### Data Preview")
                preview_df = use_cases_df[[id_column] + desc_columns].head(10)
                st.dataframe(preview_df, use_container_width=True)
                
                # Show summary statistics
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    missing_ids = use_cases_df[id_column].isna().sum()
                    st.metric("Missing Use Case IDs", missing_ids)
                
                with col_stats2:
                    missing_descriptions = sum([use_cases_df[col].isna().sum() for col in desc_columns])
                    st.metric("Total Missing Description Values", missing_descriptions)
        
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    st.markdown("---")
    
    # Evaluation Section
    if use_cases_df is not None and 'id_column' in locals() and 'desc_columns' in locals() and has_company_context and company_summary:
        st.markdown("## 🚀 Step 3: Evaluate Use Cases")
        
        col_settings1, col_settings2 = st.columns(2)
        
        with col_settings1:
            st.markdown("**Scoring Scale**: 1-100 points")
            st.markdown("Each use case will receive a detailed score and reasoning")
        
        with col_settings2:
            max_workers = st.slider(
                "Processing threads:",
                min_value=1,
                max_value=10,
                value=1,  # Default to single thread to avoid context warnings
                help="Number of parallel threads for processing. Use 1 to avoid threading warnings, or higher values for faster processing with multiple API calls."
            )
        
        if st.button("🤖 Evaluate AI Use Cases", type="primary"):
            with st.spinner("Evaluating AI use cases based on your company context..."):
                try:
                    # Prepare use cases data with concatenated descriptions
                    use_cases_data = []
                    
                    # Determine separator if multiple description columns
                    separator = " | "  # Default
                    if len(desc_columns) > 1 and 'concat_separator' in locals():
                        separator = concat_separator
                    
                    for _, row in use_cases_df.iterrows():
                        use_case_id = row[id_column]
                        
                        # Concatenate description columns
                        if len(desc_columns) == 1:
                            use_case_desc = str(row[desc_columns[0]]) if pd.notna(row[desc_columns[0]]) else ""
                        else:
                            desc_parts = [
                                str(row[col]) for col in desc_columns 
                                if pd.notna(row[col]) and str(row[col]).strip()
                            ]
                            use_case_desc = separator.join(desc_parts)
                        
                        if use_case_desc.strip():  # Only include if we have a description
                            use_cases_data.append({
                                'id': use_case_id,
                                'description': use_case_desc
                            })
                    
                    # Function to evaluate a single use case
                    def evaluate_use_case(use_case):
                        prompt = f"""You are an AI strategy consultant with deep expertise in AI implementation and business value assessment. You are evaluating AI use cases for a specific company to determine their potential benefit and strategic fit.

Company Context:
{company_summary}

Use Case to Evaluate:
ID: {use_case['id']}
Description: {use_case['description']}

IMPORTANT SCORING REQUIREMENTS:
- You must provide a score between 1-100 (no use case can receive exactly 0 or 100)
- Consider this company's specific context, industry, size, maturity, and strategic objectives
- Provide nuanced scoring that reflects real-world implementation considerations

Evaluation Criteria (consider all factors):
1. Strategic Alignment: How well does this use case align with the company's business strategy and objectives?
2. Industry Relevance: How applicable is this use case to the company's specific industry and market?
3. Technical Feasibility: Given the company's likely technical maturity, how feasible is implementation?
4. Business Impact Potential: What is the potential ROI, efficiency gains, or competitive advantage?
5. Implementation Complexity: How complex would this be to implement given the company context?
6. Resource Requirements: How well do the required resources align with the company's likely capabilities?
7. Risk vs Reward: What is the risk-adjusted potential value for this specific company?

Scoring Guidelines:
- 1-20: Very Low Benefit (significant misalignment, major obstacles, minimal value potential)
- 21-40: Low Benefit (poor fit, substantial challenges, limited value)
- 41-60: Moderate Benefit (reasonable fit, manageable challenges, decent value potential)
- 61-80: High Benefit (good strategic fit, achievable implementation, strong value potential)
- 81-99: Very High Benefit (excellent alignment, high feasibility, exceptional value potential)

Format your response exactly as follows:
Score: [number between 1-99]
Reasoning: [Provide a comprehensive explanation of your scoring decision, addressing the key evaluation criteria and how they apply to this specific company context. Explain both the potential benefits and any limitations or challenges that influenced your score.]"""

                        try:
                            response = model.invoke([HumanMessage(content=prompt)])
                            response_text = response.content.strip()
                            
                            # Extract score and reasoning with improved parsing
                            import re
                            score = None
                            reasoning = ""
                            
                            # Try multiple parsing strategies
                            
                            # Strategy 1: Look for "Score: XX" pattern
                            score_pattern = r'Score:\s*(\d+)'
                            score_match = re.search(score_pattern, response_text, re.IGNORECASE)
                            if score_match:
                                score = int(score_match.group(1))
                                # Ensure score is within valid range (1-99)
                                if score < 1:
                                    score = 1
                                elif score > 99:
                                    score = 99
                            
                            # Strategy 2: Look for reasoning section
                            reasoning_pattern = r'Reasoning:\s*(.*?)(?:\n\n|\Z)'
                            reasoning_match = re.search(reasoning_pattern, response_text, re.IGNORECASE | re.DOTALL)
                            if reasoning_match:
                                reasoning = reasoning_match.group(1).strip()
                            
                            # Fallback: If no structured format found, try to extract any number and use full text
                            if score is None:
                                number_matches = re.findall(r'\b(\d{1,2})\b', response_text)
                                for num_str in number_matches:
                                    num = int(num_str)
                                    if 1 <= num <= 99:
                                        score = num
                                        break
                            
                            if not reasoning and score is None:
                                # If we can't parse anything, use the full response as reasoning
                                reasoning = response_text[:500] + "..." if len(response_text) > 500 else response_text
                            
                            return {
                                'use_case_id': use_case['id'],
                                'description': use_case['description'],
                                'score': score if score is not None else 50,  # Default to 50 if parsing fails
                                'explanation': reasoning.strip() or "No reasoning provided",
                                'raw_response': response_text  # Keep for debugging
                            }
                        except Exception as e:
                            return {
                                'use_case_id': use_case['id'],
                                'description': use_case['description'],
                                'score': 50,  # Default score on error
                                'explanation': f"Error during evaluation: {str(e)}"
                            }
                    
                    # Process use cases with progress tracking
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    if max_workers == 1:
                        # Sequential processing to avoid threading warnings
                        for i, use_case in enumerate(use_cases_data):
                            result = evaluate_use_case(use_case)
                            results.append(result)
                            
                            # Update progress
                            progress = (i + 1) / len(use_cases_data)
                            progress_bar.progress(progress)
                            status_text.text(f"Processed {i + 1}/{len(use_cases_data)} use cases...")
                    else:
                        # Parallel processing
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            # Submit all tasks
                            future_to_use_case = {executor.submit(evaluate_use_case, uc): uc for uc in use_cases_data}
                            
                            # Process completed tasks
                            completed = 0
                            total = len(use_cases_data)
                            
                            for future in as_completed(future_to_use_case):
                                result = future.result()
                                results.append(result)
                                completed += 1
                                
                                # Update progress
                                progress_bar.progress(completed / total)
                                status_text.text(f"Processed {completed}/{total} use cases...")
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Sort results by score (highest to lowest)
                    results.sort(key=lambda x: x['score'], reverse=True)
                    
                    # Display results
                    st.markdown("## 📊 AI Use Case Evaluation Results")
                    st.markdown(f"**Evaluated {len(results)} use cases based on your company context**")
                    
                    # Summary statistics
                    scores = [r['score'] for r in results]
                    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                    
                    with col_stats1:
                        st.metric("Average Score", f"{sum(scores)/len(scores):.1f}")
                    with col_stats2:
                        st.metric("Highest Score", max(scores))
                    with col_stats3:
                        st.metric("Lowest Score", min(scores))
                    with col_stats4:
                        high_potential = len([s for s in scores if s >= 70])
                        st.metric("High Potential (70+)", high_potential)
                    
                    # Detailed results table
                    st.markdown("### Ranked Results")
                    
                    # Create results dataframe
                    results_df = pd.DataFrame([
                        {
                            'Rank': i + 1,
                            'Use Case ID': r['use_case_id'],
                            'Score': r['score'],
                            'Description': r['description'][:100] + "..." if len(r['description']) > 100 else r['description'],
                            'Explanation': r['explanation']
                        }
                        for i, r in enumerate(results)
                    ])
                    
                    # Display with color coding
                    def score_color(score):
                        if score >= 70:
                            return 'background-color: #d4edda'  # Green (High potential)
                        elif score >= 40:
                            return 'background-color: #fff3cd'  # Yellow (Moderate potential)
                        else:
                            return 'background-color: #f8d7da'  # Red (Low potential)
                    
                    # Apply styling
                    styled_df = results_df.style.map(
                        score_color, 
                        subset=['Score']
                    )
                    
                    st.dataframe(styled_df, use_container_width=True)
                    
                    # Detailed view for top recommendations
                    st.markdown("### Top 5 Recommendations")
                    
                    for i, result in enumerate(results[:5]):
                        with st.expander(f"#{i+1}: {result['use_case_id']} (Score: {result['score']})"):
                            st.markdown(f"**Description:** {result['description']}")
                            st.markdown(f"**Evaluation:** {result['explanation']}")
                    
                    # Export functionality
                    st.markdown("---")
                    st.markdown("## 📥 Export Results")
                    
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        # Export detailed results
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            results_df.to_excel(writer, sheet_name='AI Use Case Evaluation', index=False)
                        
                        st.download_button(
                            label="📊 Download Results (Excel)",
                            data=excel_buffer.getvalue(),
                            file_name="ai_use_case_evaluation.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    with col_export2:
                        # Export summary report
                        summary_text = f"""AI Use Case Evaluation Report
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

Company Context:
{company_summary}

Summary Statistics:
- Total Use Cases Evaluated: {len(results)}
- Average Score: {sum(scores)/len(scores):.1f}
- High Potential Use Cases (Score 70+): {high_potential}

Top 5 Recommendations:
{chr(10).join([f"{i+1}. {r['use_case_id']} (Score: {r['score']}) - {r['explanation']}" for i, r in enumerate(results[:5])])}

Complete Rankings:
{chr(10).join([f"{i+1}. {r['use_case_id']}: {r['score']}/10" for i, r in enumerate(results)])}
"""
                        st.download_button(
                            label="📄 Download Summary Report (Text)",
                            data=summary_text,
                            file_name="ai_use_case_summary_report.txt",
                            mime="text/plain"
                        )
                
                except Exception as e:
                    st.error(f"Error evaluating use cases: {e}")
                    st.markdown("**Troubleshooting suggestions:**")
                    st.markdown("- Check your OpenAI API configuration in the Admin Tool")
                    st.markdown("- Ensure use cases data is properly formatted")
                    st.markdown("- Try with fewer use cases if the request is too large")
                    st.markdown("- Reduce the number of processing threads")
    
    elif use_cases_df is not None and ('id_column' not in locals() or 'desc_columns' not in locals()):
        st.info("👆 Please select the ID column and description columns for your use cases.")
    elif not has_company_context:
        st.error("⚠️ Please provide company context (either through dossier upload or description).")
    else:
        st.info("👆 Please upload AI use cases data and provide company context to begin evaluation.")
