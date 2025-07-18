#!/bin/bash

# Build script for creating macOS .app bundle
# This script automates the py2app build process

set -e  # Exit on any error

echo "🚀 Building Consulting Toolkit macOS App..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "🐍 Using Python: $PYTHON_CMD"

# Check if py2app is installed
if ! $PYTHON_CMD -c "import py2app" 2>/dev/null; then
    echo "📦 Installing py2app..."
    $PYTHON_CMD -m pip install py2app
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Create the .app bundle
echo "🔨 Building .app bundle..."
$PYTHON_CMD setup.py py2app

# Check if build was successful
if [ -d "dist/Consulting Toolkit.app" ]; then
    echo "✅ Build successful!"
    echo "📱 App bundle created: dist/Consulting Toolkit.app"
    echo ""
    echo "📋 Next steps:"
    echo "1. Test the app: open 'dist/Consulting Toolkit.app'"
    echo "2. Create .streamlit/secrets.toml with your OpenAI API key"
    echo "3. The app will automatically open in your browser"
    echo ""
    echo "📦 To distribute:"
    echo "- Copy the entire 'Consulting Toolkit.app' folder"
    echo "- Users need to add their OpenAI API key to .streamlit/secrets.toml"
    echo "- Or create a .dmg file for easier distribution"
else
    echo "❌ Build failed - .app bundle not found"
    exit 1
fi
