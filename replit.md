# Consulting Toolkit

## Overview

A comprehensive Streamlit-based application designed for management consultants to systematically analyze organizational challenges, design capabilities, plan engagements, and develop strategic initiatives. The toolkit provides six specialized modules: Pain Point Analysis, Capability Design, Application Architecture, Data & AI, Engagement Planning, and Strategy Development. Each module contains AI-powered tools that process uploaded spreadsheet data and provide structured analysis using OpenAI's language models. The application features a modular architecture with centralized configuration, breadcrumb navigation, and Excel-based data import/export workflows.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses Streamlit as the primary web framework with a single-page application design. Navigation is managed through session state (`st.session_state.page`) with a centralized routing system in `main.py` that dispatches to appropriate page functions. The UI follows a consistent pattern: breadcrumb navigation, tool descriptions, file upload interfaces, column selection widgets, and results display with Excel export functionality. Page-specific modules are organized in toolkit-specific directories under `/modules/`.

### Backend Architecture
The core application logic centers around AI-powered text processing using LangChain and OpenAI integration. The `app_config.py` module provides centralized model configuration with JSON-based settings for model selection and temperature control. Each tool follows a similar pattern: upload Excel/CSV files, select relevant columns, process data in chunks to manage API context windows, send structured prompts to OpenAI models, and return formatted results. The application uses pandas for data manipulation and xlsxwriter for Excel export generation.

### Configuration Management
Model configuration is externalized to `model_config.json` allowing runtime adjustment of OpenAI models and parameters. The application loads configuration at startup and provides model reinitialization capabilities. API keys are managed through Streamlit's secrets system via `.streamlit/secrets.toml` files. The admin tool provides a web interface for model configuration and testing.

### Data Processing Pipeline
Each toolkit follows a consistent data processing pattern: file upload validation, sheet selection for Excel files, column mapping for IDs and descriptive text, chunked processing to handle large datasets within API context limits, structured prompt templates with variable substitution, AI model inference with error handling, and results formatting with Excel export capabilities.

### AI Integration Architecture
The application uses LangChain as the primary interface to OpenAI models with structured prompt templates defined in `prompts.py`. Processing is designed to handle batch operations with configurable chunk sizes to prevent context window overflow. Each tool implements specific prompt engineering patterns optimized for its use case (extraction, mapping, categorization, analysis). Error handling includes retry logic and graceful degradation for API failures.

## External Dependencies

### Core Framework Dependencies
- **Streamlit**: Web application framework providing the user interface
- **pandas**: Data manipulation and analysis for Excel/CSV processing
- **openpyxl & xlsxwriter**: Excel file reading and writing capabilities

### AI and Language Processing
- **OpenAI**: Primary AI service for text analysis and generation
- **LangChain & langchain-openai**: Framework for building AI applications and OpenAI integration
- **urllib3**: HTTP client library with version constraints for compatibility

### Development and Deployment
- **py2app**: macOS application bundling for standalone deployment
- **setuptools**: Python package building and distribution

### External Services
- **OpenAI API**: Required for all AI-powered analysis functionality
- **File System**: Local file storage for temporary data processing and configuration files

### Configuration Requirements
- OpenAI API key must be configured in `.streamlit/secrets.toml`
- Model configuration managed through `model_config.json`
- Optional company dossier files support multiple formats (JSON, XML, HTML, PDF, Word)