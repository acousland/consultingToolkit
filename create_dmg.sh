#!/bin/bash

# Create a distributable .dmg file from the .app bundle
# Run this after build_app.sh completes successfully

set -e

APP_NAME="Consulting Toolkit"
VERSION="1.0.0"
DMG_NAME="ConsultingToolkit-${VERSION}"

echo "📦 Creating distributable .dmg file..."

# Check if .app exists
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ App bundle not found. Run build_app.sh first."
    exit 1
fi

# Create temporary directory for DMG contents
TEMP_DIR=$(mktemp -d)
cp -R "dist/${APP_NAME}.app" "$TEMP_DIR/"

# Create README for users
cat > "$TEMP_DIR/README.txt" << EOF
Consulting Toolkit - Setup Instructions
======================================

1. Drag "Consulting Toolkit.app" to your Applications folder
2. Create a file called "secrets.toml" in the app's .streamlit folder
3. Add your OpenAI API key to secrets.toml:
   OPENAI_API_KEY = "your-api-key-here"
4. Double-click the app to launch

The app will open in your web browser automatically.

For support, visit: https://github.com/acousland/consultingToolkit
EOF

# Create the DMG
echo "🔧 Creating DMG file..."
hdiutil create -volname "$APP_NAME" -srcfolder "$TEMP_DIR" -ov -format UDZO "dist/${DMG_NAME}.dmg"

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ DMG created successfully: dist/${DMG_NAME}.dmg"
echo "📱 Ready for distribution!"
