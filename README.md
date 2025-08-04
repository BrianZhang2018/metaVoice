# metaVoice - Voice-Powered Desktop Automation

A modern desktop automation system that uses voice commands to control your computer, with a beautiful GUI and easy macOS app bundle installation.

## 🎤 Features

- **🎙️ Voice Command Recognition**: Local speech-to-text using Whisper.cpp
- **🖥️ Desktop Automation**: Control applications and perform tasks via voice
- **🎨 Modern GUI**: Clean, dark interface with real-time feedback
- **📱 Native macOS App**: Easy installation with `.app` bundle
- **🔒 Privacy-First**: Everything runs locally on your machine
- **📊 Usage Statistics**: Track your productivity and efficiency
- **🪟 Floating Recorder**: Minimize to a compact floating window

## 🚀 Quick Installation

### Option 1: macOS App installation (for normal user)
```bash
# 1. Clone the repository
git clone https://github.com/BrianZhang2018/metaVoice.git
cd metaVoice
# 2. Install dependencies and setup
./setup.sh
# 3. Build the app bundle
pyinstaller metaVoice.spec
# 4. Install to macos Applications
sh ./install_metaVoice.sh
```

### Option 2: Development Setup
```bash
# Clone the repository
git clone https://github.com/BrianZhang2018/metaVoice.git
cd metaVoice
# Run the setup script
./setup.sh
# Run the dashboard GUI
python3 auto_input_voice_gui.py
# Run the floatwindow GUI
python3 floating_recorder.py
```

## 📱 Using metaVoice

### First Time Setup
1. **Launch** `metaVoice.app` from macos Applications
2. **Grant permissions** for microphone access
3. **Optional**: Grant accessibility permissions for automation
4. **Start recording** with the microphone button

## 🏗️ Project Structure

```
metaVoice/
├── Core Application:
│   ├── auto_input_voice_gui.py      # Main GUI application
│   ├── whisper_wrapper.py           # Speech recognition wrapper
│   ├── text_input_automation.py     # Desktop automation
│   └── floating_recorder.py         # Floating recorder window
├── App Bundle:
│   ├── metaVoice.spec              # PyInstaller configuration
│   ├── runtime_hook.py             # Path resolution for bundled app
│   └── install_metaVoice.sh        # Installation script
├── Setup & Configuration:
│   ├── setup.sh                    # Automated setup script
│   ├── requirements.txt            # Python packages
│   └── setup_permissions.py        # Permission setup utility
├── Development:
│   ├── examples/                   # Usage examples
│   └── tests/                      # Test files
└── Documentation:
    └── docs/                       # Detailed documentation
```

## whisper.cpp is an external dependency for voice engine

**✅ How It Works:**
The setup script automatically handles whisper.cpp:
```bash
# In setup.sh - automatically downloads and builds
if [ ! -d "whisper.cpp" ]; then
    echo "🎙️ Installing Whisper.cpp..."
    git clone https://github.com/ggerganov/whisper.cpp.git
    cd whisper.cpp
    make
    cd ..
fi
```

**Build Output:**
- `dist/metaVoice.app` - The macOS application bundle
- `build/` - PyInstaller build artifacts (can be deleted after build)

### Adding New Commands
Modify the `parse_command` method in `whisper_wrapper.py`:

```python
command_patterns = {
    "your-new-command": {
        "keywords": ["your", "keywords"],
        "required_params": ["param1", "param2"]
    }
}
```

## 🛠️ Troubleshooting

### App Won't Launch
- Check microphone permissions in System Preferences
- Try launching from Applications folder
- Restart the app if first launch fails

### No Voice Recognition
- Verify microphone is working in other apps
- Check microphone permissions
- Ensure quiet environment for better recognition

### Text Not Being Sent
- Grant accessibility permissions for automation
- Check target application selection
- Try clipboard input method


## 🎯 Supported Commands - coming

The system recognizes structured commands:

### Application Development
- `"build app type [react/vue/angular] name [app-name]"`
- `"create component type [button/input/form] props [properties]"`

### Meeting Management
- `"record meeting duration [minutes]"`
- `"analyze meeting file [filename]"`

### General Automation
- `"open application [app-name]"`
- `"search for [query]"`

## License

This project uses Whisper.cpp which is licensed under the MIT License. 