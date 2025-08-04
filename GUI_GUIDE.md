# Voice Recorder GUI Applications

This guide shows you how to use the native macOS GUI voice recorder applications we've created.

## 🎤 Available Applications

### 1. **Voice Recorder GUI** (`voice_recorder_gui.py`)
A full-featured voice recording application with a modern dark interface.

### 2. **Floating Voice Recorder** (`floating_voice_recorder.py`)
A popup/floating window that can be triggered from anywhere.

### 3. **Voice Recorder Launcher** (`launch_voice_recorder.py`)
A launcher script to control the floating recorder.

## 🚀 How to Run

### Method 1: Direct Python Execution
```bash
# Full GUI application
python3 voice_recorder_gui.py

# Floating popup recorder
python3 floating_voice_recorder.py

# Launcher with commands
python3 launch_voice_recorder.py show
python3 launch_voice_recorder.py hide
python3 launch_voice_recorder.py toggle
```

### Method 2: Shell Script
```bash
# Make executable (if not already done)
chmod +x run_gui.sh

# Run the GUI
./run_gui.sh
```

### Method 3: Quick Launch
```bash
# Show floating recorder
python3 launch_voice_recorder.py show

# Hide floating recorder
python3 launch_voice_recorder.py hide

# Toggle floating recorder
python3 launch_voice_recorder.py toggle
```

## 🎯 Features

### Voice Recorder GUI
- **Modern Dark Interface**: Clean, professional look
- **Audio Visualization**: Real-time audio level meter
- **One-Click Recording**: Click microphone to start/stop
- **Settings Panel**: Adjustable recording duration
- **Command Parsing**: Automatically parses voice commands
- **Status Display**: Shows transcription and command status

### Floating Voice Recorder
- **Always on Top**: Stays above other applications
- **Draggable**: Click and drag to move around screen
- **Minimal Interface**: Compact design for quick access
- **Keyboard Shortcuts**: Press Escape to close
- **Popup Behavior**: Can be triggered from anywhere

## 🎨 Interface Elements

### Recording Button
- **Red Circle**: Click to start recording
- **Stop Icon**: Changes to stop button when recording
- **Hover Effects**: Visual feedback on interaction

### Audio Visualizer
- **11 White Bars**: Simulated audio level meter
- **Animated**: Bars move during recording
- **Realistic**: Mimics actual audio input levels

### Settings Gear
- **Grey Button**: Access settings panel
- **Duration Slider**: Adjust recording time (3-10 seconds)
- **Modal Dialog**: Settings window

## 🎤 How to Use

### Basic Recording
1. **Launch the application**
   ```bash
   python3 voice_recorder_gui.py
   ```

2. **Click the microphone button** (red circle)
   - Button turns to stop icon
   - Audio visualizer starts animating
   - Status shows "Recording... Speak now!"

3. **Speak your command**
   - Try: "build app type react name my-app"
   - Or: "record meeting duration 30 minutes"

4. **Click the stop button** (or wait for auto-stop)
   - Processing begins
   - Transcription appears
   - Command is parsed

### Voice Commands to Try
- `"build app type react name my-app"`
- `"record meeting duration 30 minutes"`
- `"analyze meeting file zoom-recording.mp4"`
- `"create component type button props onClick text"`

## 🔧 Advanced Usage

### Floating Recorder
```bash
# Show floating recorder
python3 launch_voice_recorder.py show

# The recorder will appear as a floating window
# Drag it around the screen
# Click the microphone to record
# Press Escape to close
```

### Integration with Desktop Automation
The GUI applications are designed to integrate with your desktop automation system:

```python
# Example: Handle voice commands from GUI
def handle_voice_command(command):
    if command["command"] == "build-app":
        app_type = command["parameters"].get("type")
        app_name = command["parameters"].get("name")
        # Trigger your app building logic
        build_application(app_type, app_name)
```

### Keyboard Shortcuts
- **Escape**: Close floating recorder
- **Click and Drag**: Move floating window
- **Click Microphone**: Start/stop recording

## 🛠️ Troubleshooting

### GUI Not Appearing
```bash
# Check if dependencies are installed
pip3 install customtkinter pillow

# Check if Whisper is working
python3 test_whisper.py
```

### Recording Issues
- **Check microphone permissions** in System Preferences
- **Speak clearly and loudly**
- **Ensure quiet environment**

### Performance Issues
- **Close other applications** using microphone
- **Restart the application** if it becomes unresponsive
- **Check system resources** (CPU, memory)

## 🎯 Integration Examples

### With Hammerspoon (Desktop Automation)
```lua
-- In your Hammerspoon config
function handleVoiceCommand(command)
    if command == "build-app" then
        -- Trigger app building
        hs.execute("npx create-react-app my-app")
    elseif command == "record-meeting" then
        -- Start screen recording
        startScreenRecording()
    end
end
```

### With AppleScript
```applescript
-- Handle voice commands
on handleVoiceCommand(commandText)
    if commandText contains "build app" then
        tell application "Terminal"
            do script "npx create-react-app my-app"
        end tell
    end if
end handleVoiceCommand
```

## 🎉 Success Indicators

When everything is working correctly:
- ✅ GUI appears with dark theme
- ✅ Microphone button responds to clicks
- ✅ Audio visualizer animates during recording
- ✅ Transcription appears after recording
- ✅ Commands are parsed correctly
- ✅ Settings panel opens and works

## 📱 Next Steps

The GUI applications are ready for integration with:
1. **Desktop Automation**: Connect to Hammerspoon/AppleScript
2. **Screen Recording**: Add FFmpeg integration
3. **Local AI**: Connect to Ollama for analysis
4. **Database**: Store command history and patterns

Your voice command system now has a professional GUI interface! 🚀 