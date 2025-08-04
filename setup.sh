#!/bin/bash

# metaVoice Setup Script
# This script helps users set up the metaVoice project

echo "🎤 metaVoice Setup Script"
echo "=========================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    echo "For other platforms, see the documentation"
    exit 1
fi

echo "📋 Checking prerequisites..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew found"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Installing..."
    brew install python@3.11
else
    echo "✅ Python 3 found"
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
brew install portaudio cmake

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Clone Whisper.cpp if not present
if [ ! -d "whisper.cpp" ]; then
    echo "🎙️ Installing Whisper.cpp..."
    git clone https://github.com/ggerganov/whisper.cpp.git
    cd whisper.cpp
    make
    cd ..
else
    echo "✅ Whisper.cpp found"
fi

# Download Whisper model if not present
if [ ! -f "whisper.cpp/models/ggml-base.en.bin" ]; then
    echo "📥 Downloading Whisper model..."
    cd whisper.cpp
    bash ./models/download-ggml-model.sh base.en
    cd ..
else
    echo "✅ Whisper model found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run metaVoice:"
echo "   python3 auto_input_voice_gui.py"
echo ""
echo "📱 To build the app bundle:"
echo "   pyinstaller metaVoice.spec"
echo "   ./install_metaVoice.sh"
echo ""
echo "📖 For more information, see README.md" 