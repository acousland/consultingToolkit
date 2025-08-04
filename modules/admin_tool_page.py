import streamlit as st
import json
import os
import openai
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from app_config import model, load_model_config
from navigation import render_breadcrumbs


def get_available_openai_models():
    """Fetch available OpenAI models from the API and sort by price"""
    try:
        # Get list of available models from OpenAI
        models_response = openai.models.list()
        # Filter for chat models (GPT models)
        chat_models = []
        for model_obj in models_response.data:
            model_id = model_obj.id
            # Include GPT models and o1 models
            if any(prefix in model_id for prefix in ['gpt-3.5', 'gpt-4', 'o1']):
                chat_models.append(model_id)
        
        # Sort models by price (lowest to highest based on typical usage)
        pricing = get_model_pricing()
        
        def get_typical_cost(model_name):
            """Calculate typical cost for sorting (1000 input + 500 output tokens)"""
            if model_name in pricing:
                cost_info = pricing[model_name]
                return (1000 / 1_000_000) * cost_info['input'] + (500 / 1_000_000) * cost_info['output']
            return float('inf')  # Unknown models go to end
        
        # Sort available models by cost
        sorted_models = sorted(chat_models, key=get_typical_cost)
        
        return sorted_models
    except Exception as e:
        st.error(f"Failed to fetch models from OpenAI: {e}")
        # Fallback to common models sorted by price
        fallback_models = ['gpt-4o-mini', 'gpt-3.5-turbo', 'o1-mini', 'gpt-4o', 'gpt-4-turbo', 'o1-preview']
        return fallback_models


def get_dynamic_pricing():
    """Attempt to fetch dynamic pricing from OpenAI API (when available)"""
    try:
        # Note: OpenAI doesn't currently provide a public pricing API
        # This is a placeholder for future implementation
        # For now, we'll return None to indicate static pricing should be used
        return None
    except Exception:
        return None


def get_model_pricing():
    """Get pricing information for OpenAI models with dynamic updates when possible"""
    
    # Try to get dynamic pricing first
    dynamic_pricing = get_dynamic_pricing()
    if dynamic_pricing:
        return dynamic_pricing
    
    # Fallback to static pricing (updated August 2024)
    # Pricing per 1M tokens (input/output) in USD
    pricing = {
        'o1-preview': {'input': 15.00, 'output': 60.00, 'reasoning': True, 'last_updated': '2024-08-04'},
        'o1-mini': {'input': 3.00, 'output': 12.00, 'reasoning': True, 'last_updated': '2024-08-04'},
        'o1': {'input': 15.00, 'output': 60.00, 'reasoning': True, 'last_updated': '2024-08-04'},  # o1 alias
        'gpt-4o': {'input': 5.00, 'output': 15.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-turbo': {'input': 10.00, 'output': 30.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-turbo-2024-04-09': {'input': 10.00, 'output': 30.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-turbo-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-0125-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-1106-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4': {'input': 30.00, 'output': 60.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-4-0613': {'input': 30.00, 'output': 60.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-3.5-turbo-0125': {'input': 0.50, 'output': 1.50, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-3.5-turbo-1106': {'input': 1.00, 'output': 2.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        'gpt-3.5-turbo-16k': {'input': 3.00, 'output': 4.00, 'reasoning': False, 'last_updated': '2024-08-04'},
        # Add some potential future/test models with estimated pricing
        'gpt-4.1-nano-2025-04-14': {'input': 0.10, 'output': 0.30, 'reasoning': False, 'last_updated': '2024-08-04', 'experimental': True},
    }
    return pricing


def format_model_simple(model_name):
    """Format model name with simple information"""
    pricing = get_model_pricing()
    if model_name in pricing:
        cost_info = pricing[model_name]
        # Add experimental indicator
        experimental_flag = " ⚠️ EXPERIMENTAL" if cost_info.get('experimental') else ""
        
        if cost_info['reasoning']:
            # For reasoning models, show special note
            return f"{model_name} (🧠 Reasoning Model){experimental_flag}"
        else:
            # For regular models, show simple name
            return f"{model_name} (💬 Chat Model){experimental_flag}"
    else:
        # Unknown model
        return f"{model_name} ⚠️"


def get_model_pricing():
    """Get pricing information for OpenAI models (as of August 2024)"""
    # Pricing per 1M tokens (input/output) in USD
    pricing = {
        'o1-preview': {'input': 15.00, 'output': 60.00, 'reasoning': True},
        'o1-mini': {'input': 3.00, 'output': 12.00, 'reasoning': True},
        'gpt-4o': {'input': 5.00, 'output': 15.00, 'reasoning': False},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60, 'reasoning': False},
        'gpt-4-turbo': {'input': 10.00, 'output': 30.00, 'reasoning': False},
        'gpt-4-turbo-2024-04-09': {'input': 10.00, 'output': 30.00, 'reasoning': False},
        'gpt-4-turbo-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False},
        'gpt-4-0125-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False},
        'gpt-4-1106-preview': {'input': 10.00, 'output': 30.00, 'reasoning': False},
        'gpt-4': {'input': 30.00, 'output': 60.00, 'reasoning': False},
        'gpt-4-0613': {'input': 30.00, 'output': 60.00, 'reasoning': False},
        'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50, 'reasoning': False},
        'gpt-3.5-turbo-0125': {'input': 0.50, 'output': 1.50, 'reasoning': False},
        'gpt-3.5-turbo-1106': {'input': 1.00, 'output': 2.00, 'reasoning': False},
        'gpt-3.5-turbo-16k': {'input': 3.00, 'output': 4.00, 'reasoning': False},
    }
    return pricing


def format_model_with_cost(model_name):
    """Format model name with cost information"""
    pricing = get_model_pricing()
    if model_name in pricing:
        cost_info = pricing[model_name]
        if cost_info['reasoning']:
            # For reasoning models, show special pricing note
            return f"{model_name} | ${cost_info['input']:.2f}/${cost_info['output']:.2f} per 1M tokens (reasoning model)"
        else:
            # For regular models, show input/output pricing
            return f"{model_name} | ${cost_info['input']:.2f}/${cost_info['output']:.2f} per 1M tokens (in/out)"
    else:
        # Unknown pricing
        return f"{model_name} | Pricing not available"


def estimate_call_cost(model_name, input_tokens=1000, output_tokens=500):
    """Estimate cost for a typical API call"""
    pricing = get_model_pricing()
    if model_name in pricing:
        cost_info = pricing[model_name]
        input_cost = (input_tokens / 1_000_000) * cost_info['input']
        output_cost = (output_tokens / 1_000_000) * cost_info['output']
        total_cost = input_cost + output_cost
        return total_cost
    return None


def save_model_config(model_name, temperature):
    """Save model configuration to JSON file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model_config.json")
    config = {
        "openai_model": model_name,
        "temperature": temperature
    }
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Failed to save configuration: {e}")
        return False


def admin_tool_page():
    render_breadcrumbs([("🏠 Home", "Home"), ("⚙️ Admin & Testing Tool", None)])
    
    # Model Configuration Section
    st.markdown("## 🤖 Model Configuration")
    
    # Get current configuration
    current_model_name, current_temperature = load_model_config()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### OpenAI Model Selection")
        
        # Pricing information header
        col_refresh, col_pricing_info = st.columns([1, 2])
        
        with col_refresh:
            # Get available models
            if st.button("🔄 Refresh Models", help="Fetch latest models from OpenAI API"):
                st.session_state.pop('available_models', None)  # Clear cache
        
        with col_pricing_info:
            st.caption("🤖 Available OpenAI models")
            st.caption("💡 Models sorted by cost (most economical first)")
        
        if 'available_models' not in st.session_state:
            with st.spinner("Fetching available models and pricing..."):
                st.session_state.available_models = get_available_openai_models()
        
        available_models = st.session_state.available_models
        
        # Create formatted options with simple information
        model_options = [format_model_simple(model) for model in available_models]
        model_display_dict = dict(zip(model_options, available_models))
        
        # Model selector
        try:
            current_formatted = format_model_simple(current_model_name)
            if current_formatted in model_options:
                current_index = model_options.index(current_formatted)
            else:
                current_index = 0
        except (ValueError, IndexError):
            current_index = 0
            
        selected_model_formatted = st.selectbox(
            "Choose OpenAI Model:",
            model_options,
            index=current_index,
            help="Models sorted by cost (cheapest first). Select the model for all AI operations."
        )
        
        # Get the actual model name from the formatted selection
        selected_model = model_display_dict[selected_model_formatted]
        
        # Legend for model indicators
        with st.expander("📖 Legend - Model Indicators", expanded=False):
            st.markdown("**Model Type Indicators:**")
            st.markdown("• 🧠 **Reasoning Model** - Advanced problem-solving capabilities (o1 series)")
            st.markdown("• 💬 **Chat Model** - Standard conversational AI (GPT series)")
            
            st.markdown("**Warning Indicators:**")
            st.markdown("• ⚠️ **EXPERIMENTAL** - Test/custom model that may not be available in OpenAI API")
            st.markdown("• ⚠️ **(standalone)** - Unknown model or missing pricing information")
            
            st.markdown("**Sorting:**")
            st.markdown("• Models are automatically sorted by cost (most economical first)")
            st.markdown("• This helps you choose budget-friendly options for your consulting work")
        
        # Save configuration button
        config_changed = (selected_model != current_model_name)
        
        if st.button("💾 Save Configuration", disabled=not config_changed, type="primary"):
            if save_model_config(selected_model, current_temperature):  # Keep current temperature
                st.success("✅ Configuration saved successfully!")
                st.info("ℹ️ Please restart the application to apply changes.")
                # Update session state to reflect changes
                st.session_state['config_saved'] = True
            else:
                st.error("❌ Failed to save configuration")
    
    with col2:
        st.markdown("### Current Settings")
        st.info(f"**Active Model:** {current_model_name}")
        st.info(f"**Temperature:** {current_temperature}")
        
        if config_changed:
            st.warning("⚠️ Unsaved changes detected")
            st.markdown(f"**Selected Model:** {selected_model}")
            st.markdown("**Temperature:** No change (kept current setting)")
    
    st.markdown("---")
    
    # Connection Check Section
    st.markdown("## 🔗 Connection Check")

    # Check for OpenAI API key
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        st.success("✅ OpenAI API key detected")
    else:
        st.error("❌ OpenAI API key not found in Streamlit secrets")

    # Display configured model name - try multiple methods for compatibility
    model_name = None
    
    # Method 1: Try to get from model object attributes
    if hasattr(model, 'model'):
        model_name = model.model
    elif hasattr(model, 'model_name'):
        model_name = model.model_name
    
    # Method 2: Fallback to reading directly from config file
    if not model_name or model_name == "Unknown":
        try:
            model_name, _ = load_model_config()
        except Exception as e:
            st.error(f"Config read error: {e}")
    
    # Method 3: Final fallback
    if not model_name:
        model_name = "Configuration Error"
    
    st.info(f"**Currently loaded model:** {model_name}")
    
    # Debug information (can be removed later)
    with st.expander("🔍 Debug Information", expanded=False):
        st.write("**Model object attributes:**")
        model_attrs = [attr for attr in dir(model) if not attr.startswith('_')]
        st.write(model_attrs[:10])  # Show first 10 attributes
        
        st.write("**Model object type:**")
        st.write(type(model).__name__)
        
        # Show config file contents
        try:
            config_model, config_temp = load_model_config()
            st.write(f"**Config file model:** {config_model}")
            st.write(f"**Config file temperature:** {config_temp}")
        except Exception as e:
            st.write(f"**Config read error:** {e}")

    if st.button("🧪 Run Connectivity Test", type="primary"):
        with st.spinner("Testing connection to model..."):
            try:
                # Import the current model from app_config to ensure we have the latest instance
                from app_config import model as current_model
                
                # Validate that we have a proper model object
                if not hasattr(current_model, 'invoke'):
                    st.error("❌ Model object is invalid. Please restart the application.")
                    return
                
                # Test the connection
                test_message = [HumanMessage(content="Hello! Please respond with 'Connection successful' to confirm the test.")]
                response = current_model.invoke(test_message)
                
                st.success("✅ Model responded successfully")
                with st.expander("View Response", expanded=True):
                    st.write(response.content)
                    
            except ImportError as e:
                st.error(f"❌ Failed to import model: {e}")
                st.markdown("**Solution:** Restart the application to reload the model configuration.")
            except AttributeError as e:
                st.error(f"❌ Model configuration error: {e}")
                st.markdown("**Solutions:**")
                st.markdown("- Restart the application")
                st.markdown("- Check that the selected model name is valid")
                st.markdown("- Verify your OpenAI API key has access to the selected model")
            except Exception as e:
                st.error(f"❌ Failed to connect: {e}")
                st.markdown("**Troubleshooting suggestions:**")
                st.markdown("- Check your OpenAI API key in Streamlit secrets")
                st.markdown("- Verify your internet connection")
                st.markdown("- Ensure the selected model is available in your OpenAI account")
                st.markdown("- Try restarting the application if you recently changed models")
                
                # Show additional info for experimental models
                current_model_name = getattr(current_model, "model_name", None) or getattr(current_model, "model", None)
                if current_model_name and "experimental" in str(current_model_name).lower():
                    st.warning("⚠️ You're using an experimental model that may not be available in the OpenAI API.")


