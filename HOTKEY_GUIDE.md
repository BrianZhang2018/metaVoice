# Hotkey Guide for metaVoice Floating Recorder

## Available Hotkeys

### Primary Hotkeys (macOS)
- **Cmd+Shift+Space** - Start/Stop recording
- **Cmd+Shift+R** - Show/Hide floating window

### Alternative Hotkeys (if primary fail)
- **Ctrl+Shift+Space** - Start/Stop recording  
- **Ctrl+Shift+R** - Show/Hide floating window

## Setup Instructions

### macOS Permissions
The hotkeys require accessibility permissions on macOS:

1. **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
2. Add your terminal application (Terminal, iTerm2, etc.) or IDE (VS Code, Cursor, etc.)
3. Check the box to enable accessibility access
4. Restart your terminal/IDE

### Troubleshooting

If hotkeys don't work:
1. **Check permissions** - Make sure your terminal/IDE has accessibility access
2. **Use alternative hotkeys** - Try Ctrl+Shift+Space and Ctrl+Shift+R
3. **Use buttons** - The floating window buttons work without permissions
4. **Restart application** - Sometimes permissions need a restart to take effect

## Visual Indicators

The floating window shows:
- **Hotkey status** - Small label at bottom shows available hotkeys
- **Recording status** - Button changes color and icon when recording
- **Audio visualization** - Bars show audio levels during recording
- **Window controls** - Minimize (−), Close (×), and Settings (⚙️) buttons

## Window Controls

The floating window has three control buttons on the right side with macOS-style colors:

- **Hide (−)** - Yellow button, hides the window (since minimize doesn't work with borderless windows)
- **Close (×)** - Red button, closes the application (with confirmation dialog)
- **Settings (⚙️)** - Green button, opens the main dashboard

The buttons are styled to look like native macOS window controls with proper colors and hover effects.

### Important Note About Hide Function
Since the floating window is borderless (`overrideredirect=True`), it cannot be minimized to the dock. Instead, the yellow button hides the window. To restore it:

1. **Use hotkey**: Press `Cmd+Shift+R` (if permissions are granted)
2. **Use restore script**: Run `python restore_floating_recorder.py`
3. **Restart manually**: Run `python floating_recorder.py`

## Usage Tips

1. **Quick recording** - Press Cmd+Shift+Space anywhere to start recording
2. **Window management** - Press Cmd+Shift+R to show/hide the floating window
3. **Window controls** - Use the buttons on the right side of the floating window:
   - **Minimize (−)** - Minimize to dock
   - **Close (×)** - Exit application
   - **Settings (⚙️)** - Open dashboard
4. **Visual feedback** - Watch the floating window for status updates
5. **Fallback** - If hotkeys fail, use the floating window buttons

## Testing Hotkeys

Run the test script to verify hotkey functionality:
```bash
python test_hotkeys.py
```

This will show if hotkeys are working or if permissions are needed. 