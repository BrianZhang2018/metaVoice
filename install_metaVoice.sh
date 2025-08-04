#!/bin/bash

# metaVoice Installation Script
# This script installs metaVoice to your Applications folder

echo "🎤 metaVoice Installation Script"
echo "=================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    exit 1
fi

# Check if app bundle exists
if [ ! -d "dist/metaVoice.app" ]; then
    echo "❌ metaVoice.app not found in dist/ directory"
    echo "Please run the build process first"
    exit 1
fi

echo "📦 Installing metaVoice to Applications..."
echo ""

# Remove existing installation if it exists
if [ -d "/Applications/metaVoice.app" ]; then
    echo "🗑️  Removing existing installation..."
    rm -rf "/Applications/metaVoice.app"
fi

# Copy the app bundle to Applications
echo "📋 Copying metaVoice.app to Applications..."
cp -R "dist/metaVoice.app" "/Applications/"

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