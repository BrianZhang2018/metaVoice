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
git clone <your-repo-url>
cd desktopAuto

# Install dependencies
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
desktopAuto/
├── Core Application:
│   ├── auto_input_voice_gui.py      # Main GUI application
│   ├── whisper_wrapper.py           # Speech recognition wrapper
│   ├── text_input_automation.py     # Desktop automation
│   └── floating_recorder.py         # Floating recorder window
├── App Bundle:
│   ├── metaVoice.spec              # PyInstaller configuration
│   ├── runtime_hook.py             # Path resolution for bundled app
│   └── install_metaVoice.sh        # Installation script
├── Documentation:
│   ├── INSTALLATION_GUIDE.md       # User installation guide
│   ├── GUI_GUIDE.md               # Interface documentation
│   ├── HOW_TO_RUN.md              # Development setup
│   └── HOTKEY_GUIDE.md            # Hotkey configuration
├── Dependencies:
│   ├── requirements.txt            # Python packages
│   └── whisper.cpp/               # Speech recognition engine
├── Development:
│   ├── examples/                  # Usage examples
│   ├── tests/                     # Test files
│   └── docs/                      # Detailed documentation
└── Setup:
    └── setup_permissions.py       # Permission setup utility
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

## 📞 Getting Help

- **Installation**: See `INSTALLATION_GUIDE.md`
- **Usage**: See `GUI_GUIDE.md`
- **Development**: See `HOW_TO_RUN.md`
- **Issues**: Check troubleshooting section above

## 🎉 Success!

When everything is working:
- ✅ App launches from Applications folder
- ✅ GUI appears with dark theme
- ✅ Microphone button responds
- ✅ Voice recording and transcription works
- ✅ Text can be sent to target applications

**Enjoy using metaVoice for faster, voice-powered productivity!** 🚀

## License

This project uses Whisper.cpp which is licensed under the MIT License. 