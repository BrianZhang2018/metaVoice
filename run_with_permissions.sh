#!/bin/bash

echo "🚀 metaVoice - Running with proper permissions for hotkeys"
echo ""

# Check if running as administrator
if [[ $EUID -eq 0 ]]; then
    echo "✅ Running as administrator - hotkeys should work"
    echo ""
    echo "Starting metaVoice..."
    python main.py
else
    echo "⚠️  Not running as administrator"
    echo "Global hotkeys require administrator privileges on macOS"
    echo ""
    echo "Options:"
    echo "1. Run with sudo (recommended for hotkeys):"
    echo "   sudo python main.py"
    echo ""
    echo "2. Run without hotkeys (current):"
    echo "   python main.py"
    echo ""
    echo "3. Grant accessibility permissions manually:"
    echo "   - Go to System Preferences > Security & Privacy > Privacy > Accessibility"
    echo "   - Add Terminal or your IDE to the list"
    echo ""
    
    read -p "Do you want to run with sudo for hotkey support? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Starting with sudo..."
        sudo python main.py
    else
        echo "Starting without hotkeys..."
        python main.py
    fi
fi
