# How to Run Voice Commands Locally

This guide shows you all the ways to run the Whisper.cpp voice command system on your local machine.

## 🚀 Quick Start

### 1. Test the Installation
```bash
python3 test_whisper.py
```

### 2. Quick Voice Command Test
```bash
python3 quick_test.py
```
This will record 3 seconds of audio and transcribe it.

### 3. Interactive Voice Command System
```bash
python3 run_voice_commands.py
```
This provides a menu-driven interface for testing different features.

## 📝 Different Ways to Run

### Method 1: Command Line Quick Test
```bash
# Record 3 seconds (default)
python3 quick_test.py

# Record 5 seconds
python3 quick_test.py 5

# Record 10 seconds
python3 quick_test.py 10
```

### Method 2: Interactive Menu
```bash
python3 run_voice_commands.py
```
Choose from:
- Record voice command (3 seconds)
- Record voice command (5 seconds)
- Test with sample audio file
- Exit

### Method 3: Use in Your Own Code
```python
from whisper_wrapper import WhisperWrapper

# Initialize
whisper = WhisperWrapper()

# Record and transcribe
text = whisper.transcribe_microphone(duration=5)
print(f"You said: {text}")

# Parse as command
command = whisper.parse_command(text)
print(f"Command: {command}")
```

### Method 4: Transcribe Audio Files
```python
from whisper_wrapper import WhisperWrapper

whisper = WhisperWrapper()

# Transcribe an audio file
result = whisper.transcribe_audio_file("meeting.wav", "json")
print(result["text"])
```

## 🎯 Voice Commands to Try

The system recognizes these structured commands:

### Build Applications
- `"build app type react name my-app"`
- `"create application type vue name todo-app"`
- `"make app type angular name dashboard"`

### Record Meetings
- `"record meeting duration 30 minutes"`
- `"start recording meeting"`
- `"begin meeting recording"`

### Analyze Meetings
- `"analyze meeting file zoom-recording.mp4"`
- `"transcribe meeting file meeting.wav"`
- `"summarize meeting recording"`

### Create Components
- `"create component type button props onClick text"`
- `"make component type input props placeholder"`
- `"build component type form"`

## 🔧 Advanced Usage

### Continuous Listening
```python
from example_usage import VoiceCommandHandler

handler = VoiceCommandHandler()
handler.start_listening()
```

### Custom Command Parsing
```python
# Parse any text as a command
text = "build app type react name my-app"
command = whisper.parse_command(text)
print(command)
# Output: {'command': 'build-app', 'parameters': {'type': 'react', 'name': 'my-app'}, 'original_text': 'build app type react name my-app'}
```

### Different Output Formats
```python
# JSON format (detailed)
result = whisper.transcribe_audio_file("audio.wav", "json")

# Text format (simple)
result = whisper.transcribe_audio_file("audio.wav", "txt")

# SRT format (subtitles)
result = whisper.transcribe_audio_file("audio.wav", "srt")
```

## 🛠️ Troubleshooting

### No Speech Detected
- Make sure your microphone is working
- Speak clearly and loudly
- Check microphone permissions in System Preferences

### PyAudio Errors
```bash
brew install portaudio
pip3 install pyaudio
```

### Whisper.cpp Not Found
```bash
cd whisper.cpp
make clean
make
```

### Model Not Found
```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh base.en
```

## 📊 Performance Tips

### For Real-time Commands
- Use shorter recording durations (3-5 seconds)
- Use the `tiny.en` model for faster processing
- Speak clearly and use structured commands

### For High Accuracy
- Use longer recording durations (5-10 seconds)
- Use the `small.en` model for better accuracy
- Ensure quiet environment

### For File Transcription
- Use the `base.en` or `small.en` model
- Process files in batches for efficiency

## 🔄 Integration Examples

### With Desktop Automation
```python
def handle_voice_command(command):
    if command["command"] == "build-app":
        app_type = command["parameters"].get("type")
        app_name = command["parameters"].get("name")
        # Call your app building function
        build_react_app(app_name)
```

### With Meeting Recording
```python
def record_meeting():
    # Start screen recording
    start_screen_recording()
    
    # Transcribe in real-time
    while recording:
        text = whisper.transcribe_microphone(duration=10)
        save_transcription(text)
```

### With AI Analysis
```python
def analyze_meeting(audio_file):
    # Transcribe meeting
    result = whisper.transcribe_audio_file(audio_file)
    
    # Send to local AI for analysis
    summary = local_ai.analyze(result["text"])
    return summary
```

## 🎉 Success Indicators

When everything is working correctly, you should see:
- ✅ Whisper.cpp initialized successfully
- ✅ Audio recording works
- ✅ Transcription is accurate
- ✅ Command parsing works
- ✅ No error messages

## 📞 Getting Help

If you encounter issues:
1. Run `python3 test_whisper.py` to check installation
2. Check microphone permissions
3. Verify all dependencies are installed
4. Check the troubleshooting section above 