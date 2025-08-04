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

# 4. Install to Applications
sh ./install_metaVoice.sh

# 5. Test the installation
open /Applications/metaVoice.app
```

### Option 2: Development Setup
```bash
# Clone the repository
git clone https://github.com/BrianZhang2018/metaVoice.git
cd metaVoice

# Run the setup script (recommended)
./setup.sh

# Or install manually
pip3 install -r requirements.txt

# Run the GUI
python3 auto_input_voice_gui.py
```

## 📱 Using metaVoice

### First Time Setup
1. **Launch** `metaVoice.app` from Applications
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

## 🔧 Development

### Running from Source
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the GUI
python3 auto_input_voice_gui.py

# Run tests
python3 tests/test_whisper.py
```

### Building the App Bundle
```bash
# First, ensure dependencies are installed
./setup.sh

# Build macOS app bundle
pyinstaller metaVoice.spec

# Install to Applications
sh ./install_metaVoice.sh
```

### Local Development Build Process
```bash
# 1. Build the app bundle
pyinstaller metaVoice.spec

# 2. Install to Applications (requires sudo for permissions)
sh ./install_metaVoice.sh

# 3. Test the installation
open /Applications/metaVoice.app

# 4. Clean up build artifacts (optional)
rm -rf build/ dist/
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

### Setup Issues
- **Always run `./setup.sh` first** - This installs all dependencies including whisper.cpp
- Check that Homebrew is installed
- Verify Python 3.8+ is installed
- If setup fails, try: `chmod +x setup.sh && ./setup.sh`

### Build Issues
- **Permission denied**: Use `sh ./install_metaVoice.sh` instead of `./install_metaVoice.sh`
- **PyInstaller not found**: Install with `pip3 install pyinstaller`
- **Build fails**: Clean and rebuild with `rm -rf build/ dist/ && pyinstaller metaVoice.spec`
- **App won't launch**: Check microphone permissions in System Preferences

## 📊 Performance Tips

- **Real-time Commands**: Use 3-5 second recordings
- **High Accuracy**: Use 5-10 second recordings in quiet environment
- **Apple Silicon**: Automatic Metal GPU acceleration
- **Memory**: 2GB+ free RAM recommended

## 🎯 Supported Commands

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