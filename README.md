# Consulting Toolkit

A comprehensive Streamlit-based application designed for management consultants to systematically analyse organisational challenges, design capabilities, plan engagements, and develop strategic initiatives. This toolkit provides AI-powered analysis capabilities across six specialised areas of consulting practice, including advanced AI use case evaluation and ethical analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/consultingToolkit.git
   cd consultingToolkit
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API:**
   - Create a `.streamlit/secrets.toml` file in the project root
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```
   - The `.streamlit/config.toml` file contains theme and server configuration (included in repository)
   - Your `secrets.toml` file will be automatically excluded from git for security

5. **Run the application:**
   ```bash
   streamlit run main.py
   ```
   Or use the provided script:
   ```bash
  chmod +x run.sh
  ./run.sh
  ```

## 📋 Toolkit Overview

The Consulting Toolkit is organised into six specialised toolkits, each addressing specific aspects of organisational analysis and strategic development:

### 🔍 Pain Point Toolkit
*Identify, categorise, and map organisational challenges*

Perfect for consultants analysing organisational challenges, extracting insights from qualitative data, and connecting problems to solution capabilities.

**Tools included:**
- **Pain Point Extraction:** Extract and categorise pain points from qualitative text
- **Theme & Perspective Mapping:** Organise pain points into strategic themes and perspectives
- **Pain Point Impact Estimation:** Assess business impact and implementation complexity
- **Pain Point to Capability Mapping:** Connect challenges to required organisational capabilities

**Typical workflow:** Extract → Categorise → Assess Impact → Map to Capabilities

### 📝 Capability Toolkit
*Design and refine organisational capabilities*

Essential for capability architects and consultants designing organisational transformation initiatives with structured capability frameworks.

**Tools included:**
- **Capability Designer:** Create comprehensive capability definitions with success criteria
- **Capability Analyser:** Analyse existing capabilities for gaps and improvement opportunities

**Typical workflow:** Design → Analyse → Refine

### 📊 Data, Information, and AI Toolkit
*AI use case evaluation and ethical analysis*

Essential for digital transformation consultants, AI strategy advisors, and ethics officers evaluating AI implementations with comprehensive scoring and ethical frameworks.

**Tools included:**
- **AI Use Case Customiser:** Evaluate AI use cases with company-specific context and 1-100 scoring across feasibility, impact, and strategic alignment
- **Conceptual Data Model Generator:** Create structured data models for business analysis
- **Data to Application Mapping:** Map data sources to applications and capabilities
- **Use Case Ethics Review:** Comprehensive ethical analysis using four philosophical frameworks (Deontological, Utilitarian, Social Contract, and Virtue Ethics)

**Typical workflow:** Evaluate AI Use Cases → Review Ethics → Model Data → Map Applications

### 📱 Applications Toolkit
*Enterprise architecture and application portfolio management*

Critical for enterprise architects and IT consultants managing application portfolios, conducting capability assessments, and implementing architectural governance.

**Tools included:**
- **Application Categorisation:** Classify applications as Application, Technology, or Platform using enterprise architecture principles
- **Individual Application to Capability Mapping:** Map single applications to multiple organisational capabilities with detailed analysis
- **Application to Capability Mapping:** Bulk mapping of applications to capabilities with structured analysis

**Typical workflow:** Categorise → Map to Capabilities → Analyse Architecture

### 📊 Engagement Planning Toolkit
*Plan engagement milestones and touchpoints*

Designed for engagement managers and senior consultants structuring complex organisational transformation projects and ensuring consistent client communication.

**Tools included:**
- **Engagement Touchpoint Planning:** Schedule meetings, deliverables, and communication milestones across workstreams

**Typical workflow:** Define Scope → Plan Touchpoints → Refine Planning

### 🎯 Strategy & Motivations Toolkit
*Strategic analysis and capability alignment*

Essential for strategy consultants developing strategic initiatives, analysing tactical operations, and aligning organisational capabilities with strategic goals.

**Tools included:**
- **Strategy to Capability Mapping:** Map strategic initiatives to required organisational capabilities with multi-capability support
- **Tactics to Strategies Generator:** Transform tactical initiatives into strategic activities with automatic grouping, complete mapping coverage, and individual SWOT analysis

**Typical workflow:** Map Strategies → Generate Strategic Activities → Analyse SWOT

## 🔧 Technical Architecture

### Core Components
- **Streamlit Frontend:** Interactive web interface with professional styling
- **OpenAI Integration:** AI-powered analysis using GPT models via LangChain
- **Excel Export:** Comprehensive analysis outputs in structured Excel format
- **Session Management:** Persistent state management across toolkit navigation

### Dependencies
```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
xlsxwriter>=3.0.0
openai>=1.0.0
langchain>=0.1.0
langchain-openai>=0.0.5
```

### Project Structure
```
consultingToolkit/
├── main.py                    # Application entry point and routing
├── app_config.py             # AI model configuration and prompts
├── requirements.txt          # Python dependencies
├── run.sh                   # Startup script
├── .streamlit/
│   ├── config.toml          # Theme and server configuration (tracked)
│   └── secrets.toml         # OpenAI API configuration (git-ignored)
└── modules/
    ├── home_page.py         # Landing page and toolkit overview
    ├── pain_point_toolkit/  # Pain point analysis tools
    ├── capability_toolkit/  # Capability design tools
    ├── applications_toolkit/# Enterprise architecture tools
    ├── data_information_toolkit/ # AI and data analysis tools
    ├── engagement_planning_toolkit/ # Engagement planning tools
    └── strategy_motivations_toolkit/ # Strategic analysis tools
```

## 🎯 Key Features

### AI-Powered Analysis
- **Advanced Prompting:** Sophisticated prompt engineering for accurate business analysis
- **Australian English:** Consistent professional terminology and grammar
- **Context Awareness:** Deep understanding of consulting frameworks and methodologies
- **Company Context Integration:** AI use case evaluation with company-specific context and cached session management
- **Ethical Analysis:** Multi-framework ethical evaluation using established philosophical principles

### Professional Outputs
- **Excel Generation:** Multi-sheet workbooks with structured analysis using xlsxwriter engine
- **SWOT Analysis:** Individual strategic assessments for each initiative
- **Mapping Tables:** Complete traceability between inputs and outputs
- **Unique Identifiers:** Systematic ID assignment for tracking and reference
- **Ethical Assessments:** Comprehensive multi-framework ethical analysis reports

### Enterprise Architecture Integration
- **Application Classification:** Technology, Application, and Platform categorisation
- **Capability Mapping:** Multi-dimensional capability-to-solution alignment
- **Strategic Alignment:** End-to-end traceability from tactics to strategies

### User Experience
- **Intuitive Navigation:** Clear toolkit organisation with contextual workflows
- **Progress Tracking:** Session state management for complex analysis workflows
- **Professional Interface:** Clean, consultant-friendly design with clear information hierarchy
- **Dark Theme:** macOS-inspired dark theme with professional colour palette
- **Security:** Automatic exclusion of sensitive configuration from version control

## 📚 Usage Examples

### AI Use Case Evaluation Workflow
1. **Upload Company Context:** Provide organisational dossiers (JSON/XML) or text descriptions
2. **Evaluate Use Cases:** AI-powered scoring across feasibility, impact, and strategic alignment (1-100 scale)
3. **Ethics Review:** Comprehensive analysis using Deontological, Utilitarian, Social Contract, and Virtue Ethics frameworks
4. **Export Analysis:** Structured Excel reports with detailed scoring and ethical assessments

### Pain Point Analysis Workflow
1. **Extract Pain Points:** Upload client interviews or documents
2. **Categorise by Theme:** Organise pain points into strategic themes
3. **Assess Impact:** Evaluate business impact and implementation complexity
4. **Map to Capabilities:** Connect challenges to required organisational capabilities

### Strategic Planning Workflow
1. **Map Strategies:** Connect strategic initiatives to required capabilities
2. **Analyse Tactics:** Transform tactical initiatives into strategic activities
3. **Generate SWOT:** Individual strategic assessment for each activity
4. **Export Analysis:** Comprehensive Excel output with mapping tables

### Application Architecture Workflow
1. **Categorise Applications:** Classify as Application, Technology, or Platform
2. **Map to Capabilities:** Connect applications to organisational capabilities
3. **Analyse Architecture:** Review capability coverage and gaps

## 🤝 Contributing

This toolkit is designed for professional consulting use. Contributions should maintain the high standard of business analysis accuracy and professional presentation.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For technical issues or consulting methodology questions, please refer to the application's built-in help text and prompt engineering examples.

---

*Built with ❤️ for the consulting community*
