"""
Setup script for creating a macOS .app bundle using py2app
"""
from setuptools import setup
import os

# Read version or set default
VERSION = "1.0.0"

# Application metadata
APP_NAME = "Consulting Toolkit"
APP_BUNDLE_ID = "com.consultingtoolkit.app"

# Main application entry point
APP = ['app_launcher.py']

# Data files to include
DATA_FILES = [
    ('', ['main.py']),  # Include main.py in the root of Resources
    ('modules', ['modules']),
    ('.streamlit', ['.streamlit']),
    ('', ['requirements.txt', 'README.md', 'LICENSE']),
]

# Options for py2app
OPTIONS = {
    'argv_emulation': False,  # Disable argv emulation to avoid Carbon framework issues
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': f"{APP_NAME} {VERSION}",
        'CFBundleIdentifier': APP_BUNDLE_ID,
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'NSHumanReadableCopyright': "Copyright © 2025 Consulting Toolkit",
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
        'LSUIElement': False,
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True,
            'NSAllowsLocalNetworking': True,
        },
        'LSEnvironment': {
            'PYTHONPATH': os.path.join(os.getcwd(), 'modules'),
        },
    },
    'packages': [
        'streamlit',
        'pandas',
        'openpyxl',
        'openai',
        'langchain',
        'langchain_openai',
        'langchain_core',
        'modules',
    ],
    'includes': [
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_run_context',
        'streamlit.runtime.state',
        'streamlit.runtime.caching',
        'streamlit.elements',
        'streamlit.components.v1',
        'pkg_resources',
        'altair',
        'plotly',
        'PIL',
        'watchdog',
        'tornado',
        'click',
        'toml',
        'pytz',
        'dateutil',
        'tzlocal',
        'validators',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'packaging',
        'importlib_metadata',
        'typing_extensions',
        'markdown',
        'protobuf',
        'pyarrow',
        'gitpython',
        'semver',
        'rich',
        'tenacity',
        'cachetools',
        'blinker',
        'jsonschema',
        'pympler',
        'pydeck',
        'cmath',
        'math',
        'decimal',
        'fractions',
    ],
    'excludes': [
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'matplotlib',
        'numpy.distutils',
        'scipy',
        'sklearn',
        'IPython',
        'jupyter',
        'notebook',
        'zmq',
        'tornado.test',
        'test',
        'tests',
        'testing',
    ],
    'resources': [
        'modules',
        '.streamlit',
    ],
    'iconfile': None,  # Add path to .icns file if you have one
    'strip': False,
    'optimize': 0,
    'semi_standalone': False,
    'site_packages': True,
    'arch': 'universal2',  # Support both Intel and Apple Silicon
    'emulate_shell_environment': True,
    'no_chdir': True,
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'streamlit',
        'pandas',
        'openpyxl',
        'openai',
        'langchain',
        'langchain-openai',
    ],
)
