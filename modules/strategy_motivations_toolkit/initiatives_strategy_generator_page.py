import streamlit as st
import pandas as pd
from io import BytesIO
from langchain_core.messages import HumanMessage
from app_config import model
from prompts import (
    STRATEGY_GROUPING_PROMPT,
    STRATEGY_DETAILED_PROMPT,
)

from navigation import render_breadcrumbs
def initiatives_strategy_generator_page():
    # Breadcrumb navigation as a single line with clickable elements
    render_breadcrumbs([("🏠 Home", "Home"), ("🎯 Strategy and Motivations Toolkit", "Strategy and Motivations Toolkit"), ("📈 Tactics to Strategies Generator", None)])
    
    st.markdown("# 📈 Tactics to Strategies Generator")
    st.markdown("**Identify strategic activities that your tactical initiatives are designed to deliver**")
    
    st.markdown("""
    This tool analyses your portfolio of tactical initiatives and identifies the higher-level strategic activities 
    they are designed to deliver. Upload your initiatives data and receive comprehensive analysis showing how 
    your tactics align with strategic execution approaches.
    """)
    
    st.markdown("---")
    
    # File upload section
    st.markdown("## 📁 Upload Tactical Initiatives Data")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file containing your tactical initiatives",
        type=['xlsx', 'xls', 'xlsm'],
        help="Upload a spreadsheet containing your tactical initiatives, projects, or operational activities"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file
            xls = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Select sheet to load", xls.sheet_names)
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Convert all columns to string to prevent PyArrow errors
            df = df.astype(str)
            df = df.replace('nan', pd.NA)
            
            # Create clean display data
            display_df = df.copy()
            display_df = display_df.fillna('')
            
            st.markdown("### 📋 Data Preview")
            st.dataframe(display_df.head(10))
            
            # Column selection
            st.markdown("### 🔧 Column Selection")
            
            col1, col2 = st.columns(2)
            
            with col1:
                id_column = st.selectbox(
                    "Select Initiative ID column:",
                    df.columns.tolist(),
                    help="Choose the column containing unique identifiers for each initiative"
                )
            
            with col2:
                description_columns = st.multiselect(
                    "Select initiative description columns:",
                    df.columns.tolist(),
                    help="Choose one or more columns that describe the initiatives (will be combined for analysis)"
                )
            
            if id_column and description_columns:
                # Additional context section
                st.markdown("### 📝 Additional Context (Optional)")
                additional_context = st.text_area(
                    "Provide any additional context about your organisation or strategic direction:",
                    placeholder="e.g., We are focused on digital transformation, improving customer experience, operational efficiency, regulatory compliance, market expansion...",
                    help="Optional context to help generate more relevant strategic themes",
                    height=100
                )
                
                # Processing configuration
                st.markdown("### ⚙️ Analysis Configuration")
                
                total_initiatives = len(df)
                st.metric("Total Tactical Initiatives", total_initiatives)
                
                st.info("""
                💡 **Smart Analysis**: The AI will automatically determine the optimal number of strategic activities 
                based on your tactical initiatives portfolio. This ensures natural groupings and strategic coherence.
                """)
                
                # Generate button
                if st.button("🚀 Identify Strategic Activities", use_container_width=True, type="primary"):
                    if not description_columns:
                        st.error("❌ Please select at least one description column.")
                    else:
                        generate_strategic_activities(df, id_column, description_columns, additional_context)
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.error("Please ensure your file is a valid Excel file with proper formatting.")

def generate_strategic_activities(df, id_column, description_columns, additional_context):
    """Generate strategic activities from tactical initiatives using AI with automatic optimal grouping"""
    
    with st.spinner("Analysing tactical initiatives and identifying strategic activities..."):
        
        # Prepare initiatives data
        df_clean = df.copy()
        df_clean['combined_description'] = df_clean[description_columns].fillna('').agg(' | '.join, axis=1)
        
        # Build initiatives list for AI
        initiatives_list = []
        for _, row in df_clean.iterrows():
            initiative_id = row[id_column]
            description = row['combined_description']
            initiatives_list.append(f"- {initiative_id}: {description}")
        
        initiatives_text = "\n".join(initiatives_list)
        total_initiatives = len(df_clean)
        
        # Step 1: Determine optimal number of strategic activities
        st.write("🔍 **Step 1:** Determining optimal strategic groupings...")
        
        context_section = f"Organisational Context: {additional_context}\n\n" if additional_context.strip() else ""

        grouping_prompt = STRATEGY_GROUPING_PROMPT.format(
            context_section=context_section,
            total_initiatives=total_initiatives,
            initiatives_text=initiatives_text,
        )

        try:
            # Call AI for grouping analysis
            message = HumanMessage(content=grouping_prompt)
            response = model.invoke([message])
            grouping_response = response.content.strip()
            
            # Parse the recommended number
            recommended_number = 5  # default fallback
            for line in grouping_response.split('\n'):
                if line.startswith("**RECOMMENDED NUMBER OF STRATEGIC ACTIVITIES:**"):
                    try:
                        recommended_number = int(line.split(":")[1].strip())
                        break
                    except:
                        pass
            
            st.write(f"✅ **Recommended Strategic Activities:** {recommended_number}")
            with st.expander("View Grouping Analysis", expanded=False):
                st.markdown(grouping_response)
            
            # Step 2: Generate detailed strategic activities with IDs
            st.write("🎯 **Step 2:** Generating detailed strategic activities with mapping...")
            
            detailed_prompt = STRATEGY_DETAILED_PROMPT.format(
                recommended_number=recommended_number,
                context_section=context_section,
                total_initiatives=total_initiatives,
                initiatives_text=initiatives_text,
            )

            # Call AI for detailed analysis
            message = HumanMessage(content=detailed_prompt)
            response = model.invoke([message])
            ai_response = response.content.strip()
            
            # Display results
            st.markdown("## 🎯 Strategic Activities Analysis")
            
            # Initiative summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Tactics Analysed", len(df_clean))
            
            with col2:
                st.metric("Strategic Activities Generated", recommended_number)
            
            with col3:
                # Count actual strategic activities in response
                activity_count = ai_response.count("**STRATEGIC ACTIVITY SA-")
                st.metric("Activities Identified", activity_count)
            
            st.markdown("---")
            
            # Parse AI response for Excel creation
            tactics_to_strategies_mapping = []
            strategies_summary = []
            
            # Parse the AI response to extract structured data
            lines = ai_response.split('\n')
            current_strategy_id = None
            current_strategy_name = None
            current_description = ""
            current_tactics = ""
            current_success_factors = ""
            current_risks = ""
            current_outcomes = ""
            
            # Extract mapping table data
            in_mapping_table = False
            
            for line in lines:
                line = line.strip()
                
                # Check if we're in the mapping table section
                if line.startswith("**TACTICS TO STRATEGIC ACTIVITIES MAPPING TABLE**"):
                    in_mapping_table = True
                    continue
                elif line.startswith("**STRATEGIC EXECUTION SUMMARY**"):
                    in_mapping_table = False
                    continue
                
                # Parse mapping table data
                if in_mapping_table and " | " in line and not line.startswith("Tactic_ID"):
                    parts = [p.strip() for p in line.split(" | ")]
                    if len(parts) >= 3:
                        tactics_to_strategies_mapping.append({
                            'Tactic_ID': parts[0],
                            'Strategic_Activity_ID': parts[1],
                            'Strategic_Activity_Name': parts[2]
                        })
                
                # Parse strategic activities
                if line.startswith("**STRATEGIC ACTIVITY SA-"):
                    # Save previous strategy if exists
                    if current_strategy_id:
                        strategies_summary.append({
                            'Strategic_Activity_ID': current_strategy_id,
                            'Strategic_Activity_Name': current_strategy_name,
                            'Strategic_Description': current_description,
                            'Success_Factors': current_success_factors,
                            'Risk_Considerations': current_risks,
                            'Expected_Outcomes': current_outcomes
                        })
                    
                    # Extract new strategy ID and name
                    strategy_part = line.replace("**STRATEGIC ACTIVITY ", "").replace("**", "")
                    if ":" in strategy_part:
                        current_strategy_id = strategy_part.split(":")[0].strip()
                        current_strategy_name = strategy_part.split(":", 1)[1].strip()
                    else:
                        current_strategy_id = ""
                        current_strategy_name = ""
                    
                    current_description = ""
                    current_tactics = ""
                    current_success_factors = ""
                    current_risks = ""
                    current_outcomes = ""
                
                elif line.startswith("*Strategic Description:*"):
                    current_description = line.replace("*Strategic Description:*", "").strip()
                elif line.startswith("*Mapped Tactics:*"):
                    current_tactics = line.replace("*Mapped Tactics:*", "").strip()
                elif line.startswith("*Success Factors:*"):
                    current_success_factors = line.replace("*Success Factors:*", "").strip()
                elif line.startswith("*Risk Considerations:*"):
                    current_risks = line.replace("*Risk Considerations:*", "").strip()
                elif line.startswith("*Expected Outcomes:*"):
                    current_outcomes = line.replace("*Expected Outcomes:*", "").strip()
            
            # Don't forget the last strategy
            if current_strategy_id:
                strategies_summary.append({
                    'Strategic_Activity_ID': current_strategy_id,
                    'Strategic_Activity_Name': current_strategy_name,
                    'Strategic_Description': current_description,
                    'Success_Factors': current_success_factors,
                    'Risk_Considerations': current_risks,
                    'Expected_Outcomes': current_outcomes
                })
            
            # Validate mapping coverage
            mapped_tactics = set([mapping['Tactic_ID'] for mapping in tactics_to_strategies_mapping])
            all_tactics = set([str(row[id_column]) for _, row in df_clean.iterrows()])
            unmapped_tactics = all_tactics - mapped_tactics
            
            if unmapped_tactics:
                st.warning(f"⚠️ Note: {len(unmapped_tactics)} tactics may not be clearly mapped. Check the detailed analysis.")
            else:
                st.success(f"✅ All {len(all_tactics)} tactics successfully mapped to strategic activities!")
            
            # Additional context display
            if additional_context.strip():
                st.markdown("### 📝 Analysis Context Used")
                st.info(f"Organisational context: {additional_context}")
            
            # Step 3: Generate strategic assessment for each strategy
            st.write("📋 **Step 3:** Assessing individual strategic activities with SWOT analysis...")
            
            # Generate SWOT analysis for each strategic activity
            strategy_assessments = []
            
            for strategy in strategies_summary:
                strategy_id = strategy.get('Strategic_Activity_ID', '')
                strategy_name = strategy.get('Strategic_Activity_Name', '')
                strategy_description = strategy.get('Strategic_Description', '')
                
                # Find tactics mapped to this strategy
                strategy_tactics = [mapping['Tactic_ID'] for mapping in tactics_to_strategies_mapping 
                                 if mapping.get('Strategic_Activity_ID') == strategy_id]
                
                swot_prompt = f"""You are a senior strategy consultant conducting a SWOT analysis for a specific strategic activity.

Strategic Activity: {strategy_id}: {strategy_name}

Description: {strategy_description}

Supporting Tactics: {', '.join(strategy_tactics) if strategy_tactics else 'None identified'}

{context_section}Instructions:
Conduct a comprehensive SWOT analysis for this specific strategic activity. Focus on how this particular strategic activity performs within the broader portfolio.

Return your analysis in this exact format:

**STRENGTHS**
• [Strength 1: What this strategic activity does exceptionally well]
• [Strength 2: Key advantages or capabilities this activity leverages]
• [Strength 3: Unique value propositions or competitive advantages]
• [Strength 4: Resource strengths or tactical support quality]

**WEAKNESSES**
• [Weakness 1: Internal limitations or gaps in this strategic activity]
• [Weakness 2: Resource constraints or capability gaps]
• [Weakness 3: Implementation challenges or execution risks]
• [Weakness 4: Areas where this activity underperforms]

**OPPORTUNITIES**
• [Opportunity 1: External opportunities this strategic activity can capitalize on]
• [Opportunity 2: Market trends or conditions that favor this activity]
• [Opportunity 3: Potential synergies with other strategic activities]
• [Opportunity 4: Growth or expansion possibilities]

**THREATS**
• [Threat 1: External risks or challenges to this strategic activity]
• [Threat 2: Market conditions or competitive threats]
• [Threat 3: Dependencies or vulnerabilities]
• [Threat 4: Potential conflicts with other strategic priorities]

SWOT Analysis:"""

                # Call AI for SWOT analysis
                message = HumanMessage(content=swot_prompt)
                response = model.invoke([message])
                swot_response = response.content.strip()
                
                strategy_assessments.append({
                    'strategy_id': strategy_id,
                    'strategy_name': strategy_name,
                    'strategy_description': strategy_description,
                    'supporting_tactics': strategy_tactics,
                    'swot_analysis': swot_response
                })
            
            st.write("✅ **Strategic Assessment Complete**")
            
            # Create comprehensive Excel download
            st.markdown("### 📥 Download Strategic Analysis")
            
            # Create Excel file with multiple sheets
            excel_buffer = BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                # Sheet 1: Tactics to Strategies Mapping (Primary Output)
                # Create complete mapping ensuring all tactics are included
                complete_mapping = []
                
                # First, try to use AI-generated mapping
                mapped_tactic_ids = set()
                if tactics_to_strategies_mapping:
                    for mapping in tactics_to_strategies_mapping:
                        tactic_id = str(mapping.get('Tactic_ID', '')).strip()
                        # Clean tactic ID
                        if tactic_id.startswith('- '):
                            tactic_id = tactic_id[2:]
                        complete_mapping.append({
                            'Tactic_ID': tactic_id,
                            'Strategic_Activity_ID': mapping.get('Strategic_Activity_ID', ''),
                            'Strategic_Activity_Name': mapping.get('Strategic_Activity_Name', '')
                        })
                        mapped_tactic_ids.add(tactic_id)
                
                # Ensure ALL tactics are mapped - add any missing ones
                all_tactic_ids = set([str(row[id_column]) for _, row in df_clean.iterrows()])
                unmapped_tactics = all_tactic_ids - mapped_tactic_ids
                
                # Map any unmapped tactics to the first strategy as fallback
                default_strategy = strategies_summary[0] if strategies_summary else {
                    'Strategic_Activity_ID': 'SA-001', 
                    'Strategic_Activity_Name': 'Strategic Activity 1'
                }
                
                for unmapped_tactic in unmapped_tactics:
                    complete_mapping.append({
                        'Tactic_ID': unmapped_tactic,
                        'Strategic_Activity_ID': default_strategy.get('Strategic_Activity_ID', 'SA-001'),
                        'Strategic_Activity_Name': default_strategy.get('Strategic_Activity_Name', 'Strategic Activity 1')
                    })
                
                mapping_df = pd.DataFrame(complete_mapping)
                mapping_df.to_excel(writer, sheet_name='Tactics_to_Strategies_Map', index=False)
                
                # Sheet 2: Strategic Activities Summary
                if strategies_summary:
                    strategies_df = pd.DataFrame(strategies_summary)
                    strategies_df.to_excel(writer, sheet_name='Strategic_Activities_Summary', index=False)
                
                # Individual Strategy Sheets (Sheet 3+): One sheet per strategy with SWOT
                for assessment in strategy_assessments:
                    strategy_id = assessment['strategy_id']
                    strategy_name = assessment['strategy_name']
                    strategy_description = assessment['strategy_description']
                    supporting_tactics = assessment['supporting_tactics']
                    swot_analysis = assessment['swot_analysis']
                    
                    # Create sheet name (Excel has 31 character limit)
                    sheet_name = f"{strategy_id}_Analysis"[:31]
                    
                    # Parse SWOT analysis into structured data
                    swot_lines = swot_analysis.split('\n')
                    current_section = ""
                    swot_data = []
                    
                    # Add header information
                    swot_data.append({'Category': 'STRATEGY INFO', 'Item': 'Strategy ID', 'Description': strategy_id})
                    swot_data.append({'Category': 'STRATEGY INFO', 'Item': 'Strategy Name', 'Description': strategy_name})
                    swot_data.append({'Category': 'STRATEGY INFO', 'Item': 'Description', 'Description': strategy_description})
                    swot_data.append({'Category': 'STRATEGY INFO', 'Item': 'Supporting Tactics', 'Description': ', '.join(supporting_tactics) if supporting_tactics else 'None identified'})
                    swot_data.append({'Category': '', 'Item': '', 'Description': ''})  # Blank row
                    
                    for line in swot_lines:
                        line = line.strip()
                        if line.startswith("**") and line.endswith("**"):
                            current_section = line.replace("**", "")
                        elif line.startswith("•"):
                            item_text = line[1:].strip()
                            # Split on first colon if present
                            if ":" in item_text:
                                item_parts = item_text.split(":", 1)
                                item_name = item_parts[0].strip()
                                item_desc = item_parts[1].strip()
                            else:
                                item_name = ""
                                item_desc = item_text
                            
                            swot_data.append({
                                'Category': current_section,
                                'Item': item_name,
                                'Description': item_desc
                            })
                    
                    if swot_data:
                        swot_df = pd.DataFrame(swot_data)
                        swot_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📊 Download Strategic Analysis with SWOT (Excel)",
                data=excel_buffer.getvalue(),
                file_name="tactics_to_strategies_analysis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### 🔄 Quick Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Analyse Different Data", use_container_width=True):
                    st.rerun()
            
            with col2:
                if st.button("🎯 Strategy to Capability Mapping", use_container_width=True):
                    st.session_state.page = "Strategy to Capability Mapping"
                    st.rerun()
            
            with col3:
                if st.button("🏠 Strategy Toolkit", use_container_width=True):
                    st.session_state.page = "Strategy and Motivations Toolkit"
                    st.rerun()
            
            st.success("✅ Strategic activities analysis complete with ID mapping!")
            
        except Exception as e:
            st.error(f"❌ Error generating strategic analysis: {str(e)}")
            st.error("Please check your data and try again.")
