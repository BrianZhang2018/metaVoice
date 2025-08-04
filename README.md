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

### Option 1: macOS App Bundle (Recommended)
```bash
# Download and install
./install_metaVoice.sh

# Or manually drag metaVoice.app to Applications folder
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

### Voice Commands to Try
- `"build app type react name my-app"`
- `"record meeting duration 30 minutes"`
- `"analyze meeting file zoom-recording.mp4"`
- `"create component type button props onClick text"`

### GUI Features
- **🎤 Voice Recording**: Click to start/stop recording
- **📝 Real-time Transcription**: See your speech converted to text
- **🎯 Target App Selection**: Choose where to send text
- **📊 Statistics**: Track your usage and efficiency
- **⚙️ Settings**: Configure input methods and automation

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

## 🤔 Why whisper.cpp is Not Included

**📦 Size & Performance:**
- **whisper.cpp is HUGE**: ~294MB (mostly models)
- **GitHub limits**: Repositories should stay under 1GB
- **Fast cloning**: Small repo downloads quickly
- **Bandwidth efficient**: Users only download what they need

**🔄 Maintenance Benefits:**
- **Always latest version**: Setup script downloads fresh copy
- **No version conflicts**: No need to sync with upstream
- **Automatic updates**: Gets latest whisper.cpp automatically
- **Standard practice**: Most projects exclude large dependencies

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

**Users get whisper.cpp automatically:**
1. **Clone** repo (fast, small)
2. **Run** `./setup.sh` 
3. **Whisper.cpp** downloads and builds
4. **Everything works** seamlessly

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
# Build macOS app bundle
pyinstaller metaVoice.spec

# Install to Applications
./install_metaVoice.sh
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
- Run `./setup.sh` to install all dependencies
- Check that Homebrew is installed
- Verify Python 3.8+ is installed

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

## 🎉 Success!

When everything is working:
- ✅ App launches from Applications folder
- ✅ GUI appears with dark theme
- ✅ Microphone button responds
- ✅ Voice recording and transcription works
- ✅ Text can be sent to target applications

## 📞 Getting Help

- **Installation**: Run `./setup.sh` for automated setup
- **Usage**: See GUI features section above
- **Development**: See development section
- **Issues**: Check troubleshooting section

**Enjoy using metaVoice for faster, voice-powered productivity!** 🚀

## License

This project uses Whisper.cpp which is licensed under the MIT License. 