# Desktop Automation with Whisper.cpp

A desktop automation system that uses voice commands to control your computer, record and analyze meetings, and learn from your work patterns.

## Features

- **Voice Command Recognition**: Local speech-to-text using Whisper.cpp
- **Desktop Automation**: Control applications and perform tasks via voice
- **Meeting Recording & Analysis**: Record meetings and extract insights
- **Local Learning**: AI-powered assistance that learns from your work patterns
- **Privacy-First**: Everything runs locally on your machine

## Installation

### Prerequisites

- macOS (Apple Silicon recommended for best performance)
- Python 3.8+
- Homebrew
- Git

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd desktopAuto

# Install system dependencies
brew install portaudio cmake

# Install Python dependencies
pip3 install -r requirements.txt
```

### Step 2: Install Whisper.cpp

The installation script will automatically:
- Clone Whisper.cpp repository
- Build the C++ application
- Download the base English model
- Test the installation

```bash
# Run the installation test
python3 test_whisper.py
```

## Usage

### Basic Voice Command Recognition

```python
from whisper_wrapper import WhisperWrapper

# Initialize the wrapper
whisper = WhisperWrapper()

# Transcribe from microphone
text = whisper.transcribe_microphone(duration=5)
print(f"You said: {text}")

# Parse as a command
command = whisper.parse_command(text)
print(f"Command: {command}")
```

### Supported Voice Commands

The system recognizes structured commands in the format:

```
"command: [action] type: [type] name: [name]"
```

**Examples:**
- `"build app type react name my-app"`
- `"record meeting duration 30 minutes"`
- `"analyze meeting file zoom-recording.mp4"`
- `"create component type button props onClick text"`

### Audio File Transcription

```python
# Transcribe an audio file
result = whisper.transcribe_audio_file("meeting.wav", "json")
print(result["text"])
```

## Project Structure

```
desktopAuto/
├── whisper.cpp/           # Whisper.cpp installation
├── whisper_wrapper.py     # Python wrapper for Whisper.cpp
├── test_whisper.py        # Installation and functionality tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

### Whisper Models

The system uses the `ggml-base.en.bin` model by default. You can download other models:

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh tiny.en    # 39MB - Fast
bash ./models/download-ggml-model.sh base.en    # 74MB - Balanced
bash ./models/download-ggml-model.sh small.en   # 244MB - High accuracy
```

### Performance Optimization

For Apple Silicon Macs, the system automatically uses:
- Metal GPU acceleration
- Optimized ARM64 instructions
- Multi-threading

## Development

### Adding New Commands

To add new voice commands, modify the `parse_command` method in `whisper_wrapper.py`:

```python
command_patterns = {
    "your-new-command": {
        "keywords": ["your", "keywords"],
        "required_params": ["param1", "param2"]
    }
}
```

### Testing

Run the test suite:

```bash
python3 test_whisper.py
```

## Troubleshooting

### Common Issues

1. **PyAudio Installation Fails**
   ```bash
   brew install portaudio
   pip3 install pyaudio
   ```

2. **Whisper.cpp Build Fails**
   ```bash
   cd whisper.cpp
   make clean
   make
   ```

3. **Model Download Fails**
   ```bash
   cd whisper.cpp
   bash ./models/download-ggml-model.sh base.en
   ```

### Performance Tips

- Use the `tiny.en` model for real-time applications
- Use the `small.en` model for high-accuracy transcription
- Ensure adequate free memory (2GB+ recommended)

## Next Steps

This is the foundation for your desktop automation system. Next components to add:

1. **Desktop Automation**: Integrate with Hammerspoon/AppleScript
2. **Screen Recording**: Add FFmpeg for meeting recording
3. **Local AI**: Add Ollama for meeting analysis
4. **Database**: Add SQLite for storing patterns and history
5. **GUI**: Create a user interface for configuration

## License

This project uses Whisper.cpp which is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request 