"""
Streamlit app launcher for macOS .app bundle
This script is used as the entry point for the py2app bundle
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def find_main_py():
    """Find the main.py file in the bundle"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle - try different locations
        bundle_dir = Path(sys.executable).parent
        resources_dir = bundle_dir / '..' / 'Resources'
        
        possible_paths = [
            resources_dir / 'main.py',
            bundle_dir / 'main.py',
            bundle_dir / '..' / 'main.py',
            resources_dir / 'lib' / 'python3.13' / 'main.py',
            Path(sys.executable).parent.parent / 'Resources' / 'main.py',
        ]
        
        print(f"🔍 Bundle directory: {bundle_dir}")
        print(f"🔍 Resources directory: {resources_dir}")
        
        for path in possible_paths:
            resolved_path = path.resolve()
            print(f"🔍 Checking: {resolved_path}")
            if resolved_path.exists():
                print(f"✅ Found main.py at: {resolved_path}")
                return str(resolved_path)
        
        # If we can't find main.py, list what's in the Resources directory
        if resources_dir.exists():
            print(f"📁 Contents of Resources directory:")
            for item in resources_dir.iterdir():
                print(f"  - {item.name}")
        
        # Fallback - look for any .py files in Resources
        if resources_dir.exists():
            for py_file in resources_dir.glob('*.py'):
                if py_file.name == 'main.py':
                    return str(py_file)
    
    # Running in development or fallback
    return 'main.py'

def main():
    """
    Main entry point for the Streamlit app
    """
    print("🚀 Starting Consulting Toolkit...")
    
    # Set up the environment
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # Find the main.py file
    main_py = find_main_py()
    print(f"📱 Using main file: {main_py}")
    
    # Check if main.py exists
    if not os.path.exists(main_py):
        print(f"❌ Error: Cannot find main.py at {main_py}")
        input("Press Enter to exit...")
        return
    
    # Start streamlit as a subprocess instead of using sys.argv manipulation
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', main_py,
        '--server.port=8501',
        '--server.address=localhost',
        '--server.headless=true',
        '--browser.gatherUsageStats=false',
        '--global.developmentMode=false',
        '--theme.base=light',
    ]
    
    print("🌐 Starting Streamlit server...")
    
    try:
        # Start the subprocess
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        url = "http://localhost:8501"
        print(f"🔗 Opening browser: {url}")
        webbrowser.open(url)
        
        # Wait for the process to complete
        process.wait()
        
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
