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

### Option 1: Download Pre-built App (Easiest - No Python Required)
```bash
# Download the pre-built metaVoice.app
# (Coming soon - direct download link)

# Drag and drop to Applications folder
# Or use the installer script
```

### Option 2: Build from Source (For Developers)
```bash
# 1. Clone the repository
git clone https://github.com/BrianZhang2018/metaVoice.git
cd metaVoice

# 2. Install dependencies and setup
./setup.sh

# 3. Build the app bundle
pyinstaller metaVoice.spec

# 4. Install to Applications
sh ./install_metaVoice.sh

# 5. Test the installation
open /Applications/metaVoice.app
```

### Option 3: Create Distribution Package (For Sharing)
```bash
# After building the app bundle, create a distribution package
./package_for_distribution.sh

# This creates:
# - metaVoice-distribution/ (folder with app and installers)
# - metaVoice-macOS.zip (ready to share with non-developers)
```

## 📦 Distribution for Non-Developers

The `package_for_distribution.sh` script creates a complete distribution package that includes:

- **metaVoice.app** - Pre-built application bundle
- **install.sh** - Automated installer script
- **Install metaVoice.command** - Drag-and-drop installer
- **README.txt** - User instructions

Users without Python can simply:
1. Download the ZIP file
2. Extract it
3. Double-click "Install metaVoice.command"
4. Use the app!

**Build Output:**
- `dist/metaVoice.app` - The macOS application bundle
- `build/` - PyInstaller build artifacts (can be deleted after build)

## 📱 Using metaVoice

### First Time Setup
1. **Launch** `metaVoice.app` from macOS Applications
2. **Grant permissions** for microphone access when prompted
3. **Set up text input automation** (required for voice-to-text functionality):
   ```bash
   # Run the permission setup script
   python setup_permissions.py
   ```
   This will help you grant the necessary permissions for automatic text input.
4. **Start recording** with the microphone button in the floating window

### Text Input Automation Setup
For metaVoice to automatically type your voice input into applications (like Cursor), you need to grant accessibility permissions:

1. **Run the setup script**: `python setup_permissions.py`
2. **Follow the prompts** to open System Preferences
3. **Grant permissions** to Python/Terminal in Accessibility settings
4. **Test the automation** to ensure it's working

**Note**: Without these permissions, voice input will be transcribed but won't be automatically typed into applications.

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
The setup script automatically downloads whisper.cpp:
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

### App Won't Launch (Main App Issues)
**Known Issue**: The main.py launcher may have compatibility issues on macOS 15.5 with bundled Tkinter.

**✅ WORKAROUND - Run Individual Components:**
If the main app fails to launch, you can run the components individually:

```bash
# Option 1: Run Dashboard GUI
python auto_input_voice_gui.py

# Option 2: Run Floating Recorder Only
python floating_recorder.py

# Option 3: Run from Source (Most Reliable)
cd /Users/brianzhang/ai/desktopAuto
python auto_input_voice_gui.py  # Dashboard with full features
python floating_recorder.py     # Compact recorder window
```

**Status**: Individual components work perfectly, only the combined launcher has issues.

### No Voice Recognition
- Verify microphone is working in other apps
- Check microphone permissions
- Ensure quiet environment for better recognition

### Text Not Being Sent
- Grant accessibility permissions for automation
- Check target application selection
- Try clipboard input method

### GUI Compatibility Issues
- If packaged app crashes: Use source version instead
- Tkinter compatibility varies by macOS version
- Console mode available as fallback


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