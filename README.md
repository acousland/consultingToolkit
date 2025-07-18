# Consulting Toolkit

A comprehensive Streamlit-based application designed for management consultants to systematically analyse organisational challenges, design capabilities, plan engagements, and develop strategic initiatives. This toolkit provides AI-powered analysis capabilities across five specialised areas of consulting practice.

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

The Consulting Toolkit is organised into five specialised toolkits, each addressing specific aspects of organisational analysis and strategic development:

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

### 📱 Applications Toolkit
*Enterprise architecture and application portfolio management*

Critical for enterprise architects and IT consultants managing application portfolios, conducting capability assessments, and implementing architectural governance.

**Tools included:**
- **Application Categorisation:** Classify applications as Application, Technology, or Platform using enterprise architecture principles
- **Individual Application to Capability Mapping:** Map single applications to multiple organisational capabilities with detailed analysis
- **Application to Capability Mapping:** Bulk mapping of applications to capabilities with structured analysis

**Typical workflow:** Categorise → Map to Capabilities → Analyse Architecture

### 📊 Engagement Planning Toolkit
*Structure and optimise client engagements*

Designed for engagement managers and senior consultants planning complex organisational transformation projects with multiple workstreams.

**Tools included:**
- **Engagement Structure Generator:** Create comprehensive engagement structures with workstreams, activities, and resource allocation

**Typical workflow:** Define Scope → Generate Structure → Refine Planning

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
openai>=1.0.0
langchain>=0.1.0
langchain-community>=0.0.20
langchain-openai>=0.0.5
numpy>=1.24.0
```

### Project Structure
```
consultingToolkit/
├── main.py                    # Application entry point and routing
├── app_config.py             # AI model configuration and prompts
├── requirements.txt          # Python dependencies
├── run.sh                   # Startup script
├── .streamlit/
│   └── secrets.toml         # OpenAI API configuration
└── modules/
    ├── home_page.py         # Landing page and toolkit overview
    ├── pain_point_toolkit/  # Pain point analysis tools
    ├── capability_toolkit/  # Capability design tools
    ├── applications_toolkit/# Enterprise architecture tools
    ├── engagement_planning_toolkit/ # Engagement planning tools
    └── strategy_motivations_toolkit/ # Strategic analysis tools
```

## 🎯 Key Features

### AI-Powered Analysis
- **Advanced Prompting:** Sophisticated prompt engineering for accurate business analysis
- **Australian English:** Consistent professional terminology and grammar
- **Context Awareness:** Deep understanding of consulting frameworks and methodologies

### Professional Outputs
- **Excel Generation:** Multi-sheet workbooks with structured analysis
- **SWOT Analysis:** Individual strategic assessments for each initiative
- **Mapping Tables:** Complete traceability between inputs and outputs
- **Unique Identifiers:** Systematic ID assignment for tracking and reference

### Enterprise Architecture Integration
- **Application Classification:** Technology, Application, and Platform categorisation
- **Capability Mapping:** Multi-dimensional capability-to-solution alignment
- **Strategic Alignment:** End-to-end traceability from tactics to strategies

### User Experience
- **Intuitive Navigation:** Clear toolkit organisation with contextual workflows
- **Progress Tracking:** Session state management for complex analysis workflows
- **Professional Interface:** Clean, consultant-friendly design with clear information hierarchy

## 📚 Usage Examples

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
