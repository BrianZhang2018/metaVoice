#!/bin/bash

# metaVoice Distribution Packaging Script
# This script creates a distributable package for non-developers

echo "📦 metaVoice Distribution Packaging"
echo "===================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    exit 1
fi

# Check if app bundle exists
if [ ! -d "dist/metaVoice.app" ]; then
    echo "❌ metaVoice.app not found in dist/ directory"
    echo "Please run the build process first:"
    echo "  pyinstaller metaVoice.spec"
    exit 1
fi

# Create distribution directory
DIST_DIR="metaVoice-distribution"
echo "📁 Creating distribution package..."

# Clean up old distribution
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
fi

mkdir -p "$DIST_DIR"

# Copy the app bundle
echo "📋 Copying metaVoice.app..."
cp -R "dist/metaVoice.app" "$DIST_DIR/"

# Create installation script
echo "🔧 Creating installation script..."
cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash

echo "🎤 metaVoice Installation"
echo "========================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    exit 1
fi

echo "📦 Installing metaVoice to Applications..."

# Remove existing installation if it exists
if [ -d "/Applications/metaVoice.app" ]; then
    echo "🗑️  Removing existing installation..."
    rm -rf "/Applications/metaVoice.app"
fi

# Copy the app bundle to Applications
echo "📋 Copying metaVoice.app to Applications..."
cp -R "metaVoice.app" "/Applications/"

# Set proper permissions
echo "🔐 Setting permissions..."
chmod +x "/Applications/metaVoice.app/Contents/MacOS/metaVoice"

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎉 metaVoice has been installed to /Applications/metaVoice.app"
echo ""
echo "📱 To use metaVoice:"
echo "   1. Open Applications folder"
echo "   2. Double-click metaVoice.app"
echo "   3. Grant microphone and accessibility permissions when prompted"
echo ""
echo "🔧 First time setup:"
echo "   - The app will request microphone access"
echo "   - You may need to grant accessibility permissions in System Preferences"
echo "   - Go to System Preferences → Security & Privacy → Privacy → Accessibility"
echo "   - Add metaVoice.app to the list"
echo ""
echo "🚀 Enjoy using metaVoice!"
EOF

chmod +x "$DIST_DIR/install.sh"

# Create README for distribution
echo "📄 Creating README..."
cat > "$DIST_DIR/README.txt" << 'EOF'
metaVoice - Voice-Powered Desktop Automation
============================================

This is a pre-built version of metaVoice for macOS.

INSTALLATION:
1. Double-click "install.sh" to install to Applications
2. Or manually drag "metaVoice.app" to your Applications folder

USAGE:
1. Open Applications folder
2. Double-click metaVoice.app
3. Grant microphone permissions when prompted
4. Start using voice commands!

FEATURES:
- Voice-to-text transcription
- Desktop automation
- Modern GUI interface
- Privacy-first (runs locally)

SUPPORT:
- GitHub: https://github.com/BrianZhang2018/metaVoice
- Issues: https://github.com/BrianZhang2018/metaVoice/issues

Enjoy using metaVoice! 🚀
EOF

# Create a simple drag-and-drop installer
echo "🎯 Creating drag-and-drop installer..."
cat > "$DIST_DIR/Install metaVoice.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./install.sh
read -p "Press Enter to close..."
EOF

chmod +x "$DIST_DIR/Install metaVoice.command"

# Create ZIP archive
echo "📦 Creating ZIP archive..."
zip -r "metaVoice-macOS.zip" "$DIST_DIR"

echo ""
echo "✅ Distribution package created!"
echo ""
echo "📁 Files created:"
echo "   - $DIST_DIR/ (distribution folder)"
echo "   - metaVoice-macOS.zip (ready for distribution)"
echo ""
echo "🚀 Ready for distribution to non-developers!"
echo ""
echo "📋 Distribution includes:"
echo "   ✅ metaVoice.app (pre-built application)"
echo "   ✅ install.sh (automated installer)"
echo "   ✅ Install metaVoice.command (drag-and-drop installer)"
echo "   ✅ README.txt (user instructions)"
echo ""
echo "📤 Share the ZIP file with users who don't have Python!" 